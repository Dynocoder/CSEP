# Author: Saurav Prashar
# Date: 06-06-2023

import tkinter as tk
import serial

win = tk.Tk()
win.geometry("500x500")
win.title("Realtime viewer")

# Port Setup for arduino
port = 'com5'
arduino = serial.Serial(port=port, baudrate=115200)

# value label
value_label = tk.Label(win)
value_label.pack(padx=20, pady=20)

def update_reading():
    data = arduino.readline()
    data = data.decode('utf-8')
    print(data)
    value_label.config(text=data)
    win.after(func=update_reading)


update_reading()