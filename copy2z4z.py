#!/bin/python3
import argparse
import os

# Parse arguments
argparser = argparse.ArgumentParser(
    description='Copy 2-line song files to 4-line versions')
argparser.add_argument(
    'fsevent',
    help='The fswatcher event line')
args = argparser.parse_args()


# File was removed from 2-Zeilig
def remove(path):
    os.remove(path.replace('/2-Zeilig/', '/4-Zeilig/'))
    print('Removed "' + path + '"')


# File should be reformatted and copied to 4-Zeilig
def copy(path):
    with open(path, 'r', encoding='ISO-8859-1') as song2:
        contents2 = song2.read()
        contents4 = contents2.replace('\n--\n', '\n')
        with open(path.replace('/2-Zeilig/', '/4-Zeilig/'), 'w',
                  encoding='ISO-8859-1', newline='\r\n') as song4:
            song4.write(contents4)
    print('Copied "' + path + '"')


# Parse args
action = args.fsevent.split(' ')[-1]
path = args.fsevent[:-len(action)-1]

# Check if the path points to a .sng file
if not (path.endswith('.sng') and os.path.isfile(path)):
    print('"' + path + '" is not a .sng file. Skipping...')
    exit(1)

# Call according to event
if action == 'Removed':
    remove(path)
elif action in ('Created', 'Updated'):
    copy(path)
else:
    raise NotImplementedError()
