import serial

arduino = serial.Serial('com5', baudrate=115200)
def readdata():
    while arduino.in_waiting == 0:
        pass
    status = arduino.readline()
    # the string is decoded in order to skip the escape letters ("\r", "\n") added by the arduino.
    status = status.decode()
    print(status)
    # time.sleep(1)


i = 0
while i < 1000:
    readdata()
    i =i+ 1
