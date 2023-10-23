"""
The Portcom object, contains methods to communicate with the serial port.
"""

import serial
import serial.tools.list_ports
import csv
import os
import tkinter as tk
import time
import threading


class PortCom:
    def __init__(self) -> None:
        # Arduino serial port initialization state.
        self.initialized = False
        self.t1 = None
        # variable to control the reading thread.
        self.read = False
        # arduino serial port object. None until initialized.
        self.arduino = None
        # Arduino default baudrate value.
        self.baudrate = 9600
        # Channel array.
        self.channels = ["c100", "c200", "c300", "c400"]
        # ["c1t0", "c2l0", "c300", "c400"]
        # '[27.00, 100.00, 00, 00]'
        # System dictionary with their associated commands.
        self.systems = {"Temperature": "t0", "Load Cell": "l0", "pH": "p0"}

    
    def allocatePort(self, selected_port):
        """ 
        this module allocates the port to which the arduino is connected to (as selected by the user in the menu).
        """
        try:
            #NOTE: timeout = None (will wait until reads a value), therefore, there will be a slight delay as it will take some time for arduino to process and return the values.
            self.arduino = serial.Serial(port=selected_port, baudrate=self.baudrate, timeout=None)
            print("Port Initialized")
            self.initialized = True
            return True
        
        except Exception as e:
            self.initialized = False
            print("Error")
            tk.messagebox.showerror('Port Not Connected', e)

    
    def closePort(self):
        """ 
        Closes the arduino port.
        return
        True if successful, False otherwise
        """
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

    
    OLD READ METHOD ->

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
    """
    
    
    def read_thread(self, widget_manager, displaygui):
        """ 
        This module Reads the serial port for data. this should be called indefinitely 
        in a separate thread until the user cancels it.
        Module is called in a separate thread different from the main thread.
        """
        self.list_threads()
        # While the read status is True.
        while self.read:
            # Reset previous values from the buffer
            self.arduino.reset_input_buffer()
            # creating a command from the channels list(modified acc. to the channels added.)
            com = (str)(self.channels)
            self.arduino.write(com.encode())

            # Getting the response from the serial port
            response = self.arduino.readline()

            # Updating the GUI
            self.response_list = response.decode().rstrip().rsplit(", ")
            displaygui.updateFrameData(self.response_list, int(widget_manager.sdelay.get()))

            # writing the data to the file
            if widget_manager.save_data.get():
                # print(widget_manager.save_data.get())
                widget_manager.save_to_file(self.response_list, 0)

            time.sleep(int(widget_manager.sdelay.get()))


    def list_threads(self):
        """
        Function made for listing all the threads currently running as part of the program.
        """
        for thread in threading.enumerate():
            print(f"Thread name: {thread.name}")


    def set_channel(self, channel, command):
        """
        This module sets up the channels array to pass to the arduino as a command
        parameters:
        channel - the channel at which the particular sensor is attached to.
        command - the respective command for the sensor/system attached to that channel(the sensor/system is selected by the user).
        """
        # modifying the channels array to have the corresponding command for their respective sensor
        self.channels[channel-1] = f"c{channel}{command}"
    

    def getPortStatus(self):
        """
        This module returns the status of the arduino port.
        return 
        self.initialized(boolean) true if arduino is connected, false otherwise.
        """
        return self.initialized


    def setRead(self, read):
        """
        This module sets the value of the read boolean.
        parameter
        self.read(boolean) true if value is being read/required to be read, false otherwise.
        """
        self.read = read


'''
OLD FUNCTION to save the data to csv file.
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
'''

'''
OLD FUNCTION to check if the data file already exists or is a new/ empty file.
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
    
'''

if __name__ == "__main__":
    PortCom()