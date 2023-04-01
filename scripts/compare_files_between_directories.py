"""
CSC111 Winter 2023 Course Project: MusicMapper
===============================
This script takes a directory as a command line argument and checks if all
subdirectories in the directory have a CSV file that has at least one common song
with a CSV file from at least one other subdirectory. This script must run
successfully on a data directory for this program to work properly.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""

import csv
import os


def read_csv_song_ids(filename: str) -> list[str]:
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


def get_csv_pathnames(folder_name: str) -> list[str]:
    """
    Given a folder name, returns a list of the full pathnames of all csv files within the folder.
    """
    return [os.path.join(folder_name, f) for f in os.listdir(folder_name) if f.endswith('.csv')]


def get_dir_pathnames(folder_name: str) -> list[str]:
    """
    Given a folder name, returns a list of the full pathnames of all subdirectories within the folder.
    """
    return [os.path.join(folder_name, d) for d in os.listdir(folder_name) if os.path.isdir(d)]


def check_similarity(folder_name: str) -> bool:
    """
    Given a folder name, checks whether any two csv files in any two subdirectories within the folder share
    at least one song id. If at least one shared song id is found, returns True. Otherwise, returns False.
    """
    folders = get_dir_pathnames(folder_name)

    for folder1 in folders:
        has_common_line = False
        for folder2 in folders:
            if folder1 != folder2:
                csv_files1 = get_csv_pathnames(folder1)
                csv_files2 = get_csv_pathnames(folder2)

                for file1 in csv_files1:
                    for file2 in csv_files2:
                        if compare_song_ids(file1, file2):
                            has_common_line = True
                            break
                    if has_common_line:
                        break
        if not has_common_line:
            print(
                f'{folder1} does not have a song in common with any other file.')
            return False

    return True


if __name__ == "__main__":
    import sys

    assert len(sys.argv) >= 1
    directory_arg = sys.argv[1]

    if check_similarity(directory_arg):
        print('All folders have a common song with at least one folder.')
