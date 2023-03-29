"""
CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains function(s) for reading in CSV files of Spotify data
created by Exportify.net and building a MusicGraph out of this data.
In order for the functions in this file to be able to process any given CSV file,
the CSV file must have rows in the following format (the numbers represent the
index of the property in the line):

0: Spotify ID
1: Artist IDs
2: Track Name
3: Album Name
4: Artist Name(s)
5: Release Date
6: Duration (ms)
7: Popularity
8: Added By
9: Added At
10: Genres
11: Danceability
12: Energy
13: Key
14: Loudness
15: Mode
16: Speechiness
17: Acousticness
18: Instrumentalness
19: Liveness
20: Valence
21: Tempo
22: Time Signature

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.
This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""

from glob import glob
import os
import csv
from python_ta.contracts import check_contracts
from music_graph import MusicGraph
from music_graph_components import Song


@check_contracts
def create_song_network(data_dir: str) -> MusicGraph:
    """
    Given a data directory, go through each subfolder in that directory and
    read the csv files under the subfolders. Use the information to create
    several new Songs, put them into a new MusicGraph, and return the new
    MusicGraph.
    Preconditions:
    - data_dir and its subdirectories contain csv files of the correct format,
      as described by the module header
    """
    music_graph = MusicGraph()
    all_csv_files = [file for path, _, _ in os.walk(
        data_dir) for file in glob(os.path.join(path, '*.csv'))]

    for f in all_csv_files:
        with open(f) as csv_file:
            songs_so_far = []
            reader = csv.reader(csv_file)

            next(reader)

            for line in reader:
                song_id = line[0]

                if song_id not in music_graph:
                    song_numerical_traits = {
                        "popularity": float(line[7]),
                        "danceability": float(line[11]),
                        "energy": float(line[12]),
                        "key": float(line[13]),
                        "loudness": float(line[14]),
                        "mode": float(line[15]),
                        "speechiness": float(line[16]),
                        "acousticness": float(line[17]),
                        "instrumentalness": float(line[18]),
                        "liveness": float(line[19]),
                        "valence": float(line[20]),
                        "tempo": float(line[21]),
                        "time signature": float(line[22])
                    }

                    song = Song(
                        spotify_id=line[0],
                        track_name=line[2],
                        album_name=line[3],
                        artist_names=line[4].split(','),
                        release_date=line[5],
                        genres=line[10].split(','),
                        numerical_traits=song_numerical_traits
                    )

                    music_graph.add_song(song)
                    songs_so_far.append(song_id)

            for i in range(len(songs_so_far)):
                for j in range(i + 1, len(songs_so_far)):
                    music_graph.add_edge(
                        music_graph[songs_so_far[i]], music_graph[songs_so_far[j]])

    return music_graph


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['glob', 'os', 'csv', 'datetime', 'music_graph', 'music_graph_components'],
        'allowed-io': ['create_song_network'],
        'max-line-length': 120
    })
