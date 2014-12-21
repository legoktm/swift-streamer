#!/usr/bin/env python3

import mutagen
from mutagen.mp3 import MP3


class Song:
    def __init__(self, path):
        self._path = path
        self._noext = '.'.join(path.split('.')[:-1])
        try:
            self._info = MP3(self._path)
        except mutagen.mp3.HeaderNotFoundError as e:
            print(path)
            raise e

    @property
    def title(self):
        return self._info['TIT2'].text[0]

    @property
    def album(self):
        return self._info['TALB'].text[0]

    @property
    def path(self):
        return self._path

    def filename(self, remove_ext=True):
        path = self._path.split('/')[-1]
        if remove_ext:
            path = '.'.join(path.split('.')[:-1])
        return path

    @property
    def track(self):
        return self._info['TRCK'].text[0]

    @property
    def album_mbid(self):
        return self._info['TXXX:MusicBrainz Album Id'].text[0]

if __name__ == '__main__':
    import os
    s = Song(os.path.expanduser('~/Music/Taylor Swift/1989/06 Shake It Off.mp3'))
    print(s.album_mbid)
