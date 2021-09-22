#!/bin/python3
# This script collects lines from fswatcher and removes duplicates
# AS LONG AS a python instance is running.
# With deduplicated lines, it launches the copy script
# Therefore, multiple edits of the same file are ignored,
# if they happen within a short period of time.
from argparse import ArgumentParser
from sys import stdin
from select import select
from os import system
from time import sleep

# Parse arguments
argparser = ArgumentParser(
    description='Copy 2-line song files to 4-line versions')
argparser.add_argument(
    '-l', '--latency', required=True, type=int,
    help="""Latency to wait for after copying one file.
    To avoid infinite loops, it should be the same as --dir-cache-time of rclone"""
)
args = argparser.parse_args()

queue = []
readBuffer = ''

print('Eventhandler launched.')
while True:
    # If something can be read from stdin, read it
    while stdin in select([stdin], [], [], 0)[0]:
        line = stdin.readline()
        # If the line is not empty and not already in the queue, append it
        if line and line not in queue:
            queue.append(line)
        elif not line:
            # Line was empty even though we could have read something
            # -> Stdin was closed
            print('EOF')
            exit(0)

    # After that, if there is an entry in the queue, launch the script with it
    if len(queue) != 0:
        system('python3 copy2z4z.py "' + queue.pop(0) + '"')
    # And now we wait a short amount of time to not overload the system
    sleep(args.latency + 1)
