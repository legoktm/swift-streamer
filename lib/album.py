#!/usr/bin/env python3
import musicbrainzngs
import os

from . import song

musicbrainzngs.set_useragent('swift-streamer', '0.1', 'https://github.com/legoktm/swift-streamer')


class Album:
    def __init__(self, artist, path):
        self.path = path
        self._artist = artist
        self._songs = None
        self._mb_info = None

    @property
    def artist(self):
        return self._artist

    @property
    def name(self):
        return self.mb_info['title']

    @property
    def songs(self):
        if self._songs is not None:
            return self._songs
        self._songs = []
        files = os.listdir(self.path)
        for file in files:
            if file.endswith('.mp3'):
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
    def mbid(self):
        songs = self.songs
        if not songs:
            print(self.name)
            quit()
            return None
        return self.songs[0].album_mbid

    @property
    def mb_info(self):
        if self._mb_info is None:
            self._mb_info = musicbrainzngs.get_release_by_id(self.mbid)['release']

        return self._mb_info

    @property
    def year(self):
        return self.mb_info['date'].split('-')[0]
