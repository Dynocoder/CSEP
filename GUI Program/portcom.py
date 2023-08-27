"""
The Portcom object, contains methods to communicate with the serial port.
"""

import serial
import serial.tools.list_ports
import csv
import os
import re
import tkinter as tk
import time


class PortCom:
    def __init__(self) -> None:
        self.initialized = False
        self.read = False
        self.arduino = None
        self.baudrate = 9600
        # Channel array
        self.channels = ["c100", "c200", "c300", "c400"]
        # System dictionary with their associated commands.
        self.systems = {"Temperature": "t0", "Load Cell": "l0", "Load Cell Calibrate": "lc"}


    def allocatePort(self, selected_port):
        port = selected_port
        baud = 9600
        print(port)
        
        try:
            #NOTE: timeout = None (will wait until reads a value)
            self.arduino = serial.Serial(port=port, baudrate=baud, timeout=None)
            print("Port Initialized")
            self.initialized = True
            
            
            return True
        except Exception as e:
            self.initialized = False
            print("Error")
            # tk.messagebox.showerror('Port Disconnected', 'Error: Could not connect to port')
            tk.messagebox.showerror('Port Not Connected', e)

    def closePort(self):
        try:
            self.arduino.close()
            self.initialized = False
            return True
        except:
            print("Could Not Close Port")
            return False

    """
    @param command - char type input that is sent to arduino to read readings.

    the function takes in a command (type: char), the command needs to be programmed on the arduino side.
    the function passes that command through the serial port to the arduino, then, the arduino returns a string
    readings to the serial port which is then collected and returned.
    """
    def ask_read(self):

        if (self.arduino.in_waiting > 0):
            self.arduino.reset_input_buffer()
            com = (str)(self.channels)
            self.arduino.write(com.encode("utf-8"))
            print(com.encode("utf-8"))
            # print("Waiting......")
            self.readings = self.arduino.readline()
            # send the command through the com port

            print("received: ", self.readings.decode("utf-8"))

        return 0
    

    def read_thread(self, widget_manager, displaygui):
        """Read the serial port"""

        while self.read:
            self.arduino.reset_input_buffer()
            com = (str)(self.channels)
            self.arduino.write(com.encode())
            response = self.arduino.readline()

            # printing values TESTING
            print(com)
            print(response)
            print(response.decode().rstrip().rsplit(", "))


            # Updating the GUI
            self.response_list = response.decode().rstrip().rsplit(", ")
            displaygui.updateFrameData(self.response_list, int(widget_manager.sdelay.get()))

            # writing the data to the file
            if widget_manager.save_data.get():
                # print(widget_manager.save_data.get())
                widget_manager.save_to_file(self.response_list, 0)

            time.sleep(int(widget_manager.sdelay.get()))
        
        

    """
    sets up the channels array to pass to the arduino 
    """
    def set_channel(self, channel, command):
        self.channels[channel-1] = f"c{channel}{command}"
    
    '''
    @return boolean - returns true if arduino is connected, false otherwise.
    '''
    def getPortStatus(self):
        return self.initialized

    def setRead(self, read):
        self.read = read


    def save_data_csv(self, readings, file_path):

        # self.check_data_file()

        # file_path = "data.csv"

        # Read the Last time readings
        with open(file_path, 'r') as read:
            reader = csv.DictReader(read)
            reader_list = list(reader)
            fields = reader.fieldnames

            # If the File is newly Created 
            if len(reader_list) > 0:
                last_time = reader_list[-1]
                new_time = int(last_time[fields[0]]) + 1
            else:
                new_time = 0

        read.close()

        # Write the data in the csv file with a time increment of 1 second
        with open(file_path, 'a', newline='\n') as write:
            writer = csv.DictWriter(write, fieldnames=fields)
            writer.writerow({fields[0]: new_time, fields[1]: readings})

        write.close()
        
    def check_data_file(self):

        file_path = 'data.csv'
        field_names = ["time", "readings"]

        # Checks whether the file exists or not.
        try:
            with open(file_path, 'r') as rdr:
                reader = csv.reader(rdr)
                if any(reader):
                    rdr.close()
                    os.remove(file_path)
                    self.check_data_file()
        except FileNotFoundError or FileExistsError:
            with open(file_path, 'w', newline='') as wtr:
                write = csv.DictWriter(wtr, fieldnames=field_names)
                write.writeheader()
            wtr.close()
    

if __name__ == "__main__":
    PortCom()