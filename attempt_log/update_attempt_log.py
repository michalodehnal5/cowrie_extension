#!usr/bin/python
import sys
import time

ATTEMPT_LOG = '/home/ackbar/cowrie/cowrie_extension/attempt_log/attempt_log.txt'
RETURN_TIME = 3600


# Delete logs flagged to deletition
def delete_marked_lines(filename=ATTEMPT_LOG):
    with open(filename, 'r') as f:
        lines = f.readlines()
    fw = open(filename, 'w')
    dummy_str = ''
    for line in lines:
        if 'FLAG_DELETE' not in line:
            dummy_str += line
    fw.write(dummy_str)
    fw.close()


# Flags log to delete
def mark_for_deletition(index, filename=ATTEMPT_LOG):
    with open(filename, 'r') as fr:
        lines = fr.readlines()
    fw = open(filename, 'w')
    dummy_str = ''
    for indexf, line in enumerate(lines):
        if indexf < index or indexf > index + 2:
            dummy_str += line
        else:
            dummy_str += 'FLAG_DELETE '
            dummy_str += line
    fw.write(dummy_str)
    fw.close()


# Main function that will mark logs for deletition
def update():
    f = open(ATTEMPT_LOG).readlines()
    now = time.time()
    for index, line in enumerate(f):
        if (index % 3) == 1 and now - float(line.strip('\n')) >= RETURN_TIME:
            mark_for_deletition(index - 1)
    delete_marked_lines()


update()
