import serial
import serial.tools.list_ports

class portcom:
    def __init__(self, port, baudrate) -> None:
        self.port = port
        self.baudrate = baudrate
        self.com = serial.Serial(port, baudrate)
        self.portlist = serial.tools.list_ports
    

    """
    @param command - char type input that is sent to arduino to read value.

    the function takes in a command (type: char), the command needs to be programmed on the arduino side.
    the function passes that command through the serial port to the arduino, then, the arduino returns a string
    value to the serial port which is then collected and returned.
    """
    def ask_read(self, command):
        # send the command through the com port
        self.com.write(command.encode())
        self.com.reset_input_buffer()
        self.value = self.com.readline()
        self.value = self.value.decode("utf-8")
        self.value = self.value.rstrip().strip()
        return self.value


    

if __name__ == "__main__":
    portcom()