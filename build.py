#!/usr/bin/env python3
"""
swift-streamer is a static HTML and JavaScript-based music player
Copyright (C) 2014, 2017 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import os
import queue
import shutil

import config
from lib.album import Album
from lib.mover import Mover
from lib.worker import WorkerThread

config.MUSIC = os.path.expanduser(config.MUSIC)

print('Hello, welcome to swift-streamer.')


def process_artist(artist, path):
    album_names = os.listdir(path)
    albums = []
    for album in album_names:
        if not album.startswith('.'):
            albums.append(Album(artist, os.path.join(path, album)))

    return albums


def get_all_albums():
    albums = []
    artists = []
    for artist in os.listdir(config.MUSIC):
        if config.MATCH_ARTIST_PREFIX is None or artist.startswith(config.MATCH_ARTIST_PREFIX):
            artists.append(artist)
    print('Processing: %s' % ', '.join(artists))
    for artist in artists:
        path = os.path.join(config.MUSIC, artist)
        if os.path.isdir(path):
            albums.extend(process_artist(artist, path))
    return albums


html = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>swift-player</title>
        <link rel="stylesheet" href="resources/styles.css" />
        <script src="resources/jquery-2.1.1.min.js"></script>
        <script src="resources/playlist.js"></script>
    </head>
    <body>
        <div id="queue-wrapper">
            <audio id="player" controls preload="none"></audio>
            <img id="cover"/>
            <ol id="queue">
            </ol>
        </div>
        <div id="config">%s</div>
""" % json.dumps({
    'ogg': config.GENERATE_OGGS,
})

album_header = """
<h1>{album} ({year})</h1>
    <small class="play-album">Play album</small>
    <ol>
"""

album_closer = """
    </ol>
"""

song_template = """
        <li><a class="add-queue" data-src="{src}" data-album="{album}" data-hash="{hash_}" href="">{name}</a></li>
"""

all_albums = get_all_albums()
all_albums.sort(key=lambda album: album.year)

for album in all_albums:
    html += album_header.format(album=album.name, year=album.year)
    for song in album.songs:
        html += song_template.format(
            name=song.title,
            src='audio/' + song.filename(),
            album=album.name,
            hash_=album.hash_
        )
    html += album_closer

html += """
    </body>
</html>
"""


def ensure_directory(path, hide_listings=False):
    if not os.path.exists(path):
        os.mkdir(path)
    if hide_listings:
        with open(os.path.join(path, 'index.html'), 'w') as f:
            f.write('Go away.')


ensure_directory(config.OUTPUT)
with open(config.OUTPUT + '/index.html', 'w') as f:
    f.write(html)
    print('Wrote to %s/index.html' % config.OUTPUT)

OUTPUT_AUDIO = config.OUTPUT + '/audio'
ensure_directory(OUTPUT_AUDIO, hide_listings=True)
ogg_queue = queue.Queue()
for i in range(0, 10):
    t = WorkerThread(ogg_queue)
    t.setDaemon(True)
    t.start()
for album in all_albums:
    for song in album.songs:
        if not os.path.isfile(os.path.join(OUTPUT_AUDIO, song.filename(remove_ext=False))):
            print('Copying %s...' % song.filename(remove_ext=False))
            shutil.copy(song.path, OUTPUT_AUDIO)
        if config.GENERATE_OGGS:
            ogg = song.filename() + '.ogg'
            if not os.path.isfile(os.path.join(OUTPUT_AUDIO, ogg)):
                info = {
                    'command': ['ffmpeg', '-i', song.path, '-acodec', 'libopus', ogg, '-v', 'error'],
                    'callback': Mover(ogg, OUTPUT_AUDIO).move,
                }
                ogg_queue.put(info)
ogg_queue.join()
print('Copied audio')

OUTPUT_COVERS = config.OUTPUT + '/covers'
ensure_directory(OUTPUT_COVERS, hide_listings=True)
for album in all_albums:
    path = os.path.join(OUTPUT_COVERS, album.hash_ + '.jpg')
    if album.cover_art:
        shutil.copy(album.cover_art, path)
print('Copied cover art')

OUTPUT_RESOURCES = config.OUTPUT + '/resources'
if os.path.exists(OUTPUT_RESOURCES):
    shutil.rmtree(OUTPUT_RESOURCES)
shutil.copytree('resources', OUTPUT_RESOURCES)
ensure_directory(OUTPUT_RESOURCES, hide_listings=True)
print('Copied resources')
