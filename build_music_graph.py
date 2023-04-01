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
from __future__ import annotations

from glob import glob
import os
import csv
import numpy
from sklearn.preprocessing import StandardScaler

# from python_ta.contracts import check_contracts
from music_graph import MusicGraph
from music_graph_components import Song


# @check_contracts
def build_music_graph(data_dir: str) -> MusicGraph:
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
    subdirectories = [info[0] for info in os.walk(data_dir)]
    subdirectories = subdirectories[1:]

    for subdirectory in subdirectories:
        _process_folder(subdirectory, music_graph)

    return music_graph


# @check_contracts
def _norm(v1: list[float]) -> float:
    """Returns the norm of a vector."""
    total = sum((item * item) for item in v1)
    return total ** (1 / 2)


# @check_contracts
def _process_folder(subdirectory: str, music_graph: MusicGraph) -> None:
    """
    Given a subfolder in a data directory that ONLY contains CSV files of the format
    specified in the module header, iterate through each CSV file and add it to the
    song graph.

    In addition, standardize and normalize the numerical traits based on song
    data in the FOLDER, and add edges between each song that share a PLAYLIST.
    (Note: the reasoning is that two songs might share more than one playlist
    within a genre (subfolder), but not across different subfolders. Also, bell
    shape can be assumed when operating on subfolders but not necessarily
    across different folders, so standardization works only on the subfolder
    level.)

    Preconditions:
    - data directory only contains CSV file of the format specified in the module header
    """
    csv_files = [file for path, _, _ in os.walk(
        subdirectory) for file in glob(os.path.join(path, '*.csv'))]

    playlists = []  # list that contains lists that represent playlists of songs

    for f in csv_files:
        with open(f, encoding="utf8") as csv_file:
            songs_so_far = []
            reader = csv.reader(csv_file)

            next(reader)

            for line in reader:
                song_id = line[0]

                if song_id not in music_graph:
                    song_numerical_traits = [float(line[7])] + [float(line[k]) for k in range(11, 23)]

                    song = Song(
                        spotify_id=line[0],
                        track_name=line[2],
                        artist_names=line[4].split(','),
                        numerical_traits=song_numerical_traits
                    )

                    music_graph.add_song(song)
                songs_so_far.append(song_id)
            playlists.append(songs_so_far)

    # process data
    _standardize_data(playlists, music_graph)

    # iterate through each playlist and add edges
    for playlist in playlists:
        for i in range(0, len(playlist)):
            for j in range(i + 1, len(playlist)):
                music_graph.add_edge(
                    music_graph[playlist[i]], music_graph[playlist[j]])


# @check_contracts
def _standardize_data(playlists: list[list[str]], music_graph: MusicGraph) -> None:
    """Given a list that contains each playlist and a MusicGraph, mutate each
    song's numerical traits so that they're standardized and normalized.

    Precondition:
      - all(all(song in music_graph for song in playlist) for playlist in playlists)
    """
    # process data
    all_vectors = []  # list that contains sublists for all numerical traits of all songs
    for playlist in playlists:
        for song_id in playlist:
            all_vectors.append(music_graph[song_id].numerical_traits)

    # cast data from a list of list to a 2D array for preprocessing
    song_array = numpy.array(all_vectors)

    # standardization
    st_scalar = StandardScaler()
    standardized_data = st_scalar.fit_transform(song_array)
    # check that the means are close to 0 and standard deviations are 1
    assert all(-0.0001 < value < 0.0001 for value in standardized_data.mean(axis=0))
    assert all(0.9999 < value < 1.0001 for value in standardized_data.std(axis=0))

    # cast 2D array to a list of lists
    list_of_traits = standardized_data.tolist()

    # normalization by scaling to length 1
    for i in range(0, len(list_of_traits)):
        v = list_of_traits[i]
        prod = _norm(v)
        list_of_traits[i] = [item / prod for item in v]

    # update each song's numerical trait
    m = 0
    for playlist in playlists:
        for song_id in playlist:
            music_graph[song_id].numerical_traits = list_of_traits[m]
            m += 1

    # should be true if all numerical_traits are correctly scaled to have length 1
    assert all(all(0.9999 < _norm(music_graph[s_id].numerical_traits) < 1.0001 for s_id in plst)
               for plst in playlists)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['glob', 'os', 'csv', 'datetime', 'music_graph', 'music_graph_components',
                          "sklearn.preprocessing", "numpy"],
        'allowed-io': ['_process_folder'],
        'max-line-length': 120
    })
