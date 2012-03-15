
expressions = {
        'check_disk_NT': [
            {'labelFilter': None,
             'eventtype': 'Disk',
             'regexps': [
                {'properties': ['state', 'partition', 'free_percent'],
                 'regexp': r'DISK (OK|WARNING|CRITICAL) - (.*) - Total: .* - Free: .* \((\d+)%\) - Used: .*'
                },
             ], 
            },
        ],

        'check_mem': [
            {'labelFilter': None,
             'eventtype': 'Memory',
             'regexps': [
                {'properties': ['state', 'free_percent'],
                 'regexp': r'Memory (OK|WARNING|CRITICAL) - ([0-9.]+)% .*'
                },
             ],
            },
        ],
        
        'check_ram': [
            {'labelFilter': None,
             'eventtype': 'Memory',
             'regexps': [
                {'properties': ['state', 'free_total'],
                 'regexp': r'RAM (OK|WARNING|CRITICAL) - Physical memory is.* \((\d+) MB\)'
                },
             ],
            },
        ],
        
        'check_swap': [
            {'labelFilter': None,
             'eventtype': 'Swap',
             'regexps': [
                {'properties': ['state', 'free_percent'],
                 'regexp': r'SWAP (OK|WARNING|CRITICAL) - ([0-9]+)% free.*'
                },
                {'properties': ['state', 'used_percent'],
                 'regexp': r'(OK|WARNING|CRITICAL): Swap used: ([0-9]+)% .*'
                },
             ],
            },
        ],


    'check_http': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'<A HREF="(.+)" target="_blank">HTTP (OK|WARNING|CRITICAL): HTTP/(\d+.\d+) (\d\d\d) (.+) - (\d+) bytes in (\d+.\d+) second response time </A>'
            },
            {'properties': ['state', 'version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): HTTP/(\d+.\d+) (\d\d\d) (.+) - (\d+) bytes in (\d+.\d+) second response time'
            }            
         ]
        }
    ],

    'check_ftp': [
        {'labelFilter': None,
         'eventtype': 'FTP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r"FTP (OK|WARNING|CRITICAL) - (\d+.\d+) seconds? response time on port (\d+)"
            }
         ]
        }
    ],


    'check_tcp': [
        {'labelFilter': None,
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - (\d+.\d+) seconds? response time on port (\d+)"
            },
            {'properties': ['state'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - Invalid"
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state'],
             'regexp': r"(WARNING|CRITICAL) - Socket timeout"
            }
         ]
        }
    ],
    
    
    'host' : [
        {'labelFilter': None,
         'eventtype' : 'Ping',
         'regexps': [
            {'properties': ['state', 'ip', 'loss', 'rta'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=(\d+)%(?:(?:, rta=(\d+\.\d*) ms\))|())"
            },
            {'properties': ['state', 'loss', 'rta'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([0-9.]+)%, RTA = ([0-9.]+) ms"
            }
         ],
        }
    ],



    'check_load': [
        {'labelFilter': None,
         'eventtype': 'Load',
         'regexps': [
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)"
            }
         ]
        }
    ],

    'check_cpu': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'user', 'nice', 'sys', 'iowait', 'idle' ],
             'regexp': r"(OK|WARNING|CRITICAL) - user: (\d+.\d+)?, nice: (\d+.\d+)?, sys: (\d+.\d+)?, iowait: (\d+.\d+)?, .+ idle: (\d+.\d+)?"
            }
         ]
        }
    ],

    'check_cputime': [
        {'labelFilter': None,
         'eventtype': 'CPUSimple',
         'regexps': [
            {'properties': ['state', 'usage'],
             'regexp': r"CPU (OK|WARNING|CRITICAL) - Processor Time= (\d+(?:.\d+)?) %"
            }
         ],
        },
    ],
    
    
    'check_dns': [
        {'labelFilter': None,
         'eventtype': 'DNS',
         'regexps': [
            {'properties': ['state', 'response_time', 'domain', 'ip'],
             'regexp': r"DNS (OK|WARNING|CRITICAL): (\d+.\d+) seconds? response time. (.+) returns (.+)"
            }
         ],
        },
    ],
    

    'check_cpu_snmp': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            }
         ]
        }
    ],


    'check_fping': [ 
        {'labelFilter': None,
         'eventtype': 'Ping',
         'regexps': [
            {'properties': ['state', 'ip', 'loss', 'rta'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=(\d+)%(?:(?:, rta=(\d+\.\d*) ms\))|())"
            }
         ]
        }
    ],

    'check_ping': [
        {'labelFilter': None,
         'eventtype': 'Ping',
         'regexps': [
            {'properties': ['state', 'loss', 'rta'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([0-9.]+)%, RTA = ([0-9.]+) ms"
            }
         ]
        }
    ],

    
    'check_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'args'],
             'regexp': r'(OK|WARNING|CRITICAL) - ([0-9]+) processes running with args (.+)'
            }
         ]

        }
    ],

    'check_local_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'state_of_process'],
             'regexp': r'PROCS (OK|WARNING|CRITICAL): ([0-9]+) processes with STATE = (.+)'
            }
         ]
        }
    ],

    'check_many_procs': [
        {'labelFilter': None,
         'eventtype': 'ProcsNotRunning',
         'regexps': [
            {'properties': ['process_not_running'],
             'regexp': r'([^\(]+)'
            }
         ]
        }
    ],
    
    'http_args_follow': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'http_version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+): HTTP/([0-9.]+) ([0-9]+) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time </A>'
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+) - (.+)'
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">(Connection refused)'
            }
         ]
        },
    ],

    'check_disk': [
        {'labelFilter': None,
         'eventtype': 'Disk',
         'regexps': [
            {'properties': ['state', 'free_space' , 'usage'],
             'regexp': r'DISK (OK|WARNING|CRITICAL)()()'
            }
         ]
        }
    ],

    'check_drbd': [
        {'labelFilter': 'DRBD',
         'eventtype': 'DRBD',
         'regexps': [
            {'properties': ['status', 'order', 'connected', 'updated'],
             'regexp': r'DRBD ([^:]+): Device 0 ([^ ]+) ([^ ]+) ([^ ]+)'
            }
         ]
        }
    ],

    'check_heartbeat': [
        {'labelFilter': None,
         'eventtype': 'Heartbeat',
         'regexps': [
            {'properties': ['status', 'mode'],
             'regexp': r'Heartbeat (OK|WARNING|CRITICAL) - Modo (.+)'
            }
         ]
        }
    ],

    'check_mysql': [
        {'labelFilter': None,
         'eventtype': 'MySQL',
         'regexps': [
            {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'average_queries_per_second'],
             'regexp': r'Uptime: ([0-9]+)  Threads: ([0-9]+)  Questions: ([0-9]+)  Slow queries: ([0-9]+)  Opens: ([0-9]+)  Flush tables: ([0-9]+)  Open tables: ([0-9]+)  Queries per second avg: ([0-9.]+)'
            }
         ]
        }
	],

    'check_mysql_nrpe': [
        {'labelFilter': None,
         'eventtype': 'MySQL',
         'regexps': [
            {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'average_queries_per_second'],
             'regexp': r'Uptime: ([0-9]+)  Threads: ([0-9]+)  Questions: ([0-9]+)  Slow queries: ([0-9]+)  Opens: ([0-9]+)  Flush tables: ([0-9]+)  Open tables: ([0-9]+)  Queries per second avg: ([0-9.]+)'
            }
         ]
        }
	],

    'check_dns_stats': [
        {'labelFilter': None,
         'eventtype': 'DNSStats',
         'regexps': [
            {'properties': ['state', 'success', 'referral', 'nxrrset', 'nxdomain', 'recursion', 'failure', 'duplicate', 'dropped','soa','a','ns','cname','ptr','mx','txt','aaaa'],
             'regexp': r'(OK|WARNING|CRITICAL): success: ([0-9]+), referral: ([0-9]+), nxrrset: ([0-9]+), nxdomain: ([0-9]+), recursion: ([0-9]+), failure: ([0-9]+), duplicate: ([0-9]+), dropped: ([0-9]+), soa: ([0-9]+), a: ([0-9]+), ns: ([0-9]+), cname: ([0-9]+), ptr: ([0-9]+), mx: ([0-9]+), txt: ([0-9]+), aaaa: ([0-9]+)'
            }
         ]
        }
	],

    'check_rrdtraf': [
        {'labelFilter': None,
         'eventtype': 'Traffic',
         'regexps': [
            {'properties': ['interface', 'state', 'in', 'out'],
             'regexp': r'(.+) - (OK|WARNING|CRITICAL) - Current BW in: ([0-9.]+).bps Out: ([0-9.]+).bps'
            }
         ]
        }
    ],

    'check_sessao_vip': [
        {'labelFilter': None,
         'eventtype': 'VIP',
         'regexps': [
            {'properties': ['state', 'site', 'sessions'],
             'regexp': r'(OK|WARNING|CRITICAL): (.+) - (\d+) sessoes abertas'
            }
         ]
        }
    ],

    'check_sessao_vip_temp': [
        {'labelFilter': None,
         'eventtype': 'VIP',
         'regexps': [
            {'properties': ['state', 'site', 'sessions'],
             'regexp': r'(OK|WARNING|CRITICAL): (.+) - (\d+) sessoes abertas'
            }
         ]
        }
    ],

    'check_snmp_streamsess': [
        {'labelFilter': None,
         'eventtype': 'SNMPServerSessions',
         'regexps': [
            {'properties': ['state', 'total'],
             'regexp': r'SNMP (OK|WARNING|CRITICAL) - (.+)'
            }
         ]
        }
    ],

    'check_varnish_client': [
                {'labelFilter': None,
                 'eventtype': 'VarnishClient',
                 'regexps': [
                    {'properties': ['connections', 'connections_per_second',
                                    'dropped', 'dropped_per_second', 'requests',
                                    'requests_per_second'],
                     'regexp': r'Client - Connections: ([0-9]+) \(([0-9.]+)\), Drop: ([0-9]+) \(([0-9.]+)\), Requests: ([0-9]+) \(([0-9.]+)\)',
                    },
                 ],
                },
            ],

            'check_varnish_cache': [
                {'labelFilter': None,
                 'eventtype': 'VarnishCache',
                 'regexps': [
                    {'properties': ['hits', 'hits_per_second', 'hitpasses',
                                    'hitpasses_per_second', 'misses',
                                    'misses_per_second'],
                     'regexp': r'Cache Utilization - hit: ([0-9]+) \(([0-9.]+)\), hitpass: ([0-9]+) \(([0-9.]+)\), miss: ([0-9]+) \(([0-9.]+)\)',
                    },
                 ],
                },
            ],

            'check_varnish_backend': [
                {'labelFilter': None,
                 'eventtype': 'VarnishBackend',
                 'regexps': [
                    {'properties': ['conn', 'conn_per_second', 'unhealthy',
                                    'unhealthy_per_second', 'busy',
                                    'busy_per_second', 'fail', 'fail_per_second',
                                    'reuse', 'reuse_per_second', 'toolate',
                                    'toolate_per_second', 'recycle',
                                    'recycle_per_second', 'unused',
                                    'unused_per_second'],
                     'regexp': r'Backend Usage - Conn: ([0-9]+) \(([0-9.]+)\), Unhealthy: ([0-9]+) \(([0-9.]+)\), Busy: ([0-9]+) \(([0-9.]+)\), Fail: ([0-9]+) \(([0-9.]+)\), Reuse: ([0-9]+) \(([0-9.]+)\), TooLate: ([0-9]+) \(([0-9.]+)\), Recycle: ([0-9]+) \(([0-9.]+)\), UnUsed: ([0-9]+) \(([0-9.]+)\)',
                    },
                 ],
                },
            ],

    'check_home': [
        {'labelFilter': None,
         'eventtype': 'HTTPStats',
         'regexps': [
            {'properties': ['state','ttfb', 'ttime', 'check'],
             'regexp': r'(OK|WARNING|CRITICAL): ttfb: ([0-9.]+) - ttime: ([0-9.]+) - check: ([0-9.]+)',
			},
		],
		},
	],

    ### STOPPED HERE ###
    '''

    'check_propel_pwas450': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_ldap_time54': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'http_regexp': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_fila_ldap': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_replica_ibest2': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_nrpe': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_local_users': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'https': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_local_disk': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_process_nossl': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_raid': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'https_args': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_ldap_time22': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_ft_status': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_disk_nossl': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_service_nossl': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_propel_7798': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_cputime_nossl': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_arp_snmp': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_cpu_snmp': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_snmp': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'http_args': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_rrdtraf': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_cns': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_nrpe_ssl': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_load_melig': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],

    'check_mysql_melig': [
        {'labelFilter': None,
         'eventtype': '',
         'regexps': [
            {'properties': [],
             'regexp': r''
            }
         ]
        }
    ],
    ''': []
}


#add common error expressions
errorRegexps = [
    {'properties' : ['description'],
     'regexp' : r"(\(Service Check Timed Out\))"
    },
    {'properties' : ['description'],
     'regexp' : r"(\(Host Check Timed Out\))"
    },
    {'properties' : ['description'],
     'regexp' : r"(CHECK_NRPE)"
    },
    {'properties' : ['description'],
     'regexp' : r"(NRPE: Unable to read output)"
    },
    {'properties' : ['description'],
     'regexp' : r"(Connection refused)"
    },            
    {'properties' : ['description'],
     'regexp' : r"(Connection refused by host)"
    },
    {'properties' : ['description'],
     'regexp' : r'(CRITICAL - Socket timeout after .+ seconds)'
    }
]


      
expressions['tcp'] = expressions['check_tcp']
expressions['check_local_load'] = expressions['check_load']
expressions['http_args'] = expressions['http_args_follow']
expressions['https'] = expressions['http_args_follow']
expressions['https_args'] = expressions['http_args_follow']
expressions['http_regexp'] = expressions['http_args_follow']
expressions['check_local_disk'] = expressions['check_disk']



