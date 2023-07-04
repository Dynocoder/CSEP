import serial

arduino = serial.Serial('com6', 9600)

def readVal():
    arduino.reset_input_buffer()

    data = arduino.readline()
    data = data.decode("utf-8")
    data = data.rstrip().strip()
    return data
    


while True:

    cmd = input("Enter Command: ")
    # encoding the string to utf-8.
    arduino.write(cmd.encode())
    print(readVal())
    
