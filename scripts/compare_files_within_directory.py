"""
CSC111 Winter 2023 Course Project: MusicMapper
===============================
This script takes a directory as a command line argument and checks if each CSV
File in the directory has at least one common song with another CSV file from
the directory. This script must run successfully on a data directory for this
program to work properly.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""

import csv
import os
import sys


def read_csv_song_ids(filename: str):
    """
    Given a csv filename, reads the file and returns a list of song ids.
    """
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        # only returning song id's
        return [line[0] for line in reader]


def compare_song_ids(file1: str, file2: str) -> bool:
    """
    Given two csv filenames, reads and compares the song ids in each file. If at least one song id is
    common between the two files, returns True. Otherwise, returns False.
    """

    file1_data = read_csv_song_ids(file1)
    file2_data = read_csv_song_ids(file2)

    return any(id1 == id2 for id2 in file2_data for id1 in file1_data)


def get_pathnames(folder_name: str) -> list[str]:
    """
    Given a folder name, returns a list of the full pathnames of all subdirectories within the folder.
    """
    return [os.path.join(folder_name, f) for f in os.listdir(folder_name) if f.endswith('.csv')]


def check_similarity(folder_name: str):
    """
    Given a directory name, checks each csv file shares at least one song id
    with another csv file in this directory. If at least one shared song id is
    found, returns True. Otherwise, returns False. 
    """
    csv_files = get_pathnames(folder_name)

    for file1 in csv_files:
        has_common_line = False

        for file2 in csv_files:
            if file1 != file2:
                if compare_song_ids(file1, file2):
                    has_common_line = True
                    break
        if not has_common_line:
            print(f'{file1} does not have a song in common with any other file.')
            return False

    return True


if __name__ == "__main__":
    import sys

    assert len(sys.argv) >= 1
    directory_arg = sys.argv[1]

    if check_similarity(directory_arg):
        print('All playlists have a common song with at least one other playlist.')
