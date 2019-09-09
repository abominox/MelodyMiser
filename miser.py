#!/usr/bin/env python3
# todo: make python flask webserver/daemon that accepts POST requests of spotify playlist
# links and sends them back as converted csv to the user
"""Download Spotify playlists from YT"""

import os
import csv
import argparse
from argparse import RawTextHelpFormatter
import multiprocessing as mp
import youtube_dl

opts = {
    'format': 'bestaudio/best',
    'ignoreerrors': True,
    'default_search': 'ytsearch',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Vars in global scope
ydl = youtube_dl.YoutubeDL(opts)
pool = mp.Pool()

def main():
    """Main"""
    parser = argparse.ArgumentParser(
        description="MelodyMiser -- Download a complete Spotify playlist from YouTube",
        formatter_class=RawTextHelpFormatter,
        epilog="Examples:\n"
        "test1"
        "test2"
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

def download_song(song):
    """Download a single song in a playlist"""
    ydl.download([song])
    print("Finished downloading and converting: " + song)

#def get_csv():
    #"""Download converted playlist CSV file"""

def construct_metadata(song):
    """Construct ID3 metadata for a single song"""
    print(song) #temp

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