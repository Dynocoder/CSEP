"""
MainScreen Object, creates the main port selection and file saving window, contains methods to create the saving file.
"""


import tkinter as tk
import tkinter.messagebox
import serial.tools.list_ports
from window import Window
import widgetmanager as wm
import portcom
import csv
import os

class MainScreen(Window):

    '''
    @param window - the root window object in which the mainFrame is to be drawn
    @param serial - the portcom object to initialize arduino port.
    '''
    def __init__(self, window, serial) -> None:
        self.window = window
        self.port_manager = serial
        # self.arduino = pc.PortCom
        self.file_name = "data"
        self.mainlabel = tk.LabelFrame(self.window, text="Main Menu", padx=5, pady=5, width=30)
        #dataWidget Label
        self.widget_label = tk.Frame(self.window,  padx=5, pady=5)
        self.text = tk.Label(self.mainlabel, text="Select a COM port: ", padx=5, pady=5)
        self.port_menu()
        self.connectbtn = tk.Button(self.mainlabel, text="Connect", command=self.connect, padx=5, pady=5)
        


        self.filelabel = tk.Label(self.mainlabel, text="Enter File Name: ", padx=5, pady=5)
        self.filetext = tk.Entry(self.mainlabel)
        self.filetext.insert(0, self.file_name)
        


        self.publish()
    

    '''
    Arranges the mainframes widgets in the window.
    '''
    def publish(self):
        self.mainlabel.grid(row=0, column=0, padx=5, pady=5, columnspan=3, rowspan=2, sticky="nsew")
        # Data Frame Widget Label
        self.widget_label.grid(row=3, column=0, columnspan=4)
        self.text.grid(row=0, column=0)
        self.port_menu_widget.grid(row=0, column=1)
        self.connectbtn.grid(row=0, column=3)
        self.filelabel.grid(row=1, column=0)
        self.filetext.grid(row=1, column=1)


    def port_menu(self):
        """
        @param self
        return none

        self.port_menu_widget - the optionmenu object

        displays the port selection menu on the screen
        """
        # Port Selection Menu
        self.com_ports = self.get_serial_ports()
        self.selected_port = tk.StringVar(self.mainlabel)
        try:
            self.selected_port.set(f"{self.com_ports[0][0]}")  # Set default port
            self.port_menu_widget = tk.OptionMenu(self.mainlabel, self.selected_port, *[f"{port[0]}" for port in self.com_ports])
        except Exception as e:
            self.selected_port.set("-")
            self.port_menu_widget = tk.OptionMenu(self.mainlabel, self.selected_port, *["-"])
        
    # get all the serial ports as a list.
    def get_serial_ports(self):
        self.ports = serial.tools.list_ports.comports()
        self.port_list = []
        for port in self.ports:
            self.port_list.append((port.device, port.description))
        return self.port_list
    
    # If the connect button is pressed
    def connect(self):
        self.file_name = self.filetext.get()
        print(len(self.file_name))
        print(self.file_name)

        # If the File is successfully created.
        if self.createfile(self.file_name):
            # Allocate the selected port as the arduino communication port
            self.port_manager.allocatePort(self.selected_port.get())


            # if the arduino port was successfully allocated
            if self.port_manager.getPortStatus():
                self.connectbtn['text'] = "Disconnect"
                self.connectbtn['command'] = self.disconnect
                self.port_menu_widget['state'] = "disable"
                self.filetext['state'] = "disable"
                self.wm = wm.WidgetManager(self.window, self.widget_label, self.port_manager, self)
        
    # If the disconnect button is pressed
    def disconnect(self):
        print("Disconnect pressed!")
        if self.port_manager.closePort():
            self.port_menu_widget['state'] = "active"
            self.connectbtn['text'] = "Connect"
            self.connectbtn['command'] = self.connect
            self.filetext['state'] = "normal"
        

    def createfile(self, filepath):
        # file_path = filepath
        print("create File: ", filepath)
        file_path = filepath + ".csv"
        field_names = ["time", "c1", "c2", "c3", "c4"]

        # Checks whether the file exists or not. If it does, it removes it and calls the function again.
        try:
            with open(file_path, 'r') as rdr:
                reader = csv.reader(rdr)
                if any(reader):
                    rdr.close()
                    deleteCurrentFile = tk.messagebox.askokcancel(title="File Already Exists", 
                                                                  message="Do you want to remove the file and create a new one?")
                    if deleteCurrentFile:
                        os.remove(file_path)
                        self.createfile(file_path=filepath)
                        return True
                    else:
                        return False
                else:
                    with open(file_path, 'w', newline='') as wtr:
                        return True
        except:
            with open(file_path, 'w', newline='') as wtr:
                
                return True
            wtr.close()
    
    def get_file_name(self):
        return self.file_name
    
    def getBtnText(self):
        return self.connectbtn['text']
  
if __name__ == "__main__":
    MainScreen()

