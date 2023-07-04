import tkinter as tk
import serial
from serial import Serial
import csv
import os
import time
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 


app = tk.Tk()

app.geometry("400x400")
app.title("pH Meter")

# ******* Arduino Setup *******
arduino_port = 'COM6'
arduino_baudrate = 9600
arduino = serial.Serial(arduino_port, arduino_baudrate)
arduino.timeout = 0.1
# a = serial.Serial("COM4", 115200)


"""
Checks whether the file exists or not.
deletes and creates a new one with the field names if a file already exists.
"""
def check_data_file():

    file_path = 'data.csv'
    field_names = ["time", "value"]

    # Checks whether the file exists or not.
    try:
        with open(file_path, 'r') as rdr:
            reader = csv.reader(rdr)
            if any(reader):
                rdr.close()
                os.remove(file_path)
                check_data_file()
    except FileNotFoundError or FileExistsError:
        with open(file_path, 'w', newline='') as wtr:
            write = csv.DictWriter(wtr, fieldnames=field_names)
            write.writeheader()
        wtr.close()



"""
Save the Value in a CSV file.

Arguments: 
value - the value to write in the csv
"""
def save_data_csv(value):

    file_path = "data.csv"

    # Read the Last time value
    with open(file_path, 'r') as read:
        reader = csv.DictReader(read)
        reader_list = list(reader)
        fields = reader.fieldnames

        # If the File is newly Created 
        if len(reader_list) >= 1:
            print(reader_list[-1][fields[0]])
            last_time = reader_list[-1]
            new_time = int(last_time[fields[0]]) + 1
        else:
            new_time = 0

    read.close()

    # Write the data in the csv file with a time increment of 1 second
    with open(file_path, 'a', newline='') as write:
        writer = csv.DictWriter(write, fieldnames=fields)
        writer.writerow({fields[0]: new_time, fields[1]: value})

    write.close()




"""
Updates the Graph 

Arguments:
canvas - the canvas object that is returned by FigureCanvasTkAgg() 
graph - the plot object returned by matplotlib.subplots()

Working:
the function fills two lists (times and values) reading from csv file

then the function creates a new plot and redraws the canvas.
"""
def update_graph(canvas, graph):

    times = []
    values = []

    # Appending the time and values in respective lists
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if float(row['time']) % 1 == 0:
                times.append(row['time'])
                try:
                    values.append(float(row['value']))
                except:
                    values.append(values[-1])
            else:
                pass




    # Plotting the lists on the graph
    # plt.xlim(10)
    plt.xscale('linear')
    graph.plot(times, values, color='black')

    # Drawing the canvas again
    canvas.draw()

    
    


"""
Read Value from Serial port

Working:
Waits until the arduino starts passing values.

Resets the input buffer to get the the current value.
""" 
def read_value():

    # Flushing out all the values stored in the buffer.
    arduino.reset_input_buffer()

    # Reading the most recent value in the buffer.
    value = arduino.readline()
    value = value.decode("utf-8")
    value = value.rstrip().strip()


    # Save the Data as a csv
    save_data_csv(value)

    # Update the graph
    # update_graph()

    print(value)
    return value


"""
Update the GUI with the value received (Near realtime)

Flow:
Read the value from the serial port.
update the value on the GUI
repeat after 1 second.
"""
def update_gui(canvas, graph):
    value = read_value()
    value_label.config(text=value)
    update_graph(canvas, graph)
    app.update()

    print("##################################################")
    

    app.after(5000, update_gui(canvas, graph))


# Value Label
value_label = tk.Label(app, font=('Arial', 20))
value_label.pack(padx=20, pady=20)


# ************* Graph *******************
graph_fig, graph_plot = plt.subplots()

# Tkinter and Matplotlib interface
graph_canvas = FigureCanvasTkAgg(graph_fig, master=app)
graph_canvas.draw()

# Converts the canvas to a widget tkinter can work with
graph_canvas.get_tk_widget().pack()


# # Clear input buffer from previous values.
# arduino.reset_input_buffer()


check_data_file()

# Waiting until the arduino has started to push data in the serial port
while arduino.in_waiting == 0:
    pass


update_gui(graph_canvas, graph_plot)

# Tkinter main event loop
app.mainloop()