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

    def __init__(self, root, widget_frame, port_manager, main_screen):
        self.window = root
        self.mainscreen_object = main_screen
        self.widget_frame = widget_frame
        self.port_manager = port_manager
        self.read_thread = False
        self.fieldnames = ["time"]
        self.fieldname_written = False
        self.widgets = ["Temperature", "pH", "Load Cell"]
        self.delay = [1, 5, 10, 15, 30, 45, 60, 90, 120]
        self.children = self.window.winfo_children()
        self.systems = {"Temperature": "t0", "Load Cell": "l0", "Load Cell Calibrate": "lc"}

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


    def add(self):

        # Collecting the widget from the widget type menu
        frameType = self.swidget.get()
        # creating the widget.
        self.display.addFrame(frameType)
        print(self.display.frames)
        command = self.systems[frameType]
        self.port_manager.set_channel(self.display.frameCount, command)

        print(command)
        print(self.port_manager.channels)

        # print(self.window.children)
        # print(self.window.winfo_children())

        # # If the window has less than 4 widgets displalyed
        # if (len(self.widget_frame.winfo_children()) < 4):
        #     match len(self.widget_frame.winfo_children()):
        #         case 0:
        #             self.row = 1
        #             self.column = 0
        #         case 1: 
        #             self.row = 1
        #             self.column = 1
        #         case 2:
        #             self.row = 2
        #             self.column = 0
        #         case 3:
        #             self.row = 2
        #             self.column = 1

        #     match self.swidget.get():
        #         case "Temperature":
        #             # dd = dw.DataWidget(self.widget_frame, "Temperature", self.arduino, "data.csv", 4, self.row, self.column)
        #             dd = tk.Label(self.widget_frame, text="1", padx=5, pady=5).grid(row=1, column=0, columnspan=4)
        #         case "pH":
        #             dd = dw.DataWidget(self.widget_frame, "pH", self.port_manager, "data.csv", 4, self.row, self.column)
        #         case "Load Cell":
        #             dd = dw.DataWidget(self.widget_frame, "Load Cell", self.port_manager, "data.csv", 4, self.row, self.column)
                    
            

        # print(self.widget_type)

    def remove(self):
        # self.window.winfo_children()[0].grid(row=0, column=0)
        # if (len(self.widget_frame.winfo_children()) > 0):
        #     print(self.widget_frame.winfo_children())
        #     self.widget_frame.winfo_children()[-1].grid_forget()
        #     self.widget_frame.winfo_children().pop()
        if self.display.frameCount >= 1:
            self.display.removeFrame()
    
    def start(self):
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
        # if the arduino is connected
        if self.read_thread:
            if self.port_manager.getPortStatus():
                # print("port status" + self.port_manager.getPortStatus())
                self.port_manager.read = True
                self.port_manager.t1 = threading.Thread(
                    target=self.port_manager.read_thread, args=(self, self.display,), daemon=True)
                self.port_manager.t1.start()
                
            else:
                tk.messagebox.showerror('Port Disconnected', 'Error: Port Disconnected. Can not read Value')
                return


    def save_to_file(self, response_list, time):

        data_list = []

        for i in range(self.display.frameCount):
            data_list.append(float(response_list[i]))

        


        row_data = {}
        

        if self.fieldname_written:

            # Opening and editing the file
            with open(self.mainscreen_object.get_file_name() + ".csv", 'a', newline="") as wtr:
                writer = csv.DictWriter(wtr, fieldnames=self.fieldnames)
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
            with open(self.mainscreen_object.get_file_name() + ".csv", 'w', newline="") as wtr:
                writer = csv.DictWriter(wtr, fieldnames=self.fieldnames)
                writer.writeheader()
            wtr.close()
            self.fieldname_written = True
            self.save_to_file(response_list, time)




        # # Reading throught the created file
        # with open (self.mainscreen_object.get_file_name() + ".csv", 'r') as rdr:
        #     reader = csv.DictReader(rdr)
        #     print("rdr_obj ", reader)
        #     print("rdline", rdr.readline())
        #     print("rdlinelen", len(rdr.readline()))
        #     # If the created file is empty. (no header data)
        #     # Checking whether the file is new (no headers written)
        #     if len(rdr.readlines()) == 0:
        #         print("if called")
        #         with open(self.mainscreen_object.get_file_name() + ".csv", 'w') as wtr:
        #             writer = csv.DictWriter(wtr, fieldnames=self.fieldnames)
        #             writer.writeheader()
        #             print("dddd", rdr.readlines())
        #         wtr.close()
        #     else:
        #         with open(self.mainscreen_object.get_file_name() + ".csv", 'r+', newline="") as wtr:
        #             writer = csv.DictWriter(wtr, fieldnames=self.fieldnames)
        #             reader = csv.DictReader(wtr)
        #             print("rowwwww: ", wtr.readline())
                    
                



if __name__ == "__main__":
    WidgetManager()