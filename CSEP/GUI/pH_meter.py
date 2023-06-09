import tkinter as tk
import serial
import csv
import time


app = tk.Tk()

app.geometry("400x400")
app.title("pH Meter")

# ******* Arduino Setup *******
arduino_port = 'COM5'
arduino_baudrate = 115200
arduino = serial.Serial(arduino_port, arduino_baudrate)



# Save the Value in a CSV file
def save_data(value):
    with open("data\data.csv", 'a') as data_file:
        csv_wtr = csv.writer(data_file)

        csv_wtr.writerow(value)
    
    data_file.close()
    
    


# Read Value from Serial port
def read_value():
    while arduino.in_waiting == 0:
        pass

    # Flushing out all the values stored in the buffer.
    arduino.reset_input_buffer()

    # Reading the most recent value in the buffer.
    value = arduino.readline()
    value = value.decode("utf-8")
    value = value.rstrip().strip()


    save_data(value)
    print(value)
    # print(value.encode())
    return value


# Update the GUI with the value received (Near realtime)
def update_gui():
    value = read_value()
    value_label.config(text=value)
    app.update()
    app.after(1000, update_gui)

value_label = tk.Label(app)
value_label.pack(padx=20, pady=20)


update_gui()

# Tkinter main event loop
app.mainloop()