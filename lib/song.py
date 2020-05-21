#!/usr/bin/env python3

import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3


class Song:
    def __init__(self, path):
        self._path = path
        self._noext = '.'.join(path.split('.')[:-1])
        if self._path.endswith('.mp3'):
            try:
                self._info = MP3(self._path)
            except mutagen.mp3.HeaderNotFoundError as e:
                print(path)
                raise e
        elif self._path.endswith('.flac'):
            self._info = FLAC(self._path)
        else:
            raise ValueError(f"Unknown file type: {self._path}")

    @property
    def title(self):
        if 'TITLE' in self._info:
            return str(self._info['TITLE'][0])
        if 'TIT2' not in self._info:
            print(self._info.pprint())
        return self._info['TIT2'].text[0]

    @property
    def album(self):
        if 'ALBUM' in self._info:
            return str(self._info['ALBUM'][0])
        if 'TALB' not in self._info:
            print(self._info.pprint())
        return self._info['TALB'].text[0]

    @property
    def year(self) -> str:
        try:
            return str(self._info['YEAR'][0])
        except KeyError:
            try:
                return str(self._info['TDOR'][0])
            except KeyError:
                return str(self._info['DATE'][0])

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
