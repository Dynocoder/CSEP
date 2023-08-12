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

        self.values.append([0])
        self.times.append([0])

    def AddGraph(self):
        '''
            This method will add setup the figure and the plot that will be used later on
            All the data will be inside the list to get an easier access later on
        '''
        # Setting up the plot for the each Frame
        self.figs.append([])
        # Initialize figures
        self.figs[self.frameCount-1].append(plt.Figure(figsize=(6, 4), dpi=80))
        # Initialize the plot
        self.figs[self.frameCount-1].append(
            self.figs[self.frameCount-1][0].add_subplot(111))
        # Initialize the chart
        self.figs[self.frameCount-1].append(FigureCanvasTkAgg(
            self.figs[self.frameCount-1][0], master=self.frames[self.frameCount-1]))

        self.figs[self.frameCount-1][2].get_tk_widget().grid(
            column=2, row=0, columnspan=4, rowspan=17,  sticky="n")
        
        print(self.figs)

    def updateFrame(self, value):
        # self.valueLabel[self.frameCount-1].config(text=value)
        self.figs[self.frameCount-1][1].plot(self.times[self.frameCount-1], self.values[self.frameCount-1], color='black')
        # # self.figs([self.frameCount-1][1].canvas.draw())
        # self.figs[self.frameCount-1][0].canvas.draw()
        print(self.figs[self.frameCount-1][0])
        self.updateGUI(value)
        # self.updateGUI(value)

    def updateFrames(self):
        while True:
            self.port_manager.ask_read()
            time.sleep(1)


    # def 

    def updateGUI(self, value):

        # Updating the data on the GUI
        self.valueLabel[self.frameCount-1].config(text=value)

        # Updating the Graph without csv
        # Increment by time 1 second 
        if len(self.times[self.frameCount-1]) > 0:
            self.times[self.frameCount-1].append(self.times[self.frameCount-1][-1]+1)
        else:
            self.times[self.frameCount-1].append([0])
        self.values[self.frameCount-1].append(float(value))

        # print("Time: ", time)
        print("Value: ", value)
        
        # Plotting the lists on the graph
        # plt.xlim(10)
        plt.xscale('linear')
        # self.graph_plot.plot(self.times[self.frameCount-1], self.values[self.frameCount-1], color='black')
        # self.AddGraph()

        # Drawing the canvas again
        # self.graph_canvas.draw()
        self.figs[self.frameCount-1][0].canvas.draw()

        print(self.values[self.frameCount-1])
        print(self.times[self.frameCount-1])

if __name__ == "__main__":
    DisplayGUI()