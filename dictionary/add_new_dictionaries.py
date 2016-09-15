#!usr/bin/python
import sys, time, json
from datetime import datetime

DICTIONARY = '/home/ackbar/cowrie/cowrie_extension/dictionarydictionary_json'
RESULTS_LOG = '/home/ackbar/cowrie/cowrie_extension/result_log.txt'
COUNTER = '/home/ackbar/cowrie/cowrie_extension/stupid_counter.txt'
LOGS_TO_PARSE = '/home/ackbar/cowrie/cowrie/log/cowrie.log_parsed'

# Helping class to automate inserting new values to dictionaries, not sure how it works, but it does ^^
class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def get_new_dictionaries(filename=LOGS_TO_PARSE):
    # Load new parsed logs to extract new dictionaries
    f = open(filename, 'r').readlines()

    # Helping dictionary to count attackers attempts {'ip_address': number_of_used_passwords }
    candidates = {}

    # Iterating through lines and counting attempts
    for line in f:
        timestamp, ip, login, password = line.split('~', 4)
        if ip in candidates:
            candidates[ip] += 1
        else:
            candidates[ip] = 1

    # For each record, extract those with 5-10 attempts
    for candidate in candidates:
        if 5 <= candidates[candidate] and candidates[candidate] >= 10:
            extract_candidate(filename, candidate)


def extract_candidate(filename, candidate):
    # Opening parsed file
    f = open(filename, 'r').readlines()

    # List to save all passwords
    dictionary_check = []

    # Saving all passwords of candidate to list
    for line in f:
        timestamp, ip, login, password = line.split('~', 4)
        if ip == candidate:
            dictionary_check.append(password.strip('\n'))

    # Determining if used passwords are matching existing dictionary
    dictionary_exists = check_dictionary_presence(DICTIONARY, dictionary_check)

    # If dictionary is unique, create new record of it
    if not dictionary_exists:
        enter_new_dictionary(dictionary_check, timestamp, candidate)


def check_dictionary_presence(filename, dc):
    # Loading dictionary to variable
    with open(filename) as infile:
        dictionaries = json.load(infile)

    # Iterating through dictionary, if dictionary exists, return True, else False
    current_node = dictionaries
    for password in dc:
        try:
            current_node = current_node[password]
        except KeyError:
            return False
        except TypeError:
            return False
    return True


def append_new_use_of_dictionary(filename, new_name, t, i):
    # Helping function to reduce code repetition
    with open(filename, 'a') as outfile:
        outfile.write(new_name + '~' + t + ' ' + i + '~' + '\n')


def enter_new_dictionary(lop, t, i):
    # Creating new dictionary with vivify ability
    # Loading dictionary from json file
    # Updating created dictionary with data from file
    with open(DICTIONARY) as infile:
        data = AutoVivification()
        dictionary = json.load(infile)
        data.update(dictionary)

    # Loading counter for dictionary name, and updating it with +1
    with open(COUNTER, 'r') as infile:
        counter = int(infile.readline())
    with open(COUNTER, 'w') as outfile:
        outfile.write(str(counter + 1))

    # Setting new name for not existing dictionary
    new_name = 'dictionary-' + str(counter)

    # Inserting new dictionary to tree, ugly way for doing so, did not find a way to do it with one if statement
    if len(lop) == 5:
        data[lop[0]][lop[1]][lop[2]][lop[3]][lop[4]] = new_name
        append_new_use_of_dictionary(RESULTS_LOG, new_name, t, i)
    elif len(lop) == 6:
        data[lop[0]][lop[1]][lop[2]][lop[3]][lop[4]][lop[5]] = new_name
        append_new_use_of_dictionary(RESULTS_LOG, new_name, t, i)
    elif len(lop) == 7:
        data[lop[0]][lop[1]][lop[2]][lop[3]][lop[4]][lop[5]][lop[6]] = new_name
        append_new_use_of_dictionary(RESULTS_LOG, new_name, t, i)
    elif len(lop) == 8:
        data[lop[0]][lop[1]][lop[2]][lop[3]][lop[4]][lop[5]][lop[6]][lop[7]] = new_name
        append_new_use_of_dictionary(RESULTS_LOG, new_name, t, i)
    elif len(lop) == 9:
        data[lop[0]][lop[1]][lop[2]][lop[3]][lop[4]][lop[5]][lop[6]][lop[7]][lop[8]] = new_name
        append_new_use_of_dictionary(RESULTS_LOG, new_name, t, i)
    else:  # len(lop) == 10:
        data[lop[0]][lop[1]][lop[2]][lop[3]][lop[4]][lop[5]][lop[6]][lop[7]][lop[8]][lop[9]] = new_name
        append_new_use_of_dictionary(RESULTS_LOG, new_name, t, i)

    # Dumping new data to file, for further use
    with open(DICTIONARY', 'w') as outfile:
        json.dump(data, outfile)


get_new_dictionaries()
