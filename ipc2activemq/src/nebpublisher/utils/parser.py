import time, logging
import re
import sys


NOT_IMPLEMENTED=1
BAD_FORMAT=2


logger = logging.getLogger("nebpublisher.parser")

def count_not_none(groups) :
  i = 0
  for element in groups:
    if element != None:
      i = i + 1
  return i


class Parser():
  
  def __init__ (self, topics, parser_functions):
    self.load_types()
    self.topics = topics
    self.parser_functions = parser_functions
    
    # this code was made to compile the regexps only once
  
    # iterate over command names
    for key in self.topics.expressions:
      topic = self.topics.expressions[key]
      #iterate over items in command (labelFilter, eventtype level)
      for item in topic:
          # Append error regexps to each regexps array to catch known errors
          for errorRegexp in topics.errorRegexps:
            item['regexps'].append(errorRegexp)

          #iterate over subitems (properties and regexps)
          for subitem in item['regexps']:
            #substitute text with compiled regexp
            subitem['regexp'] = re.compile(subitem['regexp'])
            
      topics.expressions[key] = topic
     
    logger.debug("Compiled regexps structure: %s " % str(topics.expressions))
      
  """ This function loads the types and the functions responsible for
      parsing each message event
  """  
  def load_types(self):
    self.switch = {
      13: self.parse_service_check
    }

  def parse(self, type, message):
    try:
      return self.switch[type](message)
    except KeyError, e:
      self.not_implemented_type(type)
      return NOT_IMPLEMENTED
    except Exception, e:
      logger.warn('Unknown exception %s' % str(sys.exc_info()))
      exit(1)

  def not_implemented_type(self, type):
    logger.warn("Type %i has no parser." % type)
    return
  
  def not_implemented_service(self, service):
    logger.warn("Service %s has no parser." % service)
    return
 
  def parse_service_check(self, message):
    if message == None:
      return BAD_FORMAT

    logger.debug("Message %s - service check" % message)
    data = []
    data = message.split('^')

    if len(data) < 4:
      return BAD_FORMAT

    host = data[0]
    command_name = data[1]
    status = data[2]
    message = data[3]

    if len(host) == 0 or len(command_name) == 0  or len(status) == 0 or len(message) == 0:
      return BAD_FORMAT

    logger.debug("Host %s - command_name %s - state %s - output %s" %(host, command_name, status, message))

    if command_name in self.topics.expressions:        
      topic = self.topics.expressions[command_name]
      result = self.create_event_from_regexp(host, message, topic)
      if result != BAD_FORMAT:
        return [result]
      return result
      
    elif command_name in self.parser_functions.commands:
      command_parser_functions = self.parser_functions.commands[command_name]
      events = self.create_events_from_parser_functions(host, message, command_parser_functions)
      return events
    
    logger.warn("Event type %s not registered as a topic" %(command_name))
    return BAD_FORMAT
  
  def create_event_from_regexp(self, host, message, topic):
    event = {'host' : host}
    logger.debug('Message to be matched: %s \n Topic: %s' % (message, str(topic)))
    
    match = False
    #iterate over items in command (labelFilter, eventtype level)
    for item in topic:
      if match == True:
        # stop iterating over item
        break  
      if item['labelFilter'] != None and not message.startswith(item['labelFilter']):
        logger.debug("Does not match with label")
      else: 
        #iterate over subitems (properties and regexps)
        for subitem in item['regexps']:
          r = subitem['regexp']
          m = r.match(message)
          if m == None: 
            logger.warn("Regexp does not produce content")
          elif count_not_none(m.groups()) != len(subitem['properties']):
            logger.warn("Regexp has a different number of properties from expected")
          else:
            # if groups in regexp and the number of properties match consider it a match
            match = True
            event['eventtype'] = item['eventtype']
            event['description'] = message

            # if the regex contains an specific event type, override it
            if 'eventtype' in subitem and subitem['eventtype'] != None:
              event['eventtype'] = subitem['eventtype']

            i = 1 # first match is the whole expression
            for property in subitem['properties']:
              if m.group(i) != None:
                event[property] = m.group(i)
                i = i + 1
            # stop iterating over subitem
            break

            
            
      
    logger.debug('event: %s' % str(event))
    if match == True:
      return event
    else:
      logger.warn('No expression for: %s' %(message))
      return BAD_FORMAT
      
  def create_events_from_parser_functions(self, host, message, command_parser_functions):
    for parser_function_struct in command_parser_functions:
      if parser_function_struct['labelFilter'] == None or not message.startswith(parser_function_struct['labelFilter']):
        logger.debug("Does not match with label")
      else:
        events = parser_function_struct['function'](message, parser_function_struct['eventtype'], parser_function_struct['labelFilter'])
        return events
