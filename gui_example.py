'''
    gui_example.py

    An example of opening the GUI.
'''

import sys
import time

from collections import defaultdict

from PyQt5.QtWidgets import QApplication

from maze import Maze, Game, game_repeater
from goodies import WhateverGoody	
from baddies import RandomBaddy
from gui import GameViewer

EXAMPLE_MAZE = Maze(10, 10, "0001010000"
                            "0111010101"
                            "0100000011"
                            "0110100010"
                            "0000100110"
                            "1111100000"
                            "0000001000"
                            "1000111010"
                            "0010001010"
                            "1100101010")

def gui_example():
    ''' Opens a GUI, allowing games to be stepped through or quickly played one after another '''
    app = QApplication.instance() or QApplication(sys.argv)
    gv = GameViewer()
    gv.show()
    gv.set_game_generator(game_repeater(EXAMPLE_MAZE * (3, 3), WhateverGoody, WhateverGoody, RandomBaddy))
    app.exec_()


if __name__ == "__main__":
    gui_example()
