"""
The main data display object, creates the channel frame, with the graph and label in it.
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import time

class DisplayGUI():
    def __init__(self, root, port_manager) -> None:
        self.root = root
        self.port_manager = port_manager
        self.fontsize = 16

        # Array of frames in the root window
        self.frames = []

        # Frame positioning
        self.frameRow = 3
        self.frameColumn = 0

        # Number of frames in the row
        self.frameCount = 0

        # Array of figs(graph figures), value labels for the frames. indexed respective to the index of frames.
        # follows [[Matplotlib_figure, Matplotlib_subplot, Matplotlib_tkinter_object]] structure.
        self.figs = []
        self.valueLabel = []

        # Times and values for the graphs
        self.times=[]
        self.values=[]

    def addFrame(self, frameName):
        '''
            Adds the frame to the root
        '''
        if self.frameCount < 4:
            self.frames.append(tk.LabelFrame(self.root, text=frameName, padx=5, pady=5))
            self.frameCount = len(self.frames)

            # Frame Placement
            if self.frameCount % 2 == 0:
                self.frameColumn = 5
            else:
                self.frameColumn = 0
            

            self.frameRow = 5 + 5 * int((len(self.frames)-1)/2)

            

            self.frames[self.frameCount-1].grid(row=self.frameRow, column=self.frameColumn, rowspan=4, columnspan=4)
            # tk.Label(self.frames[0], text="DFDS:K", padx=5, pady=5).grid(row=0, column=0)
            # self.datawidget(self.frames[self.frameCount-1])

            self.AddGraph()

            self.addValueLabel()

            # self.values.append([])

            # value_text = tk.Label(self.frames[self.frameCount-1], text="Value: ", padx=25, pady=5, font=('Arial', self.fontsize)).grid(row=0, column=0)
            # self.value = tk.Label(self.frames[self.frameCount-1], padx=25, pady=5, font=('Arial', self.fontsize)).grid(row=1, column=0)

    """
    Remove the last frame in the list of frames
    """
    def removeFrame(self):
        # Remove from grid view
        self.frames[self.frameCount-1].grid_remove()
        # Remove from list of frames
        self.frames.pop()
        # Remove the graphs and labels from the list of frames
        self.figs.pop()
        self.valueLabel.pop()
        self.values.pop()
        self.times.pop()
        # reset the channels in the port_manager object.
        self.port_manager.channels[self.frameCount-1] = f"c{self.frameCount}00"
        # reset the number of frames currently in the list.
        self.frameCount = len(self.frames)

        print(self.port_manager.channels)

    """
    Adds a Value label to the frame.
    """
    def addValueLabel(self):
        self.valueLabel.append(tk.Label(self.frames[self.frameCount-1], text="Value: ", padx=25, pady=5, font=('Arial', self.fontsize)))

        self.valueLabel[self.frameCount-1].grid(row=0, column = 0)

        self.values.append([])
        self.times.append([])

    def AddGraph(self):
        '''
            This method will add setup the figure and the plot that will be used later on
            All the data will be inside the list to get an easier access later on
        '''
        # Setting up the plot for the each Frame
        self.figs.append([])
        print("figs list ", self.figs)
        # Initialize figures
        self.figs[self.frameCount-1].append(
            plt.Figure(figsize=(6, 4), dpi=80))
        print("figs ", self.figs[self.frameCount-1])
        # Initialize the plot
        self.figs[self.frameCount-1].append(
            self.figs[self.frameCount-1][0].add_subplot(111))
        print("figs with subplot ", self.figs[self.frameCount-1])
        # Initialize the chart
        self.figs[self.frameCount-1].append(FigureCanvasTkAgg(
            self.figs[self.frameCount-1][0], master=self.frames[self.frameCount-1]))
        print("figs after canvas tkagg", self.figs[self.frameCount-1])
        self.figs[self.frameCount-1][2].get_tk_widget().grid(
            column=2, row=0, columnspan=4, rowspan=17,  sticky="n")
        
        print("fig after all operations" , self.figs)

    def updateFrameData(self, value, time_delay):
        # updating the values list
        print(len(self.values))

        save_data_list = []

        
        for i in range(len(self.values)):
            print(float(value[i]))
            try:
                # appending the value to the respective list in values lists
                self.values[i].append(float(value[i]))
                # save_data_list.append(value[i])

                # appending time values
                if len(self.times[i]) == 0:
                    self.times[i].append(0)
                else:
                    self.times[i].append(self.times[i][-1]+time_delay)
            except:
                pass
        
        self.updateGUI()
        
        print(self.values)
        print(self.times)

        return 

    def updateGUI(self):

        for i in range(self.frameCount):
            # Updating the data on the Label
            self.valueLabel[i].config(text=self.values[i][-1])

            # Updating the graph
            # access the graph individually
            # access the data for that graph from self.values and self.times
            # Access the Matplotlib_subplot from the figs list.
            self.figs[i][1].plot(self.times[i], self.values[i])
            
            # re-draw it with the self.values and self.times list 
            plt.xlim(10)
            plt.ylim(10)
            plt.xscale('linear')
            plt.yscale('linear')
            self.figs[i][2].draw()

if __name__ == "__main__":
    DisplayGUI()