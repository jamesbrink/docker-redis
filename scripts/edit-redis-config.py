#!/usr/bin/env python
# This script reads existing redis configuration into memory
# Updates values based on ENV variables, and writes the configuration
# back out to disk.
from os import getenv,putenv
import re

CONFIG_FILE = '/etc/redis/redis.conf'
# Ugly I know =/
ENV_CONFIG_OPTIONS = (
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


def parse_env_variables():
    config_options = {}
    for env_variable in ENV_CONFIG_OPTIONS:
        env_value = getenv(env_variable.upper())
        if env_value:
            print '%s value: %s' % (env_variable,env_value)
            config_options[env_variable] = env_value
        else:
            print 'could not find ' + env_variable
            config_options[env_variable] = None
    return config_options


def print_header(string):
    print '=' * 80
    print string
    print '=' * 80


def read_config_file(input_file):
    config_file = None
    config_file_contents = []
    try:
        config_file = open(input_file)
        config_file_contents = config_file.readlines()
    except IOError as e:
        print e
    finally:
        if config_file:
            config_file.close()
    return config_file_contents


def write_config_file(output_file,config_file_contents):
    config_file = None
    try:
        config_file = open(output_file,'w')
        for line in config_file_contents:
            config_file.write(line)
    except IOError as e:
        print e
        return False
    finally:
        if config_file:
            config_file.close()
    return True


def update_config(config_file_contents,config_options):
    for index,line in enumerate(config_file_contents):
        if not re.match(r'^#.*$',line):
            regex = r'^([\w-]+)\s+\w+$'
            config_option = re.match(regex,line)
            if config_option:
                config_option = config_option.group(1)
                if config_option in config_options:
                    config_file_contents[index] = '%s %s\n' % (config_option, config_options[config_option])
    return config_file_contents


# It all starts here
print_header('Altering coniguration using the following settings:')
config_options = parse_env_variables()
config_file_contents = read_config_file(CONFIG_FILE)
new_config = update_config(config_file_contents,config_options)
if write_config_file(CONFIG_FILE,new_config):
    print_header('Configuration updated')
else:
    print_header('Something went wrong!')






