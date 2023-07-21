import tkinter as tk
import tkinter.messagebox
import serial.tools.list_ports
from window import Window
import portcom
import csv

class MainScreen(Window):

    '''
    @param window - the root window object in which the mainFrame is to be drawn
    @param serial - the portcom object to initialize arduino port.
    '''
    def __init__(self, window, serial) -> None:
        self.window = window
        self.arduino_port = serial
        # self.arduino = pc.PortCom
        self.file_name = "data"
        self.mainlabel = tk.LabelFrame(self.window, text="Main Menu", padx=5, pady=5)
        self.text = tk.Label(self.mainlabel, text="Select a COM port: ", padx=5, pady=5)
        self.port_menu()
        self.connectbtn = tk.Button(self.mainlabel, text="Connect", command=self.connect, padx=5, pady=5)
        


        self.filelabel = tk.Label(self.mainlabel, text="Enter File Name: ", padx=5, pady=5)
        self.filetext = tk.Entry(self.mainlabel)
        self.filetext.insert(0, self.file_name)
        


        self.publish()
    



    """
    @param self
    return none

    self.port_menu_widget - the optionmenu object

    displays the port selection menu on the screen
    """
    def port_menu(self):
        # Port Selection Menu
        self.com_ports = self.get_serial_ports()
        self.selected_port = tk.StringVar(self.mainlabel)
        self.selected_port.set(f"{self.com_ports[0][0]}")  # Set default port
        self.port_menu_widget = tk.OptionMenu(self.mainlabel, self.selected_port, *[f"{port[0]}" for port in self.com_ports])
        

    '''
    Arranges the mainframes widgets in the window.
    '''
    def publish(self):
        self.mainlabel.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.text.grid(row=0, column=0)
        self.port_menu_widget.grid(row=0, column=1)
        self.connectbtn.grid(row=0, column=3)
        self.filelabel.grid(row=1, column=0)
        self.filetext.grid(row=1, column=1)

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
            # self.arduinooo = pc.allocatePort(self.arduino_port)
            print(type(self.arduino_port))


            # if the arduino port was successfully allocated
            if self.arduino_port.allocatePort(self):
                self.connectbtn['text'] = "Disconnect"
                self.connectbtn['command'] = self.disconnect
                self.port_menu_widget['state'] = "disable"
                self.filetext['state'] = "disable"
        
    # If the disconnect button is pressed
    def disconnect(self):
        print("Disconnect pressed!")
        if self.arduino.closePort():
            self.port_menu_widget['state'] = "active"
            self.connectbtn['text'] = "Connect"
            self.connectbtn['command'] = self.connect
            self.filetext['state'] = "normal"
        

    def createfile(self, filepath):
        # file_path = filepath
        print("create File: ", filepath)
        file_path = filepath + ".csv"
        field_names = ["time", "value"]

        # Checks whether the file exists or not. If it does, it removes it and calls the function again.
        try:
            with open(file_path, 'r') as rdr:
                reader = csv.reader(rdr)
                if any(reader):
                    rdr.close()
                    deleteCurrentFile = tk.messagebox.askokcancel(title="File Already Exists", message="Do you want to remove the file and create a new one?")
                    if deleteCurrentFile:
                        os.remove(file_path)
                        self.createfile(file_path=filepath)
                        return True
                    else:
                        return False
        except:
            with open(file_path, 'w', newline='') as wtr:
                write = csv.DictWriter(wtr, fieldnames=field_names)
                write.writeheader()
                return True
            wtr.close()
    
    def getFileName(self):
        return self.file_name
    
    def getBtnText(self):
        return self.connectbtn['text']
  
if __name__ == "__main__":
    MainScreen()

