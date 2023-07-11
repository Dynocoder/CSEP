import serial
import serial.tools.list_ports
import csv
import os


class PortCom:
    def __init__(self) -> None:
        self.initialized = False
        self.arduino = None


    def allocatePort(self, ComGUI):
        port = ComGUI.selected_port.get()
        baud = 9600
        try:
            self.arduino = serial.Serial(port, baud)
            self.arduino.timeout = 0.1
            print("done")
            self.initialized = True
            
            return True
        except:
            print("Error")

    def closePort(self):
        try:
            self.arduino.close()
            self.initialized = False
            return True
        except:
            print("Could Not Close Port")
            return False

    """
    @param command - char type input that is sent to arduino to read value.

    the function takes in a command (type: char), the command needs to be programmed on the arduino side.
    the function passes that command through the serial port to the arduino, then, the arduino returns a string
    value to the serial port which is then collected and returned.
    """
    def ask_read(self, command):
        self.arduino.reset_input_buffer()
        # send the command through the com port
        self.arduino.write(command.encode())
        
        self.value = self.arduino.readline()
        self.value = self.value.decode("utf-8")
        self.value = self.value.rstrip().strip()

        return self.value
    
    '''
    @return boolean - returns true if arduino is connected, false otherwise.
    '''
    def getInitializedStatus(self):
        return self.initialized


    def save_data_csv(self, value, file_path):

        # self.check_data_file()

        # file_path = "data.csv"

        # Read the Last time value
        with open(file_path, 'r') as read:
            reader = csv.DictReader(read)
            reader_list = list(reader)
            fields = reader.fieldnames
            # print("fields", fields)
            # print(len(reader_list))

            # If the File is newly Created 
            if len(reader_list) > 0:
                # print("CSV List: ", reader_list)
                # print(reader_list[-1][fields[0]])
                last_time = reader_list[-1]
                new_time = int(last_time[fields[0]]) + 1
            else:
                new_time = 0

        read.close()

        # Write the data in the csv file with a time increment of 1 second
        with open(file_path, 'a', newline='\n') as write:
            writer = csv.DictWriter(write, fieldnames=fields)
            writer.writerow({fields[0]: new_time, fields[1]: value})

        write.close()
        
    def check_data_file(self):

        file_path = 'data.csv'
        field_names = ["time", "value"]

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