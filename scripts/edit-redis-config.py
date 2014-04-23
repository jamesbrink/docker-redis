#!/usr/bin/env python
from os import getenv,putenv

# Ugly I know =/
CONFIGURATION_OPTIONS = (
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
print 'Altering coniguration using the following settings:\n'

for env_variable in CONFIGURATION_OPTIONS:
    env_value = getenv(env_variable.upper())
    if env_value:
        print '%s value: %s' % (env_variable,env_value)
    else:
        print 'could not find ' + env_variable




