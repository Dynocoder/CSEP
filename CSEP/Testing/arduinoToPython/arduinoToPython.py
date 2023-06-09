"""
This is a basic program that will take input from the Serial port the arduino is 
connected to and will print that on the CLI.

GOAL: data from arduino to the python code.


"""

import time
import serial

arduino = serial.Serial('com5', 115200)

# sleep used to let the port configuration happen. Sometimes the code will break due to no delay.
time.sleep(1)

while True:
    while arduino.in_waiting == 0:
        pass
    arduinoData = arduino.readline()
    # the string is decoded in order to skip the escape letters ("\r", "\n") added by the arduino.
    arduinoData = str(arduinoData, 'utf-8')
    print(arduinoData)
