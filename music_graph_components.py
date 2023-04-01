"""CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains the Song and Edge class.

The Song class is used to represent a song from Spotify.

The Edge class is used to represent an edge between two Songs.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""
from __future__ import annotations

from python_ta.contracts import check_contracts


@check_contracts
class Song:
    """A song from Spotify.

    Instance Attributes:
        - spotify_id: The Spotify ID of this song.
        - track_name: The name of this song.
        - album_name: The album name of this song.
        - artist_names: The name(s) of the artist(s) of this song.
        - release_date: The date that this song was released.
        - genres: The genre(s) of this song.
        - numerical_traits: A list containing the numerically-quantified traits of this song.
        - edges:
            A mapping containing the songs that are adjacent to this song.
            Each key in the mapping is the Spotify ID of a neighbour song,
            and the corresponding value is an Edge leading to that neighbour song.

    Representation Invariants:
        - self.spotify_id not in self.edges
        - all(self in self.edges[u].endpoints for u in self.edges)
        - self.spotify_id != ''
        - self.track_name != ''
        - self.album_name != ''
        - self.artist_names != []
        - all(name != '' for name in self.artist_names)
        - len(self.numerical_traits) == 13
    """
    spotify_id: str
    track_name: str
    album_name: str
    artist_names: list[str]
    release_date: str
    genres: list[str]
    numerical_traits: list[float]
    edges: dict[str, Edge]

    def __init__(self, spotify_id: str, track_name: str, album_name: str, artist_names: list[str],
                 release_date: str, genres: list[str], numerical_traits: list[float]) -> None:
        """Initialize a new song with an empty collection of edges, the given Spotify ID, track name,
        album name, artist name(s), release date, genre(s), and numerical trait(s).
        """
        self.spotify_id = spotify_id
        self.track_name = track_name
        self.album_name = album_name
        self.artist_names = artist_names
        self.release_date = release_date
        self.genres = genres
        self.numerical_traits = numerical_traits
        self.edges = {}


@check_contracts
class Edge:
    """A link (or "edge") connecting two Songs in a MusicGraph network.

    Instance Attributes:
    - endpoints: The two Songs that are linked by this Edge.

    Representation Invariants:
    - len(self.endpoints) == 2
    - 0.0 <= self._similarity_score <= 1.0
    """
    # Private Instance Attributes:
    #     - _similarity_score:
    #         A float that represents the similarity between the two Songs that are linked by this Edge.
    #         The higher this value is, the more similar the two Songs are.
    endpoints: set[Song]
    _similarity_score: float

    def __init__(self, first_song: Song, second_song: Song) -> None:
        """Initialize an edge with the two given Songs, and
        set self._similarity_score to a starting value of 0.0.

        Also add this Edge to first_song and second_song.

        Preconditions:
            - first_song != second_song
            - first_song and second_song are not already connected by an Edge
        """
        self.endpoints = {first_song, second_song}
        first_song.edges[second_song.spotify_id] = self
        second_song.edges[first_song.spotify_id] = self
        self._similarity_score = (1.0 + self.cosine_similarity(first_song.numerical_traits,
                                                               second_song.numerical_traits)) / 2.0

    def cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        """Returns the cosine similarity between the two input vectors, given that the inputs have length 1.
        (cosine similarity = dot product / lengths)

        Should range from -1.0 to 1.0

        Precondition:
         - sum((v1[i] + v1[i]) ** 2 for i in range(0, len(v1))) == 1
         - sum((v2[i] + v2[i]) ** 2 for i in range(0, len(v1))) == 1"""
        total = sum((v1[i] * v2[i]) for i in range(0, len(v1)))
        assert -1.0 < total < 1.0
        return total

    def get_similarity_score(self) -> float:
        """Return the similarity score of this Edge."""

        return self._similarity_score

    def get_endpoints(self) -> tuple[Song, ...]:
        """Return the two Songs in this Edge's endpoints collection."""
        return tuple(self.endpoints)

    def get_other_endpoint(self, song: Song) -> Song:
        """Return the endpoint of this Edge that is not equal to the given Song.

        Preconditions:
        - song in self.endpoints
        """
        return (self.endpoints - {song}).pop()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 120,
        'max-args': 10,
        'disable': ['R0902']
    })
