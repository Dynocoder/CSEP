import serial
import time

arduino = serial.Serial('COM6', 9600)


command = "['c1t0', 'c200', 'c300', 'c400']"

while True:
    arduino.write(command.encode())

    reading = arduino.readline()

    print(reading)
    time.sleep(1)

