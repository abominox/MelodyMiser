#!/usr/bin/env python3
# todo: make python flask webserver/daemon that accepts POST requests of spotify playlist
# links and sends them back as converted csv to the user
"""Download Spotify playlists from YT"""

import os
import csv
import argparse
from argparse import RawTextHelpFormatter
import youtube_dl

def main():
    """Main"""
    parser = argparse.ArgumentParser(
        description="Download a complete Spotify playlist from YouTube",
        formatter_class=RawTextHelpFormatter,
        epilog="Examples:\n"
        "test1"
        "test2"
    )
    parser.add_argument('-s', '--source', required=True,
                        help="Specifies the source file containing the playlist (.csv)")
    parser.add_argument('-d', '--directory',
                        help="Specifies the destination save path for created .mp3 files. "
                        "Omit to save in the current directory.")
    parser.add_argument('-j', '--pool',
                        help="Specifies the number of processor cores to allocate for "
                        "download tasks. Defaults to 1 if not specified.")

    args = parser.parse_args()

    if not args.directory:
        args.directory = os.getcwd()

    os.chdir(args.directory)
    opts = {
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    download_song(youtube_dl.YoutubeDL(opts))

def download_song(ydl):
    """Download a single song"""
    ydl.download(['https://www.youtube.com/watch?v=f4fVdf4pNEc'])

#def convert_csv():
    #"""Download converted playlist CSV file"""

def construct_metadata(song):
    """Construct ID3 metadata for a single song"""
    print(song) #temp

def parse_csv(csv_path):
    """Parse downloaded csv file"""
    try:
        with open(str(csv_path), encoding='utf-16') as playlist:
            reader = csv.reader(playlist, delimiter='\t')
            print(reader) # temp
            # parse CSV, then check to see which artist/title pairs exist in current dir
            # move non-existent results to new list
    except IndexError:
        # consider checking for empty playlists when parsing
        # from API on web server instead
        print("You have an empty playlist!")

main()
