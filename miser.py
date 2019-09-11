#!/usr/bin/env python3
# todo: make python flask webserver/daemon that accepts POST requests of spotify playlist
# links and sends them back as converted csv to the user
"""Download Spotify playlists from YT"""

import os
import csv
import requests
import time
#import eyed3 as eyed3
import argparse
from argparse import RawTextHelpFormatter
import multiprocessing as mp
import youtube_dl

# Vars in global scope
pool = mp.Pool()

def main():
    """Main"""
    parser = argparse.ArgumentParser(
        description="MelodyMiser -- Download a song/complete Spotify playlist from YouTube",
        formatter_class=RawTextHelpFormatter,
        epilog="Example:\n"
        "miser -l <spotify-playlist-link> "
        "-j 3 -d /home/user/music\n"
        "miser -l 'ESPRIT 空想 - Trip II The OC' -d ."
    )
    parser.add_argument('-l', '--link', required=True,
                        help="Specifies the link to the public Spotify playlist "
                        "that will be downloaded.")
    parser.add_argument('-d', '--directory',
                        help="Specifies the destination save path for created .mp3 files. "
                        "Omit to save in the current directory.")
    parser.add_argument('-j', '--pool', type=int, choices=range(0, mp.cpu_count()), default=1,
                        help="Specifies the number of processor cores to allocate for "
                        "parallel tasks. Defaults to 1 if not specified.")

    args = parser.parse_args()

    # init multiprocessor based on passed CPU cores
    pool = mp.Pool(args.pool)

    if not args.directory:
        args.directory = os.getcwd()
    os.chdir(args.directory)

    songs_list = parse_csv(args.link)

    pool.map(download_song, songs_list)

    #pool.map(construct_metadata, songs_list)

def download_song(song):
    """Download a single song in a playlist"""
    #artist = str(song.split(" -"))
    #song_name = str(song.split("- "))

    opts = {
    'format': 'bestaudio/best',
    'ignoreerrors': True,
    'quiet': False,
    'default_search': 'ytsearch',
    #'outtmpl': '%(title)s.%(ext)s',
    #'outtmpl': artist + " " + song_name + '.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }

    ydl = youtube_dl.YoutubeDL(opts).download(song)

    print("Finished downloading and converting: " + song)

#def get_csv():
    #"""Download converted playlist CSV file"""

def construct_metadata(song):
    """Construct ID3 metadata for a single song"""
    to_tag = eyed3.load("TEST")

    print("Retrieving ID3 metadata for " + song)


    # wait 1 second to avoid MusicBrainz rate-limiting
    time.sleep(1)

def parse_csv(csv_path):
    """Parse downloaded csv file"""
    song_list = []

    try:
        with open(csv_path, encoding='utf-8') as playlist:
            print("Parsing " + csv_path)
            reader = csv.reader(playlist, delimiter=',')
            next(reader) # skip csv header
            for row in reader:
                song_list.append(row[2] + " - " + row[1])
            # todo: parse CSV, then check to see which songs already exist in current dir
            # move non-existent results to new list and return that
    except IndexError as error:
        # consider validating playlists when parsing
        # from API on web server instead
        print(str(error))
    
    return song_list

main()