#!/usr/bin/env python3

import hashlib
import os

from . import song


class Album:
    def __init__(self, artist, path):
        self.path = path
        self._artist = artist
        self._songs = None

    @property
    def artist(self):
        return self._artist

    @property
    def name(self):
        return self.songs[0].album

    @property
    def hash_(self):
        return hashlib.sha1(self.name.encode()).hexdigest()

    @property
    def songs(self):
        if self._songs is not None:
            return self._songs
        self._songs = []
        files = os.listdir(self.path)
        for file in files:
            # Look for mp3 files, but ignore OSX ._ files.
            if file.endswith(('.mp3', '.flac')) and not file.startswith('.'):
                self._songs.append(song.Song(os.path.join(self.path, file)))
        self._songs.sort(key=lambda song: song.filename())
        return self._songs

    @property
    def cover_art(self):
        art = os.path.join(self.path, 'cover.jpg')
        if os.path.isfile(art):
            return art
        else:
            return None

    @property
    def year(self):
        return self.songs[0].year
