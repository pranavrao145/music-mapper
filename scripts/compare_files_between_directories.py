# TODO: make these decent

import csv
import os


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


def get_csv_pathnames(folder_name: str) -> list[str]:
    return [os.path.join(folder_name, f) for f in os.listdir(folder_name) if f.endswith('.csv')]


def get_dir_pathnames(folder_name: str) -> list[str]:
    return [os.path.join(folder_name, d) for d in os.listdir(folder_name) if os.path.isdir(d)]


def check_similarity(folder_name: str):
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
    if check_similarity(os.getcwd()):
        print('All folders have a common song with at least one folder.')
