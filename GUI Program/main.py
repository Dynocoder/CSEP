import window as w
import portcom as pc


arduino_baudrate = 9600


arduino = pc.PortCom()
windowobj = w.window("Temperature GUI")

main_frame = w.mainScreen(windowobj.window, serial=arduino)


# Wait Until the Information screen has been submitted
while main_frame.getBtnText() == "Connect":
    windowobj.window.update()
    # print(main_frame.getBtnText())
    

# wait until the port is initialized, and the window is still open.
while arduino.getInitializedStatus() == False and windowobj.window.state == "normal":
    # print(arduino.getInitializedStatus())
    windowobj.window.update()

# if arduino.setup:
datawidget = w.dataWidget(windowobj.window, "Temperature Sensor", arduino=arduino, file_name = main_frame.getFileName(), delaySeconds=5)

windowobj.window.mainloop()