import serial
import serial.tools.list_ports

class portcom:
    def __init__(self, port, baudrate) -> None:
        self.port = port
        self.baudrate = baudrate
        self.com = serial.Serial(port, baudrate)
        self.portlist = serial.tools.list_ports
    
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