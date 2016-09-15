#!usr/bin/python
import json
import time
import datetime

ATTEMPT_LOG = '/home/ackbar/cowrie/cowrie_extension/attempt_log/attempt_log.txt'
DICTIONARY = '/home/ackbar/cowrie/cowrie_extension/dictionary/dictionary_json'
RESULTS_LOG = '/home/ackbar/cowrie/cowrie_extension/result_log.txt'


# Returns index of source ip, if there is one
def find_index(src_ip, filename=ATTEMPT_LOG):
    with open(filename, 'r') as f:
        lines = f.readlines()
    if lines.index(src_ip + '\n') % 3 == 0:
        return lines.index(src_ip + '\n')


# Loads used passwords of attacker from log
def load_passwords(index, filename=ATTEMPT_LOG):
    with open(filename) as pswds:
        used_passwords = pswds.readlines()[index + 2].split()
        return used_passwords


# Load dictionary from json file
def load_dictionary(filename=DICTIONARY):
    with open(filename) as infile:
        data_to_read = json.load(infile)
        return data_to_read


# Deletes data from log
def delete_log_entry(index, filename=ATTEMPT_LOG):
    with open(filename, 'r') as f:
        lines = f.readlines()
    f = open(filename, 'w')
    delete = 0
    for line in lines:
        if delete < index or delete > index + 2:
            f.write(line)
        delete += 1


# Creates new log
def create_new_entry(src_ip, password_list, filename=ATTEMPT_LOG):
    f = open(filename, 'a')
    f.write(src_ip + '\n' + str(time.time()) + '\n')
    dummy_string = ''
    for word in password_list:
        dummy_string += word + ' '
    f.write(dummy_string + '\n')
    f.close()
    return find_index(src_ip)


# Updates attackers log
def update_log(src_ip, index, password_list, filename=ATTEMPT_LOG):
    delete_log_entry(index, filename)
    create_new_entry(src_ip, password_list, filename)


# If attacker fails once, we flag him as fail so we can skip process of matching dictionary in next attempts
def flag_attacker_as_fail(src_ip, passwords):
    passwords.append('FLAG_NOT')
    update_log(src_ip, find_index(src_ip), passwords)


# When attackers succeeds in access to the machine, we log attackers ip and time this event occurred
# Important to have, this log will be used as source of information for my bachelor thesis
def update_result_log(bookmark, src_ip, filename=RESULTS_LOG):
    with open(filename) as infile:
        lines = infile.readlines()
    dummy_str = ''
    for line in lines:
        if bookmark in line:
            dummy_str += line.strip('\n') + \
                         datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +\
                         ' ' + src_ip + '~\n'
        else:
            dummy_str += line
    f = open(filename, 'w')
    f.write(dummy_str)
    f.close()


# Main function that will determine if attacker succeeds of fails in attempt to log in the machine
def attempt_result(new_attempt_password, src_ip):
    # Load dictionary from json file
    dictionary = load_dictionary()

    # Find attacker in log, if not create new
    # Keep index for further use
    try:
        index = find_index(src_ip)
    except ValueError:
        index = create_new_entry(src_ip, [])

    # Load passwords from attacker log
    passwords = load_passwords(index)

    # If attacker once failed for not matching dictionary, he will be failed automatically in following attempts
    if len(passwords) != 0 and passwords[-1] == 'FLAG_NOT':
        return False

    # Dummy variable that will keep last accessed element in dictionary while iterating
    bookmark = dictionary

    # Iterating to the last password in list-passwords
    for password in passwords:
        if len(passwords) is not 0:
            try:
                bookmark = bookmark[password]
            except KeyError:
                flag_attacker_as_fail(src_ip, passwords)
                return False
            except TypeError:
                flag_attacker_as_fail(src_ip, passwords)
                return False

    # See if:
    # # New password is still in dictionary - in that case continue - still return False
    # # New password is final in dictionary - success attacker is allowed in - return True
    # # If new password throws exception, new password does not match any dictionary - return False
    try:
        bookmark = bookmark[new_attempt_password]
        if isinstance(bookmark, basestring):
            passwords.append(new_attempt_password)
            update_log(src_ip, index, passwords)
            print('Attacker succeeded: delete this message - add message to cowrie_log')
            update_result_log(bookmark, src_ip)
            return True
        else:
            passwords.append(new_attempt_password)
            update_log(src_ip, index, passwords)
            return False
    except KeyError:
        flag_attacker_as_fail(src_ip, passwords)
        return False
    except TypeError:
        flag_attacker_as_fail(src_ip, passwords)
        return False


