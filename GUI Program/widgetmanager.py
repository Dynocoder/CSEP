import tkinter as tk
import datawidget as dw
from tkinter import ttk
import displaygui


class WidgetManager():

    def __init__(self, root, widget_frame, arduino):
        self.window = root
        self.widget_frame = widget_frame
        self.arduino = arduino
        self.widgets = ["Temperature", "pH", "Load Cell"]
        self.delay = [1, 5, 10, 15, 30, 45, 60, 90, 120]
        self.children = self.window.winfo_children()
        self.arduino = arduino

        self.display = displaygui.DisplayGUI(self.window)

        # print("b:",self.children[0].grid_forget, "type: ", type(self.children[0]))

        print(self.window.children)


        # Widget Manager Tab
        self.widget_manager = tk.LabelFrame(self.window, text="Widget Manager", padx=5, pady=5, width=30)


        self.menu_text = tk.Label(self.widget_manager, text="Select Widget:", padx=5, pady=5)
        self.delay_text = tk.Label(self.widget_manager, text="Select Delay (in seconds): ", padx=5, pady=5)


        self.swidget = tk.StringVar(self.widget_manager)
        self.swidget.set(self.widgets[0])
        # Widget Type Menu
        self.widget_menu = tk.OptionMenu(self.widget_manager, self.swidget, *self.widgets)

        # Delay Menu
        self.sdelay = tk.StringVar(self.widget_manager)
        self.sdelay.set(self.delay[1])
        self.delay_menu = tk.OptionMenu(self.widget_manager, self.sdelay, *self.delay)

        self.add_widget = tk.Button(self.widget_manager, text="Add", padx=5, pady=5, command=self.add)
        self.remove_widget = tk.Button(self.widget_manager, text="Remove", padx=5, pady=5, command=self.remove)

        self.separator = ttk.Separator(self.widget_manager, orient="vertical")

        self.start_stream = tk.Button(self.widget_manager, text="Start", padx=5, pady=5, command=self.start)
        self.stop_stream = tk.Button(self.widget_manager, text="Stop", padx=5, pady=5, command=self.stop)

        self.start_saving = tk.Checkbutton(self.widget_manager, text="Start Saving", padx=5, pady=5)


        


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
        self.start_saving.grid(row=1, column=3, columnspan=2, padx=15)


    def add(self):

        self.display.addFrame("T")
        self.widget_type = self.swidget.get()
        print(self.display.frames)

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
        #             dd = dw.DataWidget(self.widget_frame, "pH", self.arduino, "data.csv", 4, self.row, self.column)
        #         case "Load Cell":
        #             dd = dw.DataWidget(self.widget_frame, "Load Cell", self.arduino, "data.csv", 4, self.row, self.column)
                    
            

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
        self.getData()

    def stop(self):
        pass

    def saveToFile(self):
        pass



    def getData(self):
        """
        The Function uses the arduino object and reads the data from the serial port using the portcom module.

        """
        # if the arduino is connected
        if self.arduino.getInitializedStatus():
            # Continue to get the data until the user has not pressed stop.
            # if self.start_stream['text'] == "Stop":
            self.val = self.arduino.ask_read("t")
            

            # self.updateGUI(value=self.val)
            print(self.val)
            self.display.updateFrame(self.val)
            
            # if the user wants to save the data
            # if self.saveToFile():
            #     self.save_data_csv(self.val)
            self.display.frames[self.display.frameCount-1].update()
            print("***")
            delay = (int)(self.sdelay.get())
            self.display.frames[self.display.frameCount-1].after(delay*1000, self.getData)
            # else:
            #     return
        else:
            tk.messagebox.showerror('Port Disconnected', 'Error: Port Disconnected. Can not read Value')
            return
        
    



        



if __name__ == "__main__":
    WidgetManager()