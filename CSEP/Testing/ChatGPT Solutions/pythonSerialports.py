import tkinter as tk
import serial.tools.list_ports

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        port_list.append((port.device, port.description))
    return port_list

def on_select(event):
    selected_value = event.widget.get()
    selected_port, selected_device = selected_value.split(' (', 1)
    selected_device = selected_device[:-1]  # Remove the closing parenthesis
    print(f"Selected Port: {selected_port}")
    print(f"Selected Device: {selected_device}")

# Create the main window
window = tk.Tk()

# Set the window dimensions
window.geometry("800x600")

# Create the dropdown menu
serial_ports = get_serial_ports()
device_dict = dict(serial_ports)
selected_value = tk.StringVar(window)
selected_value.set(f"{serial_ports[0][0]} ({serial_ports[0][1]})")  # Set default port and device
port_menu = tk.OptionMenu(window, selected_value, *[f"{port[0]} ({port[1]})" for port in serial_ports], command=on_select)
port_menu.pack(pady=20)

# Start the GUI event loop
window.mainloop()
