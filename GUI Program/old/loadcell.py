import serial
import time

arduino = serial.Serial('COM5', 9600)


command = "['c1t0', 'c200', 'c300', 'c400']"
lread = 'r'


# print(arduino.out_waiting)
arduino.write(lread.encode())

# arduino.w
# while (arduino.in_waiting <= 0):
#     # print("in_waiting bytes: ", arduino.in_waiting)
#     # print("out_waiting bytes: ", arduino.out_waiting)
#     pass

print(arduino.read())
# time.sleep(1)
arduino.close()

