import window as w
import portcom as pc


arduino_baudrate = 9600


arduino = pc.PortCom()
windowobj = w.window("200x200", "tt")

main_frame = w.mainScreen(windowobj.window, arduino)

datawidget = w.dataWidget(windowobj.window, "Temperature Sensor", arduino=arduino)


windowobj.window.mainloop()