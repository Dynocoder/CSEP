import window as w
import mainScreen as ms
import datawidget as dw
import portcom as pc


arduino_baudrate = 9600

print()

arduino = pc.PortCom()
windowobj = w.Window()



main_frame = ms.MainScreen(windowobj.window, serial=arduino)



# # Wait Until the Information screen has been submitted
# while main_frame.getBtnText() == "Connect":
#     windowobj.window.update()
#     # print(main_frame.getBtnText())
    

# wait until the port is initialized, and the window is still open.
# while arduino.getInitializedStatus() == False and windowobj.window.state == "normal":
#     # print(arduino.getInitializedStatus())
#     windowobj.window.update()

# if arduino.setup:
# datawidget = dw.DataWidget(windowobj.window, "Temperature Sensor", arduino=arduino, file_name = main_frame.getFileName(), delaySeconds=5)

windowobj.window.mainloop()