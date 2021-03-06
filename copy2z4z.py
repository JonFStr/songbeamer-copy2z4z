#!/bin/python3
import argparse
import os
import re

# Parse arguments
argparser = argparse.ArgumentParser(
    description='Copy 2-line song files to 4-line versions')
argparser.add_argument(
    'fsevent',
    help='The fswatcher event line')
args = argparser.parse_args()


# Reformatting
def reformat2to4(contents2):
    # Make 'small' line break a comment
    contents4 = re.sub(r'\n\s*--\s*\n', r'\n##H --\n', contents2)
    return contents4


def reformat4to2(contents4):
    # Remove comment indicator
    contents2 = re.sub(r'\n\s*#{1,2}H --\s*\n', r'\n--\n', contents4)
    return contents2


# ====== Functions for Action handling
# File was removed from 2-Zeilig
def remove(pathOld):
    pathNew = pathOld.replace('/2-Zeilig/', '/4-Zeilig/') \
            if '/2-Zeilig/' in pathOld \
               else pathOld.replace('/4-Zeilig/', '/2-Zeilig/')
    if os.path.exists(pathNew):
        os.remove(pathNew)
        print('Removed "' + pathNew + '"')
    else:
        print('Did not remove "' + pathNew + '": File does not exist')


# File should be reformatted and copied to the other folder
def copy(pathOld):
    with open(pathOld, 'r', encoding='ISO-8859-1') as songOld:
        # Read old file
        contentsOld = songOld.read()

        # Chose function to reformat based on Path
        contentsNew = reformat2to4(contentsOld) \
            if '/2-Zeilig/' in pathOld \
               else reformat4to2(contentsOld)

        # Determine new path
        pathNew = pathOld.replace('/2-Zeilig/', '/4-Zeilig/') \
            if '/2-Zeilig/' in pathOld \
               else pathOld.replace('/4-Zeilig/', '/2-Zeilig/')

        # Check if the contents have changed compared with on disk
        # If they haven't, this is probably a loop, break out of it!
        if os.path.exists(pathNew):
            with open(pathNew, 'r', encoding='ISO-8859-1') as songNew:
                contentsDisk = songNew.read()
                if contentsDisk == contentsNew:
                    # Log action to stdout
                    print('Skipped copying "' + pathOld + '" to "' + pathNew +
                        '" because new content is identical to content on disk')
                    return

        # Write new file
        with open(pathNew, 'w',
                  encoding='ISO-8859-1', newline='\r\n') as songNew:
            # Write new content
            songNew.write(contentsNew)

            # Log action to stdout
            print('Copied "' + pathOld + '" to "' + pathNew + '"')


# Parse args
action = args.fsevent.split(' ')[-1]
path = args.fsevent[:-len(action)-1]

# Check if the path points to a .sng file
if not path.endswith('.sng'):
    print('"' + path + '" is not a .sng file. Skipping...')
    exit(1)

# Check if song was removed from folder (is no longer there)
if os.path.isfile(path):
    copy(path)
# Then if the file doesn't exist (anymore), remove the 2nd version
elif not os.path.exists(path):
    remove(path)
else:
    raise NotImplementedError()
