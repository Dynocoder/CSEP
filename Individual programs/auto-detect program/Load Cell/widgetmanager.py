"""
The Widget Manager object, creates the widget manager menu. Contains methods to control the channels and the 
communication with serial port.
"""

import tkinter as tk
from tkinter import ttk
import displaygui
import threading
import csv


class WidgetManager():

    def __init__(self, root, port_manager, file_name=None, minimal=False):
        self.window = root
        self.minimal = minimal
        self.file_name = file_name
        # self.widget_frame = widget_frame
        self.port_manager = port_manager
        # Read thread status
        self.read_thread = False
        # List of the field names to write on the file
        self.fieldnames = ["time"]
        # true if the fieldnames are written on the data file, false otherwise.
        self.fieldname_written = False
        # The list of the widget type
        self.widgets = ["Temperature", "pH", "Load Cell"]
        # delay time list
        self.delay = [1, 5, 10, 15, 30, 45, 60, 90, 120]
        # List of all the tkinter objects in the main window
        self.children = self.window.winfo_children()
        # Command key value pairs
        self.systems = {"Temperature": "t0", "Load Cell": "l0", "pH": "p0"}


        # DISPLAY object to control the widgets
        self.display = displaygui.DisplayGUI(self.window, self.port_manager)

        # Widget Manager Tab
        self.widget_manager = tk.LabelFrame(self.window, text="Widget Manager", padx=5, pady=5, width=30)


        self.menu_text = tk.Label(self.widget_manager, text="Select Widget:", padx=5, pady=5)
        self.delay_text = tk.Label(self.widget_manager, text="Select Delay (in seconds): ", padx=5, pady=5)


        # Widget Type Menu
        self.swidget = tk.StringVar(self.widget_manager)
        self.swidget.set(self.widgets[0])
        self.widget_menu = tk.OptionMenu(self.widget_manager, self.swidget, *self.widgets)

        # Delay Menu
        self.sdelay = tk.StringVar(self.widget_manager)
        self.sdelay.set(self.delay[1])
        self.delay_menu = tk.OptionMenu(self.widget_manager, self.sdelay, *self.delay)

        # Add/Remove Widgets
        self.add_widget = tk.Button(self.widget_manager, text="Add", padx=5, pady=5, command=self.add)
        self.remove_widget = tk.Button(self.widget_manager, text="Remove", padx=5, pady=5, command=self.remove)

        # separator line (visual purposes only)
        self.separator = ttk.Separator(self.widget_manager, orient="vertical")

        # Start/Stop Stream
        self.start_stream = tk.Button(self.widget_manager, text="Start", padx=5, pady=5, command=self.start)
        self.stop_stream = tk.Button(self.widget_manager, text="Stop", padx=5, pady=5, command=self.stop)

        # Start/Stop Saving
        self.save_data = tk.BooleanVar()
        self.start_saving = tk.Checkbutton(self.widget_manager, text="Start Saving", variable=self.save_data, padx=5, pady=5)


        self.publish()

    
    def publish(self):
        """ Placing the elements on the window, using grid placement """
        if self.minimal:
            # Widget Config Tab
            self.widget_manager.grid(row=0, column=3, padx=5, pady=5, columnspan=5,sticky="nsew", rowspan=2)
            self.delay_text.grid(row=1, column=0)
            self.delay_menu.grid(row=1, column=1, sticky="nsew", padx=5)

            self.start_stream.grid(row=0, column=0, sticky="", padx=15)
            self.stop_stream.grid(row=0, column=1, sticky="", padx=15)
            self.stop_stream['state'] = 'disable'

        else:
            # Widget Config Tab
            self.widget_manager.grid(row=0, column=4, padx=5, pady=5, columnspan=5,sticky="nsew", rowspan=2)

            self.menu_text.grid(row=0, column=0)
            self.widget_menu.grid(row=0, column=1, padx=5)
            self.delay_text.grid(row=1, column=0)
            self.delay_menu.grid(row=1, column=1, sticky="nsew", padx=5)
            self.add_widget.grid(row=0, column=2, sticky="nsew", padx=5)
            self.remove_widget.grid(row=1, column=2, padx=5)

            self.separator.place(relx=0.71, rely=0, relwidth=0.001, relheight=1)

            self.start_stream.grid(row=0, column=3, sticky="", padx=15)
            self.stop_stream.grid(row=0, column=4, sticky="", padx=15)
            self.stop_stream['state'] = 'disable'
            self.start_saving.grid(row=1, column=3, columnspan=2, padx=15)


    
    def add(self, frame_type):
        """ 
        This module Adds a widget frame to the grid
        """
        # Collecting the widget from the widget type menu or externally
        if self.minimal:
            self.frame_type = frame_type
        else:
            self.frame_ype = self.swidget.get()
        # creating the widget.
        self.display.addFrame(self.frame_type)
        print(self.display.frames)
        command = self.systems[self.frame_type]
        self.port_manager.set_channel(self.display.frameCount, command)

        # TESTING PRINTING
        print(command)
        print(self.port_manager.channels)

    
    def remove(self):
        """ Removing the widget frames from the grid"""
        if self.display.frameCount >= 1:
            self.display.removeFrame()
    
    def start(self):
        """
        this module starts the reading process.
        Changes necessary GUI elements, calls the required methods.
        """
        # Disable adding new Frames and option menus
        self.add_widget['state'] = "disable"
        self.remove_widget['state'] = "disable"
        self.widget_menu['state'] = "disable"
        self.delay_menu['state'] = "disable"
        self.start_stream['state'] = "disable"
        self.stop_stream['state'] = "active"
        self.read_thread = True
        
        self.getData()

    def stop(self):
        """
        This module stops the reading process.
        changes the elements attributes back to the original state.
        """
        # Enable adding new Frames and option menus
        self.add_widget['state'] = "active"
        self.widget_menu['state'] = "active"
        self.delay_menu['state'] = "active"
        self.remove_widget['state'] = "active"
        self.start_stream['state'] = "active"
        self.stop_stream['state'] = "disable"
        self.read_thread = False
        self.port_manager.read = False


    def getData(self):
        """
        The Function uses the port_manager object and reads the data from the serial port using the portcom module.
        """

        # if the thread is true
        if self.read_thread:
            # if the arduino is connected
            if self.port_manager.getPortStatus():
                self.port_manager.read = True
                self.port_manager.t1 = threading.Thread(
                    target=self.port_manager.read_thread, args=(self, self.display,), daemon=True)
                self.port_manager.t1.start()
                
            else:
                tk.messagebox.showerror('Port Disconnected', 'Error: Port Disconnected. Can not read Value')
                return


    
    def save_to_file(self, response_list, time):
        """ Saving the data to the file """
        # list of data values
        data_list = []

        # appending the data values according to the widgets 
        for i in range(self.display.frameCount):
            data_list.append(float(response_list[i]))

        # data row to append in file
        row_data = {}
        
        # if the fieldnames are already written on the file
        if self.fieldname_written:

            # Opening and editing the file
            with open(self.file_name + ".csv", 'a', newline="") as wtr:
                writer = csv.DictWriter(wtr, fieldnames=self.fieldnames)
                # if the data is already written, start from last time added
                if len(self.display.times[0]) > 0:
                    row_data = {"time": int(self.display.times[0][-1])}
                else:
                    row_data = {"time": 0}
                row_data.update({f"c{i}": value for i, value in enumerate(data_list, start=1)})
                print(row_data)
                print(self.fieldnames)
                writer.writerow(row_data)
            wtr.close()
        else:
            # Generating Fieldnames
            for i in range(self.display.frameCount):
                self.fieldnames = ["time"] + [f'c{i+1}' for i in range(self.display.frameCount)]
            with open(self.file_name + ".csv", 'w', newline="") as wtr:
                writer = csv.DictWriter(wtr, fieldnames=self.fieldnames)
                writer.writeheader()
            wtr.close()
            self.fieldname_written = True
            self.save_to_file(response_list, time)


if __name__ == "__main__":
    WidgetManager()