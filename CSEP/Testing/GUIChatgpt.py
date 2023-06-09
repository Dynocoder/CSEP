import tkinter as tk
import serial
import serial.tools.list_ports

# Listing all the serial ports on the computer
ports_list = list(serial.tools.list_ports.comports())
com_list = [port.description for port in ports_list]

# Tkinter window object creation
window = tk.Tk()
window.geometry("800x600")
window.title("pH Meter")

error_label = tk.Label(window)
error_label.pack()

# Initializes the serial port
def initialize_port(port):
    try:
        error_label.config(text="Configuring Port...")
        arduino = serial.Serial(port, baudrate=115200, timeout=1)
        error_label.config(text="Port configured")
        return arduino
    except serial.SerialException:
        error_label.config(text="Error: Could not set port")
    except OSError:
        error_label.config(text="Error: Select the correct board")

# The chosen (actual Arduino port) port is passed to initialize_port() to initialize the port
def select_port(port):
    for cport in ports_list:
        if cport.description == port:
            arduino_port = cport.device
            error_label.config(text="Configuring port, please wait...")
            return initialize_port(arduino_port)

# Accept the input from the drop-down menu
def choose_arduino(event):
    serial_port = event
    arduino = select_port(serial_port)
    if arduino is not None:
        port_label.config(text=serial_port)
        # Start reading data from the Arduino using arduino.readline()

# Dropdown menu to choose Arduino com port
selected_option = tk.StringVar(window)
selected_option.set("Select Port")
port_menu = tk.OptionMenu(window, selected_option, *com_list, command=choose_arduino)
port_menu.pack()

# Displaying the selected com port
port_label = tk.Label(window)
port_label.pack()

window.mainloop()
