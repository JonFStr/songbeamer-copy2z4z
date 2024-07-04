import os
import re

import config


def from2to4(contents2):
    """
    Reformat content from 2-lines version to 4-lines
    :param contents2: The content to be reformatted
    :return: The reformatted content
    """
    # Make 'small' line break a comment
    return re.sub(r'\n\s*--\s*\n', r'\n##H --\n', contents2)


def from4to2(contents4):
    """
    Reformat content from 4-lines version to 2-lines
    :param contents4: The content to be reformatted
    :return: The reformatted content
    """
    # Remove comment indicator
    return re.sub(r'\n\s*#{1,2}H --\s*\n', r'\n--\n', contents4)


def remove(path: str):
    if os.path.exists(path):
        os.remove(path)
        print(f'Removed "{path}"')
        return True
    else:
        print(f'Did not remove "{path}": File does not exist')
        return False


# File should be reformatted and copied to the other folder
def copy(src: str, abort=False):
    changed = False
    from2 = False
    if config.dir2 in src:
        dst = src.replace(config.dir2, config.dir4)
        from2 = True
    else:
        dst = src.replace(config.dir4, config.dir2)

    with open(src, 'r', encoding='ISO-8859-1') as src_file:
        # Read old file
        src_content = src_file.read()

        # Chose function to reformat based on Path
        dst_content = from2to4(src_content) \
            if from2 \
            else from4to2(src_content)

        skip = False
        # Check if the contents have changed compared with on disk
        # If they haven't, this is probably a loop, break out of it!
        if os.path.exists(dst):
            with open(dst, 'r', encoding='ISO-8859-1') as dst_file:
                previous_content = dst_file.read()
                if previous_content == dst_content:
                    # Log action to stdout
                    print(f'Skipped copying "{src}" to "{dst}" because new content is identical to content on disk')
                    skip = True

        # Write new file
        if not skip:
            with open(dst, 'w', encoding='ISO-8859-1', newline='\r\n') as dst_file:
                # Write new content
                dst_file.write(dst_content)

                # Log action to stdout
                print(f'Copied "{src}" to "{dst}"')
                changed = True

    if not abort:
        changed |= copy(dst, True)
    return changed
