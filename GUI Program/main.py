import window as w
import portcom as pc

windowobj = w.window("200x200", "tt")

main_frame = w.mainScreen(windowobj.window)

arduinoport = main_frame.get_selected_port()
arduino = pc.portcom(arduinoport, 9600)




# arduino = pc.portcom("com5", 9600)





windowobj.window.mainloop()