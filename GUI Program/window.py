import tkinter as tk
import serial.tools.list_ports
import portcom as pc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import csv
import os


class window():
    

    def __init__(self, title) -> None:
        self.window = tk.Tk()
        # self.window.geometry(res)
        self.window.title(title)
        self.window.wm_protocol("WM_DELETE_WINDOW", self.quit_me)
        self.window.update()
    
    def quit_me(self):
        print('quit')
        self.window.quit()
        self.window.destroy()
    
class mainScreen():

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
        self.createfile(self.file_name)


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
                    os.remove(file_path)
                    self.createfile(file_path=filepath)
        except FileNotFoundError or FileExistsError:
            with open(file_path, 'w', newline='') as wtr:
                write = csv.DictWriter(wtr, fieldnames=field_names)
                write.writeheader()
            wtr.close()
    
    def getFileName(self):
        return self.file_name
    
    def getBtnText(self):
        return self.connectbtn['text']



  
class dataWidget():

    '''
    @param root - tkinter main window object.
    @param title (String) - title of the widget.
    @param arduino - The initialized com port where arduino is connected.
    @param datafile_path - the path of the data file where the data has to be saved.
    '''

    def __init__(self, root, title, arduino, file_name, delaySeconds) -> None:
        self.title = title
        self.window = root
        self.arduino = arduino
        self.delaySeconds = delaySeconds
        self.fontsize = 16
        self.file_name = file_name
        self.times = []
        self.values = []


        self.dataWidget = tk.LabelFrame(self.window, text=self.title, padx=5, pady=5)

        self.valueWidget = tk.Frame(self.dataWidget, padx=5, pady=5)

        self.valueText = tk.Label(self.valueWidget, text="Value: ", padx=5, pady=5, font=('Arial', self.fontsize))
        self.readValue = tk.Label(self.valueWidget, padx=5, pady=5, font=('Arial', self.fontsize))

        self.startbtn = tk.Button(self.dataWidget, text="Start", command=self.startClick, font=('Arial', self.fontsize))
        
        self.save = tk.IntVar()
        self.start_saving = tk.Checkbutton(self.valueWidget, text="Start Saving", font=('Arial', self.fontsize), onvalue=1, offvalue=0, variable=self.save)

        
        # self.test_check = tk.Checkbutton(self.valueWidget, text="test", onvalue=1, offvalue=0, variable=self.test).grid(row=3, column=0)

        self.drawGraph()



        self.publish()

    # The Function returns True if the user has clicked the start saving checkbox.
    def saveToFile(self):
        if self.save.get():
            return True
        else:
            return False

    '''
    Arranges the display widgets in the window.
    '''
    def publish(self):
        self.dataWidget.grid(row=1, column=0, sticky="nsew")
        self.valueText.grid(row=0, column=0)
        self.readValue.grid(row=0, column=1)
        self.valueWidget.grid(row=0, column=0)
        self.graph_canvas.get_tk_widget().grid(row=0, column=2)
        self.startbtn.grid(row=1, column=0)
        self.start_saving.grid(row=1, column=0)


        self.dataWidget.grid_columnconfigure(0, weight=1, uniform='group1')
        self.dataWidget.grid_columnconfigure(1, weight=1, uniform='group1')
        self.dataWidget.grid_rowconfigure(0, weight=1)
    
    # Display the graph in the GUI
    def drawGraph(self):
        # *********GRAPH MESS*****************
        graph_fig, self.graph_plot = plt.subplots()
        plt.rcParams['figure.figsize'] = [4, 4]

        # Tkinter and Matplotlib interface
        self.graph_canvas = FigureCanvasTkAgg(graph_fig, master=self.dataWidget)
        self.graph_canvas.draw()

        # # Converts the canvas to a widget tkinter can work with
        # graph_canvas.get_tk_widget().pack()
        # *********GRAPH MESS ENDS*****************
    

    # The Function is called when the Start button is clicked. The Functions Calls the getDate method
    def startClick(self):
        # Converting the Start button to Stop Button
        self.startbtn['text'] = "Stop"
        self.startbtn['command'] = self.stopClick

        self.getData()
    

    # The Function is called when the Stop button is clicked.
    def stopClick(self):
        # Converting the Start button to Start Button
        self.startbtn['text'] = "Start"
        self.startbtn['command'] = self.startClick
        print("stop clicked")


    """
    The Function uses the arduino object and reads the data from the serial port using the portcom module.

    """
    def getData(self):
        # if the arduino is connected
        if self.arduino.getInitializedStatus():
            # Continue to get the data until the user has not pressed stop.
            if self.startbtn['text'] == "Stop":
                self.val = self.arduino.ask_read("t")
                


                self.updateGUI(value=self.val)
                


                # if the user wants to save the data
                if self.saveToFile():
                    pass
                self.dataWidget.update()
                print("***")
                self.dataWidget.after(self.delaySeconds*1000, self.getData)
            else:
                return
        else:
            tk.messagebox.showerror('Port Disconnected', 'Error: Port Disconnected. Can not read Value')
            return
    
    def updateGUI(self, value):
        # Updating the data on the GUI
        self.readValue.config(text=value)

        #Updating the Graph using a csv file
        # with open(self.file_name+".csv", 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if float(row['time']) % 1 == 0:
        #             self.times.append(row['time'])
        #             try:
        #                 self.values.append(float(row['value']))
        #             except:
        #                 self.values.append(self.values[-1])
        #         else:
        #             pass


        # Updating the Graph without csv
        # Increment by time 1 second 
        if len(self.times) > 0:
            self.times.append(self.times[-1]+1)
        else:
            self.times.append(0)
        self.values.append(float(value))

        # print("Time: ", time)
        print("Value: ", value)
        
        # Plotting the lists on the graph
        # plt.xlim(10)
        plt.xscale('linear')
        self.graph_plot.plot(self.times, self.values, color='black')

        # Drawing the canvas again
        self.graph_canvas.draw()


    


if __name__ == "__main__":
    window()
    mainScreen()
    dataWidget()
