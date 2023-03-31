"""CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains the MusicGraph class, which is used to represent the network of Songs.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""
from __future__ import annotations
from python_ta.contracts import check_contracts
from music_graph_components import Song, Edge


# @check_contracts
class MusicGraph:
    """A graph that represents the network of all the Songs from the inputted data set.

    Representation Invariants:
        - all(s == self._songs[s].spotify_id for s in self._songs)
    """
    # Private Instance Attributes:
    #     - _songs:
    #         A collection of the songs contained in this music graph.
    #         Maps the spotify_id of the Song to the Song object.
    _songs: dict[str, Song]

    def __init__(self) -> None:
        """Initialize an empty music graph."""
        self._songs = {}

    def add_song(self, song: Song) -> None:
        """Add a Song object to this music graph.

        The added Song is not adjacent to any other songs.

        Preconditions:
            - song.spotify_id not in self._songs
        """
        self._songs[song.spotify_id] = song

    def add_edge(self, first_song: Song, second_song: Song) -> None:
        """Add an edge between two Songs in this music graph.

        Do nothing if the Spotify ID of the first_song is contained in the edges of second_song.

        Preconditions:
            - first_song != second_song
            - first_song.spotify_id in self._songs
            - second_song.spotify_id in self._songs
        """
        if first_song.spotify_id not in second_song.edges:
            Edge(first_song, second_song)

    def __contains__(self, spotify_id: str) -> bool:
        """Determine whether a song with the given spotify_id is part of this music graph.

        Preconditions:
            - spotify_id is a valid Spotify song ID
        """
        return spotify_id in self._songs

    def __getitem__(self, spotify_id: str) -> Song:
        """Return the Song with the given spotify_id in this music graph.

        Raise ValueError if the given spotify_id is not in this music graph.

        Preconditions:
            - spotify_id is a valid Spotify song ID
        """
        if spotify_id in self._songs:
            return self._songs[spotify_id]
        else:
            raise ValueError

    def get_recommendations(self, song_id: str, num_recs: int) -> list[tuple[str, float]]:
        """Given a song input, return a list of num_recs recommended songs in (song name, similarity score)
        form."""
        song = self[song_id]
        list_of_edges = list(song.edges.values())
        # sort list of edges by similarity score
        list_of_edges.sort(key=lambda edge: edge.get_similarity_score())

        # make sure the list of edges is sorted properly
        assert all(list_of_edges[i].get_similarity_score() <= list_of_edges[i + 1].get_similarity_score()
                   for i in range(len(list_of_edges)))

        results = []
        j = len(list_of_edges) - 1
        while j >= num_recs and j >= 0:
            edge = list_of_edges[j]
            results.append((edge.get_other_endpoint(song).track_name, edge.get_similarity_score()))

        return results



if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['music_graph_components'],  # 'check_contracts'
        # the names (strs) of functions that call print/open/input
        'allowed-io': [],
        'max-line-length': 120
    })
