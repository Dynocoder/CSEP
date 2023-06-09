import tkinter as tk
import time
import serial
import serial.tools.list_ports

# listing all the serial ports on the computer
ports_list = serial.tools.list_ports.comports()
print(ports_list)
com_list = []
for port in ports_list:
    com_list.append(port.description)

global arduino

# tk window object creation.
window = tk.Tk()
window.geometry("400x400")
window.title("pH Meter")

error_label = tk.Label(window)
error_label.pack()


label = tk.Label(window)
label.pack()



def read_data(arduino):
    while arduino.in_waiting == 0:
        pass
    status = arduino.readline()
    # the string is decoded in order to skip the escape letters ("\r", "\n") added by the arduino.
    status = str(status, 'utf-8')
    print(status)
    return status


def update_label(arduino):
    status = read_data(arduino)
    value_label.config(text=f"Status: {status}")
    window.update()
    window.after(0, update_label(arduino))

# Initializes the serial port
def initialize_port(port):
    try:
        arduino = serial.Serial(port, baudrate=115200, timeout=3)
        error_label.config(text="Port configured successfully")
        print("Port is Configured....")
        update_label(arduino)
    
    except:
        # OSError - The serial library will give OSError when the correct board is not selected(don't experiment too much, will crash).
        # A message will be displayed if some other error happens.
        if OSError:
            error_label.config(text="OSError: Select the correct board")
        else:
            error_label.config(text="Could not set port")


# Accept the input from the drop down menu.
# The chosen port is passed to initialize_port() to intitialie the port
def choose_arduino(event):
    serial_port = event    
    for cport in ports_list:
        name = cport.description
        if cport.description == serial_port:
            if name.lower().startswith("arduino"):
                arduino_port  = cport.device
                initialize_port(arduino_port)
                # port_label.config(text=serial_port)


# Dropdown menu to chose arduino com port
selected_option = tk.StringVar(window)
selected_option.set("Select Port")
port_menu = tk.OptionMenu(window, selected_option,
                          *com_list, command=choose_arduino)
port_menu.pack()

 
# submit = tk.Button(window, text="Select", command=choose_arduino())
# submit.pack()

# testing - displaying the selected com port
port_label = tk.Label(window)
port_label.pack()


value_label = tk.Label(window, text="test")
value_label.pack(padx=12, pady=12)


# Start the main window.
window.mainloop()


