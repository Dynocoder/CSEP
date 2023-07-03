import window as w
import portcom as pc

windowobj = w.window("300x200", "Temperature Sensor")

arduino = pc.portcom("com5", 9600)





windowobj.window.mainloop()