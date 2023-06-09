import tkinter as tk
import serial
import threading
import csv
import time

def update_label():
    if ser.is_open:
        # Read data from the serial port
        data = ser.readline().decode().strip()
        
        # Update the label with the received data
        label.config(text=data)

        window.update()
        window.update_idletasks()
        
        # Write data to CSV file
        write_data_to_csv(data)
    
    # Schedule the next update after 1 second
    label.after(1000, update_label)

def write_data_to_csv(data):
    elapsed_time = time.time() - start_time
    
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([elapsed_time, data])

def close_serial():
    ser.close()
    window.destroy()

# Create a serial port object
ser = serial.Serial('COM5', 115200)  # Replace 'COM1' with your serial port and '9600' with the baud rate

# Create the main window
window = tk.Tk()
window.title("Serial Data GUI")

# Create the label
label = tk.Label(window, text="Waiting for data...")
label.pack(pady=10)

# Initialize the start time
start_time = time.time()

# Start updating the label
update_label()

# Bind a function to handle window closing
window.protocol("WM_DELETE_WINDOW", close_serial)

# Start a separate thread for reading data from the serial port
thread = threading.Thread(target=update_label)
thread.daemon = True
thread.start()

# Start the main event loop
window.mainloop()
