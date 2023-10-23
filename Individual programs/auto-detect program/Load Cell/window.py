"""
The Basic Window object, Creates the initial window for other objects to create objects upon.
"""

import tkinter as tk
import tkinter.messagebox
import serial.tools.list_ports
import portcom as pc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import csv
import os


class Window():
    def __init__(self, title="Lab Controller") -> None:
        self.window = tk.Tk()
        # The state of the program.
        self.running = True
        self.window.title(title)
        # calls the self.quit_program function when the window is closed using the cross.
        self.window.wm_protocol("WM_DELETE_WINDOW", self.quit_program)

        # TESTING PRINTING
        print(self.window.winfo_children())
        print(self.window.children)

        self.window.update()

    
    """ Closes the tkinter window and ends the program """
    def quit_program(self):
        print('quit')
        self.running = False
        self.window.quit()
        self.window.destroy()


if __name__ == "__main__":
    Window()
