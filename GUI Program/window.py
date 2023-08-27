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
    

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.running = True
        self.window.title("Lab Controller")
        self.window.wm_protocol("WM_DELETE_WINDOW", self.quit_program)
        print(self.window.winfo_children())
        print(self.window.children)
        self.window.update()

    
    
    def quit_program(self):
        print('quit')
        self.running = False
        self.window.quit()
        self.window.destroy()


if __name__ == "__main__":
    Window()
