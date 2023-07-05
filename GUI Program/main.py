import window as w
import portcom as pc


arduino_baudrate = 9600


arduino = pc.PortCom()
windowobj = w.window("Temperature GUI")

main_frame = w.mainScreen(windowobj.window, arduino)

# wait until the port is initialized, and the window is still open.
while arduino.getInitializedStatus() == False and windowobj.window.state == "normal":
    # print(arduino.getInitializedStatus())
    windowobj.window.update()

# print("DONEEEEEEEEEEEEEEEEEEEEEE")



# if arduino.setup:
datawidget = w.dataWidget(windowobj.window, "Temperature Sensor", arduino=arduino)

windowobj.window.mainloop()