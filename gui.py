"""CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains the code responsible for using the Python libraries Networkx, MatPlotLib, and Tkinter
to create the MusicMapper GUI and integrate the functionality.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""

# imports for tkinter
from tkinter import ttk, Tk, StringVar
import tkinter

from typing import Any

# imports for networkx
import networkx as nx

# imports for matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

# imports for MusicMapper
from python_ta.contracts import check_contracts
from music_graph import MusicGraph


@check_contracts
class MainFrame:
    """Generates an instance of the main page along with its functionality.

     Instance Attributes:
        - main_frm: Creates the tkinter frame.
        - music_graph: Creates an instance of the MusicGraph class.
        - title_label: Creates the title label.
        - song_input: Represents the user song input.
        - artist_input: Represents the user artist input.
        - num_songs_input: Represents the desired song number input.
        - artist_entry: Creates an entry box for the user to input artist name.
        - song_entry: Creates an entry box for the user to input song name.
        - num_songs_entry: Creates a spinbox for the user to choose the number of recommended songs.
        - create_playlist_button: Creates a button object.
        - playlists_graph: Creates a networkx graph object.
        - fig: Creates a figure object.
        - canvas: Creates a canvas object.
        - toolbar: Creates a toolbar.
        - ax: Creates the graph axes.

    Preconditions:
    - the song_input and artist_input are valid inputs found in the dataset.
    - artist_input must be the artist of the song associated with song_input.
    """
    main_frm: Tk
    music_graph: MusicGraph
    title_label: ttk.Label
    song_input: StringVar
    artist_input: StringVar
    num_songs_input: StringVar
    artist_entry: ttk.Entry
    song_entry: ttk.Entry
    num_songs_entry: ttk.Spinbox
    create_playlist_button: ttk.Button
    playlists_graph: nx.Graph
    fig: Figure
    canvas: FigureCanvasTkAgg
    toolbar: NavigationToolbar2Tk
    ax: Any

    def __init__(self, main_frm: Tk, music_graph: MusicGraph) -> None:
        """Initialize the tkinter interface.
        """
        # initialize root frame
        self.main_frm = main_frm
        # window size
        self.main_frm.state('zoom')
        # window title
        self.main_frm.title('MusicMapper')
        # create music graph object
        self.music_graph = music_graph

        # create title label
        self.title_label = ttk.Label(
            main_frm, text='MusicMapper', font=('BM Hanna Pro', 120))

        # (user-input) song entry
        self.song_input = StringVar()
        self.song_entry = ttk.Entry(main_frm, textvariable=self.song_input)
        # entry textbox placeholder
        self.song_entry.insert(0, 'Enter a Song')

        # (user-input) artist entry
        self.artist_input = StringVar()
        self.artist_entry = ttk.Entry(main_frm, textvariable=self.artist_input)
        # entry textbox placeholder
        self.artist_entry.insert(0, 'Enter an Artist')

        # (user-input) number of songs
        self.num_songs_input = StringVar()
        self.num_songs_entry = ttk.Spinbox(
            main_frm, from_=1, to=50, textvariable=self.num_songs_input, state='readonly')
        self.num_songs_entry.insert(0, '1')

        # create playlist button
        self.create_playlist_button = ttk.Button(
            main_frm, text='Create Playlist')
        # add button functionality
        self.create_playlist_button['command'] = lambda: [
            self.graph_playlist()]

        # ********** graph elements
        # create graph object
        self.playlists_graph = nx.Graph()
        # create figure object (holds plot elements)
        self.fig = Figure(figsize=(5, 4), dpi=100, frameon=False)
        # adds canvas to interface
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frm)
        # create toolbar for graph
        self.toolbar = NavigationToolbar2Tk(self.canvas, main_frm)
        self.toolbar.update()
        # creates plot axis
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        # removes axis frame that obscures graph
        self.ax.axis('off')

        # adjust widget positions
        self.title_label.pack()
        self.song_entry.pack()
        self.artist_entry.pack()
        self.num_songs_entry.pack()
        self.create_playlist_button.pack()

    def graph_playlist(self) -> None:
        """Executes MusicMapper's playlist recommendation algorithm via a button click and represents the results as an
        undirected graph.
        """
        # clears axis and graph to remove the previous graph
        self.ax.clear()
        self.playlists_graph.clear()

        # ********** recommendation algorithm
        input_song = self.button_click()[0]
        input_artist = self.button_click()[1]
        num_songs = self.button_click()[2]

        spotify_id = self.music_graph.get_spotify_id(input_song, input_artist)

        songs = self.music_graph.get_recommendations(spotify_id, num_songs)

        # use loop to create the graph nodes and edges
        for song in songs:
            self.playlists_graph.add_edge(input_song, song[0], weight=song[1])

        # produce graph with weighted edges
        self.create_weighted_edges(self.playlists_graph)

    def create_weighted_edges(self, playlist_graph: nx.Graph()) -> None:
        """Produces the graph's weighted edges and embeds the graph in the tkinter interface.
        """
        # filter edges with high v.s. low similarity scores into two separate lists
        elarge = [(song1, song2) for (song1, song2, weights) in playlist_graph.edges(data=True) if
                  weights["weight"] > 0.5]
        esmall = [(song1, song2) for (song1, song2, weights) in playlist_graph.edges(data=True) if
                  weights["weight"] <= 0.5]

        # node positions (dict where each key is a node that corresponds to its position)
        pos = nx.spring_layout(playlist_graph, seed=7)
        # adds canvas to interface
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # call to draw_graph
        self.draw_graph(playlist_graph, pos, elarge, esmall)
        self.canvas.draw()

    def draw_graph(self, playlist_graph: nx.Graph(), pos: dict, elarge: list, esmall: list) -> None:
        """Draws the nodes, edges, and labels of the graph.
        """
        # draw graph nodes
        nx.draw_networkx_nodes(playlist_graph, pos,
                               node_size=850, node_color="#2a9d8f", ax=self.ax)
        # draw node labels
        nx.draw_networkx_labels(
            playlist_graph, pos, font_size=23, font_family="Times New Roman", ax=self.ax)

        # draw the solid edges (high similarity score)
        nx.draw_networkx_edges(
            playlist_graph, pos, edgelist=elarge, width=6, edge_color="#e76f51", ax=self.ax)
        # draw the dashed edges (low similarity score)
        nx.draw_networkx_edges(playlist_graph, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="#264653",
                               style="dashed", ax=self.ax)

        # gets similarity score for each edge via the "weight" attribute. {(song1, song2): similarity_score)}
        edge_labels = nx.get_edge_attributes(playlist_graph, "weight")
        # display the similarity score on the edges
        nx.draw_networkx_edge_labels(playlist_graph, pos, edge_labels, font_family="Times New Roman",
                                     font_size=17, ax=self.ax)

    def button_click(self) -> tuple[str, str, int]:
        """Records and returns the song input and artist input upon button click.
        """
        # retrieves and stores user-input
        retrieve_song_input = self.song_entry.get()
        retrieve_artist_input = self.artist_entry.get().split(",")[0]
        retrieve_num_songs_input = int(self.num_songs_entry.get())

        return (retrieve_song_input, retrieve_artist_input, retrieve_num_songs_input)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'matplotlib.backends.backend_tkagg', 'tkinter', 'matplotlib.figure',
                          'matplotlib', 'music_graph', 'build_music_graph'],
        'allowed-io': [],
        'disable': ['R0902'],
        'max-line-length': 120,
    })
