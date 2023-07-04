import serial
import serial.tools.list_ports

class PortCom:
    def __init__(self) -> None:
        pass


    def allocatePort(self, ComGUI):
        port = ComGUI.selected_port.get()
        baud = 9600
        try:
            self.arduino = serial.Serial(port, baud)
            self.arduino.timeout = 0.1
            print("done")
            
            return True
        except:
            print("Error")

    def closePort(self):
        self.arduino.close()

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


    

if __name__ == "__main__":
    PortCom()