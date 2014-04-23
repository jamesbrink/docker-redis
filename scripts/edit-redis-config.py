#!/usr/bin/env python
from os import getenv,putenv

# Ugly I know =/
configuration_options = (
            'timeout',
            'loglevel',
            'databases',
            'rdbcompression',
            'dbfilename',
            'appendonly',
            'appendfsync',
            'no-append-fsync-on-rewrite',
            'vm-enabled',
            'vm-max-memory',
            'vm-page-size',
            'vm-pages',
            'vm-max-threads',
            'hash-max-zipmap-entries',
            'hash-max-zipmap-value',
            'list-max-zipmap-entries',
            'list-max-zipmap-value',
            'set-max-intset-entries',
            'activerehashing'
        )

for env_variable in configuration_options:
    if getenv(env_variable.upper()):
        env_value = getenv(env_variable.upper())
        print '%s value: %s' % (env_variable,env_value)
    else:
        print 'could not find ' + env_variable




