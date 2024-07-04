import time
from threading import Event

import config
import rclone
import reformatter
from helpers import changed_song_pairs


def parse_pairs():
    result = False

    return result


def main(exit_evt: Event):
    print('Starting automated SongBeamer songs reformatter…')
    last_change = 0.0

    while not exit_evt.is_set():
        changed = False
        rclone.pull_changes()

        # Get songs which have changed recently
        for s2, s4 in changed_song_pairs(last_change):
            # If only one file is there, and it was modified before the last run, its counterpart was deleted
            if s2 is None:
                if s4[1] < last_change:
                    changed |= reformatter.remove(s4[0])
                else:
                    changed |= reformatter.copy(s4[0])
            elif s4 is None:
                if s2[1] < last_change:
                    changed |= reformatter.remove(s2[0])
                else:
                    changed |= reformatter.copy(s2[0])
            else:
                # No deletion (continue did not fire): Update files
                # The newer file gets copied over first, but then copied back anyway.
                # This is to make sure that both files are formatted properly for their location,
                # and allows to put "--" into files in config.dir4 for ease of editing
                if s2[1] < s4[1]:
                    changed |= reformatter.copy(s4[0])
                else:
                    changed |= reformatter.copy(s2[0])

        if changed:
            rclone.push_changes()

        last_change = time.time()
        exit_evt.wait(config.delay)

    print('Terminated.')


if __name__ == '__main__':
    import signal

    # Catch interrupt
    exit_event = Event()


    def signal_handler(sig, frame):
        print('Signal caught! Shutting down…')
        exit_event.set()


    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)

    main(exit_event)
