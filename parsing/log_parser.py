#!usr/bin/python
import re, sys

LOG_TO_PARSE = '/home/ackbar/cowrie/cowrie/log/cowrie.log'
SAVE_DESTINATION = '/home/ackbar/cowrie/cowrie_extension/parsing/'

def parse(file_name):
    file_to_read = open(file_name, 'r')
    lines = file_to_read.readlines()
    file_to_read.close()
    file_to_write_name = SAVE_DESTINATION + 'cowrie_log_parsed'
    file_to_write = open(file_to_write_name, 'w')
    parse_lines_needed = 'login attempt'
    for line in lines:
        if parse_lines_needed in line:
            time, the_rest = line.split('+', 1)
            ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
            root_pass = re.findall(r'\[\S+/[\S*\s*]*\]', line)
            victim, password = str(root_pass).split('/', 1)

            file_to_write.write(time + '~')
            file_to_write.write(str(ip).strip('\'\]\['))
            file_to_write.write('~')
            file_to_write.write(str(victim).strip('\'\]\[\"'))
            file_to_write.write('~')
            file_to_write.write(str(password).strip('\'\]\[\"'))
            file_to_write.write('\n')

    file_to_write.close()

parse(LOG_TO_PARSE)


