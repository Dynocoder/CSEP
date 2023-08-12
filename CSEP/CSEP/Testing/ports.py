import serial
import serial.tools.list_ports


s = serial.Serial

# the serial.tools.list_ports.comports() function returns a list of all the COM ports in the pc
# Tested for Windows.
ports = serial.tools.list_ports.comports()

for port in ports:

    print(port.description)
