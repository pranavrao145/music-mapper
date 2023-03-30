"""CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains the code responsible for using the Python libraries Networkx and Tkinter to create the
MusicMapper GUI.
Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.
This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""

# imports for tkinter
from tkinter import ttk, Tk, StringVar
import tkinter

# imports for networkx
import networkx as nx

# imports for matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import axes

from python_ta.contracts import check_contracts


@check_contracts
class MainFrame:
    """Generates an instance of the main landing page of MusicMapper along with its functionality.

     Instance Attributes:
        - main_frm: Creates tkinter frame.
        - title_label: Creates MusicMapper title label.
        - song_input: Represents the user song input.
        - song_entry: Creates the entry box for user input.
        - create_playlist_button: Creates a button object that generates a playlist.
    """
    main_frm: Tk
    title_label: ttk.Label
    song_input: StringVar
    song_entry: ttk.Entry
    create_playlist_button: ttk.Button
    playlists_graph: nx.Graph
    fig: Figure
    canvas: FigureCanvasTkAgg
    toolbar: NavigationToolbar2Tk
    ax: axes._axes.Axes

    def __init__(self, main_frm: Tk) -> None:
        # initialize root frame
        self.main_frm = main_frm
        # window size
        self.main_frm.state('zoom')
        # window title
        self.main_frm.title('MusicMapper')

        # create title label
        self.title_label = ttk.Label(main_frm, text='MusicMapper', font=('Trattatello', 120))

        # (user-input) song entry
        self.song_input = StringVar()
        self.song_entry = ttk.Entry(main_frm, textvariable=self.song_input)
        # entry textbox placeholder
        # self.song_entry.insert(0, 'Enter a Song')

        # create playlist button
        self.create_playlist_button = ttk.Button(main_frm, text='Create Playlist')
        # add button functionality
        self.create_playlist_button['command'] = lambda: [self.graph_playlist()]

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
        self.create_playlist_button.pack()

    def graph_playlist(self) -> None:
        """Executes MusicMapper's playlist recommendation algorithm via a button click and represents the results as an
        undirected graph.
        """
        # clears axis and graph to remove the previous graph
        self.ax.clear()
        self.playlists_graph.clear()

        # ********** (TO BE CHANGED) potential example of algorithm output
        input_song = self.button_click()
        songs = [('Eat Your Young', 1.5), ('Eyes Closed', 0.4), ('Jaded', 0.8), ('Run Away to Mars', 0.2)]

        # use loop to create the graph nodes and edges
        for song in songs:
            self.playlists_graph.add_edge(input_song, song[0], weight=song[1])
        # **********

        # produce graph with weighted edges
        self.create_weighted_edges(self.playlists_graph)

    def create_weighted_edges(self, playlist_graph: nx.Graph()) -> None:
        """Produces a graph with weighted edges by embedding the graph in the tkinter interface.
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
        # ********** drawing the graph
        # draw graph nodes
        nx.draw_networkx_nodes(playlist_graph, pos, node_size=700, ax=self.ax)
        # draw node labels
        nx.draw_networkx_labels(playlist_graph, pos, font_size=15, font_family="sans-serif", ax=self.ax)

        # draw the solid edges (high similarity score)
        nx.draw_networkx_edges(playlist_graph, pos, edgelist=elarge, width=6, ax=self.ax)
        # draw the dashed edges (low similarity score)
        nx.draw_networkx_edges(playlist_graph, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style="dashed",
                               ax=self.ax)
        # gets similarity score for each edge via the "weight" attribute. {(song1, song2): similarity_score)}
        edge_labels = nx.get_edge_attributes(playlist_graph, "weight")
        # display the similarity score on the edges
        nx.draw_networkx_edge_labels(playlist_graph, pos, edge_labels, ax=self.ax)

    def button_click(self) -> str:
        """Records and returns the song input upon button click.
        """
        # retrieves and stores user-input
        retrieve_song_input = self.song_entry.get()
        # test print: will delete before final submission
        print(retrieve_song_input)
        return retrieve_song_input


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['networkx', 'matplotlib.backends.backend_tkagg', 'tkinter', 'matplotlib.figure',
    #                       'matplotlib'],
    #     'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120,
    # })

    # create main frame
    root = Tk()
    main_frame_window = MainFrame(root)
    # run GUI
    root.mainloop()
