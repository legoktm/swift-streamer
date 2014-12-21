#!/usr/bin/env python3

import os
import shutil
from subprocess import check_output

import config
from lib.album import Album


config.MUSIC = os.path.expanduser(config.MUSIC)


def process_artist(artist, path):
    album_names = os.listdir(path)
    albums = []
    for album in album_names:
        albums.append(Album(artist, os.path.join(path, album)))

    return albums


def get_all_albums():
    albums = []
    artists = os.listdir(config.MUSIC)
    print(artists)
    for artist in artists:
        albums.extend(process_artist(artist, os.path.join(config.MUSIC, artist)))
    return albums

html = """
<html>
    <head>
        <title>swift-player</title>
        <script src="js/jquery-2.1.1.min.js"></script>
        <script src="js/playlist.js"></script>
    </head>
    <body>
        <h1>Queue</h1>
            <audio id="player" controls preload="none"></audio>
            <img id="cover" style="float:right;"/>
            <ol id="queue">
            </ol>
"""

album_header = """
<h1>{album} ({year})</h1>
    <ol>
"""

album_closer = """
    </ol>
"""

song_template = """
        <li><a class="add-queue" data-src="{src}" data-album="{album}" href="">{name}</a></li>
"""

all_albums = get_all_albums()
all_albums.sort(key=lambda album: album.year)

for album in all_albums:
    html += album_header.format(album=album.name, year=album.year)
    for song in album.songs:
        html += song_template.format(name=song.title, src='audio/' + song.filename(), album=album.name)
    html += album_closer

html += """
    </body>
</html>
"""


def ensure_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

ensure_directory(config.OUTPUT)
with open(config.OUTPUT + '/index.html', 'w') as f:
    f.write(html)
    print('Wrote to %s/index.html' % config.OUTPUT)

OUTPUT_AUDIO = config.OUTPUT + '/audio'
ensure_directory(OUTPUT_AUDIO)
for album in all_albums:
    for song in album.songs:
        if not os.path.isfile(song.filename(remove_ext=False)):
            shutil.copy(song.path, OUTPUT_AUDIO)
        ogg = song.filename() + '.ogg'
        if not os.path.isfile(os.path.join(OUTPUT_AUDIO, ogg)):
            check_output(['ffmpeg', '-i', song.path, '-c:a', 'libvorbis', '-q:a', '4', ogg])
            shutil.move(ogg, OUTPUT_AUDIO)
print('Copied audio')

OUTPUT_COVERS = config.OUTPUT + '/covers'
ensure_directory(OUTPUT_COVERS)
for album in all_albums:
    path = os.path.join(OUTPUT_COVERS, album.name + '.jpg')
    if album.cover_art:
        shutil.copy(album.cover_art, path)
print('Copied cover art')

OUTPUT_JS = config.OUTPUT + '/js'
if os.path.exists(OUTPUT_JS):
    shutil.rmtree(OUTPUT_JS)
shutil.copytree('js', OUTPUT_JS)
print('Copied js')
