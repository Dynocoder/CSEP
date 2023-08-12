import window as w
import mainScreen as ms
import datawidget as dw
import portcom as pc


arduino_baudrate = 9600

print()

port_manager = pc.PortCom()
windowobj = w.Window()



main_frame = ms.MainScreen(windowobj.window, serial=port_manager)



# # Wait Until the Information screen has been submitted
# while main_frame.getBtnText() == "Connect":
#     windowobj.window.update()
#     # print(main_frame.getBtnText())
    

# wait until the port is initialized, and the window is still open.
# while port_manager.getInitializedStatus() == False and windowobj.window.state == "normal":
#     # print(port_manager.getInitializedStatus())
#     windowobj.window.update()

# if port_manager.setup:
# datawidget = dw.DataWidget(windowobj.window, "Temperature Sensor", port_manager=port_manager, file_name = main_frame.getFileName(), delaySeconds=5)

windowobj.window.mainloop()