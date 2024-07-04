import subprocess

import config
from helpers import local_dir

rclone_argv = ['rclone', '--error-on-no-transfer',
               'sync', '--fs-cache-expire-duration', '0', '-u',
               '--include', f'/{config.dir2}**', '--include', f'/{config.dir4}**']


def pull_changes():
    result = subprocess.run(rclone_argv + [config.remote, local_dir], capture_output=True)

    match result.returncode:
        case 1 | 2 | 3 | 4 | 7 | 8 | 10:
            print(f'Rclone failed with return code {result.returncode}')
            print(result.stderr)
            exit(1)
        case _:
            pass


def push_changes():
    print('Uploading changes…')
    result = subprocess.run(rclone_argv + [local_dir, config.remote], capture_output=True)
    match result.returncode:
        case 1 | 2 | 3 | 4 | 7 | 8 | 10:
            print(f'An error occurred while uploading changes [errno {result.returncode}]')
            print(result.stderr)
            exit(1)
        case _:
            print('Changes uploaded successfully.')
