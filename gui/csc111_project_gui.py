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
from python_ta.contracts import check_contracts

# imports for networkx
import networkx as nx


# imports for matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# imports for tkinter
from tkinter import ttk
from tkinter import *
import tkinter

# styles
frame_colour = '#247BA0'
label_colour = '#247BA0'


def graph_playlist():
    """Executes MusicMapper's playlist recommendation algorithm via a button click and represents the results as an
    undirected graph.
    """
    # create graph object
    playlist_graph = nx.Graph()

    # ********** (TO BE CHANGED) potential example of algorithm output
    input_song = 'Die For You'
    songs = [('Eat Your Young', 1.5), ('Eyes Closed', 0.4), ('Jaded', 0.8), ('Run Away to Mars', 0.2)]

    # use loop to create the graph nodes and edges
    for song in songs:
        playlist_graph.add_edge(input_song, song[0], weight=song[1])
    # **********

    # produce graph with weighted edges
    create_weighted_edges(playlist_graph)


def create_weighted_edges(playlist_graph: nx.Graph()) -> None:
    """Produces a graph with weighted edges by embedding the graph in the tkinter interface.
    """
    # filter edges with high v.s. low similarity scores into two separate lists
    elarge = [(song1, song2) for (song1, song2, weights) in playlist_graph.edges(data=True) if weights["weight"] > 0.5]
    esmall = [(song1, song2) for (song1, song2, weights) in playlist_graph.edges(data=True) if weights["weight"] <= 0.5]

    # create figure object (holds plot elements)
    fig = Figure(figsize=(5, 4), dpi=100, frameon=False)

    # node positions (dict where each key is a node that corresponds to its position)
    pos = nx.spring_layout(playlist_graph, seed=7)

    # call to draw_graph
    draw_graph(playlist_graph, pos, fig, elarge, esmall)

    # creates canvas that will hold the graph that will be embedded into the tkinter interface
    canvas = FigureCanvasTkAgg(fig, master=root)

    # adds toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    # adds canvas to interface
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def draw_graph(playlist_graph: nx.Graph(), pos: dict, fig: Figure, elarge: list, esmall: list) -> None:
    """Draws the nodes, edges, and labels of the graph.
    """

    # add axis to figure
    ax = fig.add_axes([0, 0, 1, 1])
    # removes frame that obscures graph
    ax.axis('off')

    # ********** drawing the graph
    # draw graph nodes
    nx.draw_networkx_nodes(playlist_graph, pos, node_size=700, ax=ax)
    # draw node labels
    nx.draw_networkx_labels(playlist_graph, pos, font_size=15, font_family="sans-serif", ax=ax)

    # draw the solid edges (high similarity score)
    nx.draw_networkx_edges(playlist_graph, pos, edgelist=elarge, width=6, ax=ax)
    # draw the dashed edges (low similarity score)
    nx.draw_networkx_edges(playlist_graph, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style="dashed",
                           ax=ax)

    # gets the similarity score for each edge by accessing the "weight" attribute. {(song1, song2): similarity_score)}
    edge_labels = nx.get_edge_attributes(playlist_graph, "weight")
    # display the similarity score on the edges

    nx.draw_networkx_edge_labels(playlist_graph, pos, edge_labels, ax=ax)


class MainFrame:
    """Generates an instance of the main landing page of MusicMapper along with its functionality.
    """
    def __init__(self, main_frm):
        # initialize root frame
        self.main_frm = main_frm
        self.create_widgets(self.main_frm)

    def create_widgets(self, main_frm):
        """Creates the graph elements/widgets.
        """
        # create title label
        self.title_label = ttk.Label(main_frm, text='MusicMapper', font=('Trattatello', 120))

        # (user-input) song entry
        self.song_input = StringVar()
        self.song_entry = ttk.Entry(main_frm, textvariable=self.song_input)
        # entry textbox placeholder
        # self.song_entry.insert(0, 'Enter a Song')

        # create playlist button
        self.create_playlist_button = ttk.Button(main_frm, text='Create Playlist')
        self.create_playlist_button['command'] = lambda: [self.button_click(), graph_playlist()]

        # adjust widget positions
        self.title_label.pack()
        self.song_entry.pack()
        self.create_playlist_button.pack()

    def button_click(self) -> str:
        """Creates graph and records the song input upon button click.
        """
        # retrieves and stores user-input
        retrieve_song_input = self.song_entry.get()
        # test print
        print(retrieve_song_input)
        return retrieve_song_input


# creates a window
root = Tk()
# window size
root.state('zoom')
# change name of window
root.title('MusicMapper')

# create instance of main frame
main_frame_window = MainFrame(root)
# retrieve user input
user_input = main_frame_window.button_click()

# runs GUI
root.mainloop()


# Note: python_ta is giving me a lot of errors right now (which I'll have to resolve)
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['networkx', 'matplotlib.pyplot', 'matplotlib.animation', 'tkinter'],
    #     'allowed-io': [],     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
