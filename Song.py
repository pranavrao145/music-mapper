"""CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains the Song class, which is used to represent a song from Spotify.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""
from __future__ import annotations
from Edge import Edge
import datetime
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
        - numerical_traits:
            A mapping containing the numerically-quantified traits of this song.
            Each key in the mapping is the name of the trait, and the corresponding
            value is the numerical value of that trait.
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
        - all(name != '' for name in self.artist_names)
        - all(genre != '' for genre in self.genres)
        - all(trait_name != '' for trait_name in self.numerical_traits)
    """
    spotify_id: str
    track_name: str
    album_name: str
    artist_names: list[str]
    release_date: datetime.date
    genres: list[str]
    numerical_traits: dict[str, float]
    edges: dict[str, Edge]

    def __init__(self, spotify_id: str, track_name: str, album_name: str, artist_names: list[str],
                 release_date: datetime.date, genres: list[str], numerical_traits: dict[str, float]) -> None:
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


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations', 'Edge', 'datetime', 'check_contracts'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
