"""Not in Use anymore"""

import tkinter as tk
import portcom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import csv
import os
import tkinter as tk
from window import Window



class DataWidget(Window):

    '''
    @param root - tkinter main window object.
    @param title (String) - title of the widget.
    @param arduino - The initialized com port where arduino is connected.
    @param datafile_path - the path of the data file where the data has to be saved.
    '''

    def __init__(self, root, title, arduino, file_name, delaySeconds, row, column) -> None:
        Window.__init__(self)
        self.title = title
        self.window = root
        self.arduino = arduino
        self.delaySeconds = delaySeconds
        self.fontsize = 16
        self.file_name = file_name
        self.row = row
        self.column = column
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
        self.dataWidget.grid(row=self.row, column=self.column, sticky="nsew")
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
                    self.save_data_csv(self.val)
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


    def save_data_csv(self, value):
        file_path = self.file_name + ".csv"
        # Read the Last time value
        with open(file_path, 'r') as read:
            reader = csv.DictReader(read)
            reader_list = list(reader)
            fields = reader.fieldnames

            # If the File is newly Created 
            if len(reader_list) >= 1:
                print(reader_list[-1][fields[0]])
                last_time = reader_list[-1]
                new_time = int(last_time[fields[0]]) + self.delaySeconds
            else:
                new_time = 0

        read.close()

        # Write the data in the csv file with a time increment of 1 second
        with open(file_path, 'a', newline='') as write:
            writer = csv.DictWriter(write, fieldnames=fields)
            writer.writerow({fields[0]: new_time, fields[1]: value})

        write.close()


if __name__ == "__main__":
    DataWidget()