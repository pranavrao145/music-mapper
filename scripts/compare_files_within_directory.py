# TODO: make these decent

import csv
import os
import sys


def read_csv_song_ids(filename: str):
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        # only returning song id's
        return [line[0] for line in reader]


def compare_song_ids(file1: str, file2: str) -> bool:
    file1_data = read_csv_song_ids(file1)
    file2_data = read_csv_song_ids(file2)

    # just comparing song id's
    for id1 in file1_data:
        for id2 in file2_data:
            if id1 == id2:
                print(id1)
                return True

    return False

    # return any(id1 == id2 for id2 in file2_data for id1 in file1_data)


def get_pathnames(folder_name: str) -> list[str]:
    return [os.path.join(folder_name, f) for f in os.listdir(folder_name) if f.endswith('.csv')]


def check_similarity(folder_name: str):
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
    if sys.argv:
        directory_arg = sys.argv[1]
    else:
        directory_arg = os.getcwd()

    if check_similarity(directory_arg):
        print('All playlists have a common song with at least one other playlist.')
