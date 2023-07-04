import tkinter as tk
import serial.tools.list_ports
import portcom as pc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 


class window():
    

    def __init__(self, res, title) -> None:
        self.window = tk.Tk()
        # self.window.geometry(res)
        self.window.title(title)
        
        self.window.update()
    
class mainScreen():

    '''
    @param window - the root window object in which the mainFrame is to be drawn
    @param serial - the portcom object to initialize arduino port.
    '''
    def __init__(self, window, serial) -> None:
        self.window = window
        self.arduino = serial
        self.mainlabel = tk.LabelFrame(self.window, text="Main Menu", padx=5, pady=5)
        self.text = tk.Label(self.mainlabel, text="Select a COM port: ", padx=5, pady=5)
        self.port_menu()
        self.connectbtn = tk.Button(self.mainlabel, text="Connect", command=self.connect)


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
        self.connectbtn.grid(row=0, column=2, padx=5, pady=5)

# get all the serial ports as a list.
    def get_serial_ports(self):
        self.ports = serial.tools.list_ports.comports()
        self.port_list = []
        for port in self.ports:
            self.port_list.append((port.device, port.description))
        return self.port_list
    
    def connect(self):
        # if self.connectbtn['text'] in "Connect":
        if self.arduino.allocatePort(self):
            self.connectbtn['text'] = "Disconnect"
            self.connectbtn['command'] = self.disconnect
            self.port_menu_widget['state'] = "disable"
    

    def disconnect(self):
        print("Disconnect pressed!")
        self.arduino.closePort()
        self.port_menu_widget['state'] = "active"
        self.connectbtn['text'] = "Connect"
        

class dataWidget():

    def __init__(self, root, title, arduino) -> None:
        self.title = title
        self.window = root
        self.arduino = arduino
        self.dataWidget = tk.LabelFrame(self.window, text=self.title, padx=5, pady=5)

        self.valueText = tk.Label(self.dataWidget, text="Value: ", padx=5, pady=5)
        self.readValue = tk.Label(self.dataWidget, padx=5, pady=5)

        self.startbtn = tk.Button(self.dataWidget, text="Start", command=self.startClick)



        # *********GRAPH MESS*****************
        graph_fig, graph_plot = plt.subplots()

        # Tkinter and Matplotlib interface
        self.graph_canvas = FigureCanvasTkAgg(graph_fig, master=self.dataWidget)
        self.graph_canvas.draw()

        # # Converts the canvas to a widget tkinter can work with
        # graph_canvas.get_tk_widget().pack()
        # *********GRAPH MESS ENDS*****************

        self.publish()

    '''
    Arranges the display widgets in the window.
    '''
    def publish(self):
        self.dataWidget.grid(row=1, column=0, sticky="news")
        self.valueText.grid(row=0, column=0)
        self.readValue.grid(row=0, column=1)
        self.graph_canvas.get_tk_widget().grid(row=0, column=2)
        self.startbtn.grid(row=1, column=0)
    
    def startClick(self):
        self.getData()

    def getData(self):
        self.val = self.arduino.ask_read("t")
        self.readValue.config(text=self.val)
        self.dataWidget.update()
        print("******************")
        self.dataWidget.after(5000, self.getData)
        


if __name__ == "__main__":
    window()
    mainScreen()
    dataWidget()
