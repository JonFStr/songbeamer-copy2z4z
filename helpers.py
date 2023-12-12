import os
from typing import Optional

import config

Song = tuple[str, float]
SongPair = tuple[Optional[Song], Optional[Song]]

local_dir = "songs/"


def localpath(path: str):
    return os.path.join(local_dir, path)


def get_songs(start_path):
    songs: list[Song] = []
    for entry in os.scandir(start_path):
        if entry.is_dir():
            songs += get_songs(entry.path)  # Recurse subdir
        elif not entry.name.endswith('.sng'):
            pass  # Not a song-file
        else:
            songs.append((entry.path, entry.stat().st_ctime))  # Tuple of path and change time
    return songs


def changed_song_pairs(last_change: float):
    # Get songs sorted by path
    def basename(song: Song) -> str:
        return os.path.basename(song[0])

    def filter_predicate(pair: SongPair):
        if pair[0] is None or pair[1] is None:
            return True
        else:
            pair: tuple[Song, Song]  # Redefine type after None-check for linter
            return pair[0][1] > last_change or pair[1][1] > last_change

    songs2 = sorted(get_songs(localpath(config.dir2)), key=basename)
    songs4 = sorted(get_songs(localpath(config.dir4)), key=basename)

    pairs: list[tuple[Optional[Song], Optional[Song]]] = []
    # Iterate over all elements in songs2 and songs4
    idx2 = 0
    idx4 = 0
    while idx2 < len(songs2) or idx4 < len(songs4):
        s2 = songs2[idx2]
        s4 = songs4[idx4]

        # Append matching songs and increment index on append
        if basename(s2) == basename(s4):
            # Paths match, just append the pair
            pairs.append((s2, s4))
            idx2 += 1
            idx4 += 1
        elif basename(s2) < basename(s4):
            # Song2 is in sorting order before Song4, therefore Song2 has a missing counterpart
            pairs.append((s2, None))
            idx2 += 1
        elif basename(s2) > basename(s4):
            # The other way around
            pairs.append((None, s4))
            idx4 += 1

    return filter(filter_predicate, pairs)
