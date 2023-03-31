"""CSC111 Winter 2023 Course Project: MusicMapper
===============================
This module contains the main block, which contains the code
necessary for running our entire program.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the CSC111
community at the University of Toronto St. George campus.

This file is Copyright (c) 2023 Yibing Ju, Jiya Patel, Pranav Rao, and Bruce Liu.
"""
from tkinter import Tk
from gui import MainFrame
from build_music_graph import create_song_network

if __name__ == '__main__':
    # Create our MusicGraph.
    music_graph = create_song_network('data')
    root = Tk()
    main_frame_window = MainFrame(root, music_graph)
    # Run GUI
    root.mainloop()
