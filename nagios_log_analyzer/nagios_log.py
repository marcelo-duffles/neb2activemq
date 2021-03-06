#!/usr/bin/env python
#coding: utf-8

import glob

class NagiosLog(object):
    '''This class analysis a Nagios log'''


    def __init__(self, log_filename):
        self.filename = log_filename
        log_file_object = open(log_filename)
        self.lines = log_file_object.readlines()
        log_file_object.close()
        self.service_descriptions = None
        self.descriptions_and_commands = None
        self.commands_and_outputs = None


    def cleanup(self, update=True, save_in_file=None):
        '''Kind of messages to exclude:
        [1268192123] Auto-save of retention data completed successfully.
        [1268190013] Warning: Return code of 126 for check of service 'xxx' on host 'zzz' was out of bounds. Make sure the plugin you're trying to run actually exists.
        [1268225809] Local time is Wed Mar 10 09:56:49 BRT 2010
        [1268225809] LOG VERSION: 2.0
        [1268225922] EXTERNAL COMMAND: RESTART_PROGRAM;1268225922
        [1268225809] PROGRAM_RESTART event encountered, restarting...
        [1268225809] Nagios 3.2.0 starting... (PID=3443)
        [1268227762] SERVICE FLAPPING ALERT: zes-001;cpu;STARTED; Service appears to have started flapping (22.3% change >= 20.0% threshold)
        [1271265737] neb2ipc: I'm still here! Processing events to activemq
        [1276228945] Event broker module '/iG/nagios/bin/neb2ipc.o' deinitialized successfully.
        [1276225600] SERVICE NOTIFICATION: nagiosadmin;cache-02;Memoria;UNKNOWN;notify-host-by-email;ERROR: netsnmp : No response from remote host 10.10.71.2.

        #TODO We can also the approach of catch just the lines we know, like:
            if ' '.join(line_by_spaces[1:3]) == 'SERVICE ALERT:' or \
               ' '.join(line_by_spaces[1:3]) == 'HOST ALERT:' or \
               ' '.join(line_by_spaces[1:4]) == 'CURRENT HOST STATE:' or \
               ' '.join(line_by_spaces[1:4]) == 'CURRENT SERVICE STATE:':
        '''

        new_lines = []
        for line in self.lines:
            info = line.split()
            prohibited_words = ['Auto-save', 'Warning:', 'Local', 'LOG',
                                'EXTERNAL', 'PROGRAM_RESTART', 'Nagios',
                                'neb2ipc:']
            if info[1] in prohibited_words or info[2] == 'FLAPPING' \
               or not ';' in line or ' '.join(info[1:3]) == 'SERVICE NOTIFICATION:':
                continue
            new_lines.append(line)

        if update:
            self.lines = new_lines

        if save_in_file:
            file_object = open(save_in_file, 'w')
            file_object.writelines(new_lines)
            file_object.close()
        else:
            return new_lines


    def get_service_descriptions(self):
        if not self.service_descriptions:
            descriptions = []
            for line in self.lines:
                info = ': '.join(line.split(': ')[1:])
                description = info.split(';')[1]
                descriptions.append(description)
            self.service_descriptions = list(set(descriptions))
        return self.service_descriptions


    def save_service_descriptions_in(self, filename):
        service_descriptions = self.get_service_descriptions()
        file_object = open(filename, 'w')
        file_object.write('\n'.join(service_descriptions))
        file_object.close()


    def get_service_description_and_check_command(self, list_of_files):
        if not self.descriptions_and_commands:
            services_and_commands = {}
            for conf_file in list_of_files:
                file_object = open(conf_file)
                content = file_object.read()
                services = content.split('define service')[1:]
                for service in services:
                    try:
                        description = service.split('service_description')[1].split('\n')[0].strip()
                    except IndexError:
                        continue
                    command = service.split('check_command')[1].split('\n')[0].strip()
                    if command.startswith('check_nrpe!'):
                        command = command.split('!')[1]
                    services_and_commands[description] = command
                file_object.close()
            self.descriptions_and_commands = services_and_commands
        return self.descriptions_and_commands


    def export_descriptions_and_commands_from_conf(self, conf_files, csvname):
        descriptions_and_commands = \
                self.get_service_description_and_check_command(conf_files)
        csv_file_object = open(csvname, 'w')
        csv_file_object.write('"Service description","Check command"\n')
        for pair in descriptions_and_commands.iteritems():
            csv_file_object.write('"%s","%s"\n' % pair)
        csv_file_object.close()


    def get_not_found_services(self, update=True):
        not_found = []
        for service in self.service_descriptions:
            if service not in self.descriptions_and_commands:
                not_found.append(service)

        if update:
            self.not_found_services = not_found
        return not_found


    def save_not_found_services(self, filename):
        file_object = open(filename, 'w')
        for service in self.get_not_found_services():
            file_object.write(service + '\n')
        file_object.close()


    def remove_not_found_services(self, update=True, save=None):
        new_log = []
        for line in self.lines:
            info = ': '.join(line.split(': ')[1:])
            description = info.split(';')[1]
            if description in self.not_found_services:
                continue
            new_log.append(line)

        if update:
            self.lines = new_log
        if save:
            file_object = open(save, 'w')
            file_object.writelines(new_log)
            file_object.close()
        return new_log


    def get_check_commands_and_outputs(self):
        if not self.commands_and_outputs:
            commands_and_outputs = []
            for i, line in enumerate(self.lines):
                info = ': '.join(line.split(': ')[1:]).split(';')
                check_command = self.descriptions_and_commands[info[1]].split('!')[0]
                if check_command == 'check_nrpe':
                    check_command = self.descriptions_and_commands[info[1]].split('!')[1]
                if 'CURRENT HOST STATE:' in line:
                    check_output = ';'.join(info[4:]).replace('\n', '')
                    state = info[3]
                else:
                    check_output = ';'.join(info[5:]).replace('\n', '')
                    state = info[4]

                commands_and_outputs.append({'check_command': check_command,
                                             'output': check_output,
                                             'state': state})
            self.commands_and_outputs = commands_and_outputs
        return self.commands_and_outputs


def find_command_and_output(commands_and_outputs, command, output):
    for cmd_out in commands_and_outputs:
        if cmd_out['check_command'] == command and cmd_out['output'] == output:
            return True
    return False


def remove_duplicates(commands_and_outputs):
    new_list = []
    for cmd_out in commands_and_outputs:
        command = cmd_out['check_command']
        output = cmd_out['output']
        if not find_command_and_output(new_list, command, output):
            new_list.append(cmd_out)
    return new_list


def group_commands(commands_and_outputs):
    grouped_commands = {}
    for cmd_out in commands_and_outputs:
        command = cmd_out['check_command']
        output = cmd_out['output']
        if command not in grouped_commands:
            grouped_commands[command] = [output]
        else:
            grouped_commands[command].append(output)
    return grouped_commands


def write_grouped_commands(grouped_commands_and_outputs, filename):
    file_object = open(filename, 'w')
    for command, outputs in grouped_commands_and_outputs.iteritems():
        file_object.write('%s\n\t%s\n\n' % (command, '\n\t'.join(outputs)))
    file_object.close()


if __name__ == '__main__':
    import os
    import logging, logging.config
    import sys
    import fnmatch

    def get_all_files(directory, pattern):
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in fnmatch.filter(filenames, pattern):
                filepaths.append(os.path.join(dirpath, f))
        return filepaths

    #For Intelie developers: change '*' in the next lines for the datacenter path
    sys.path.append('/path/to/topics.py') #for topics and parser_functions
    sys.path.append('../ipc2activemq/src/nebpublisher/utils') #for neb_parser
    parent_dir = '/path/to/analysis/directory'
    conf_dir = '/path/to/config/directory'
    log_conf = '../ipc2activemq/src/nebpublisher/conf/log.ini'

    if os.path.isfile(log_conf):
        print "configuring log from log.ini"
        logging.config.fileConfig(log_conf)
    else:
        print "no log.ini was found"
        logging.basicConfig()

    import topics
    import parser_functions
    import neb_parser

    nagios = NagiosLog('%s/nagios.log' % parent_dir)
    nagios.cleanup(save_in_file='%s/nagios-cleanup.log' % parent_dir)
    nagios.save_service_descriptions_in('%s/service_descriptions.txt' % parent_dir)

    conf_files = get_all_files(conf_dir, '*.cfg')
    csvname = '%s/nagios-service_descriptions-and-commands.csv' % parent_dir
    nagios.export_descriptions_and_commands_from_conf(conf_files, csvname)

    nagios.save_not_found_services('%s/nagios-inconsistent.txt' % parent_dir)
    nagios.remove_not_found_services(save='%s/nagios-cleanup-consistent.log' % parent_dir)
    commands_and_outputs = nagios.get_check_commands_and_outputs()

    commands_and_outputs = remove_duplicates(commands_and_outputs)
    grouped_commands = group_commands(commands_and_outputs)
    write_grouped_commands(grouped_commands, '%s/all_commands_grouped.txt' % parent_dir)

    my_parser = neb_parser.Parser(topics, parser_functions)
    total_parsed = 0
    not_parsed = []

    check_command_count = {}
    check_command_count_not_parsed = {}
    for cmd_out in commands_and_outputs:
        command = cmd_out['check_command']
        output  = cmd_out['output']
        state = cmd_out['state']
        message = 'HOST^%s^%s^%s' % (command, state, output)

        if command in check_command_count:
            check_command_count[command] += 1
        else:
            check_command_count[command] = 1

        parsed = my_parser.parse(13, message)
        if parsed != neb_parser.BAD_FORMAT:
            print message
            print command, parsed
            print ''
            total_parsed += 1
        else:
            if command in check_command_count_not_parsed:
                check_command_count_not_parsed[command] += 1
            else:
                check_command_count_not_parsed[command] = 1
            not_parsed.append(cmd_out)

    not_parsed = remove_duplicates(not_parsed)
    not_parsed_grouped = group_commands(not_parsed)
    write_grouped_commands(not_parsed_grouped, '%s/not_parsed_grouped.txt' % parent_dir)

    if len(not_parsed):
        print ''
        print '--- Events not parsed:'
        for event in not_parsed:
            print '    %s' % event
            print ''

    total_events = len(commands_and_outputs)
    percentual = 100 * float(total_parsed) / total_events if total_events != 0 \
                                                          else 0
    print '--- Total of events: %d' % len(commands_and_outputs)
    print '--- Total of parsed events: %d (%f%%)' % (total_parsed, percentual)

    print '--- Check command count:'
    print '      ' + u'\u02cf' + u'\u02cd' * 96 + u'\u02ce'
    print '      |      SERVICE DESCRIPTION      |         CHECK COMMAND         | # OF EVENTS (not parsed/total) |'
    print '      |' + u'\u02c9' * 31 + '|' + u'\u02c9' * 31 + '|' + u'\u02c9' * 32 + '|'

    yes = u'\u2713' #unicode rules
    no = u'\u2717'

    for description, full_command in nagios.descriptions_and_commands.iteritems():
        command = full_command.split('!')[0]
        if command == 'check_nrpe':
            command = full_command.split('!')[1]
        if command in check_command_count:
            if command in check_command_count_not_parsed:
                not_parsed_count = str(check_command_count_not_parsed[command])
            else:
                not_parsed_count = '0'
            value = not_parsed_count + '/' + str(check_command_count[command])
        else:
            value = '(!) 0'
            not_parsed_count = '0'
        print '      | %29s | %29s | %s %28s |' % (description, command,
                                                   yes if not_parsed_count == '0' else no,
                                                   value)
    print '      ' + u'\u02cb' + u'-' * 96 + u'\u02ca'
