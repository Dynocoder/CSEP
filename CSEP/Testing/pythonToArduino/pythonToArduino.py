import serial

arduino = serial.Serial('com5', 115200)

while True:

    cmd = input("Enter Command: ")
    # encoding the string to utf-8.
    arduino.write(cmd.encode())
