import window as w
import main_screen as ms
import portcom as pc
import widgetmanager as wm
import threading

title = "Temperature Sensor"
port_manager = pc.PortCom()
window_obj = w.Window(title=title)

main_frame = ms.MainScreen(window_obj.window, serial=port_manager, save_file = False)



main_frame.connectbtn.bind("<ButtonRelease-1>", lambda x: connect())
window_obj.window.wm_protocol("WM_DELETE_WINDOW", lambda: close_program())




def connect():
    main_frame.connect()
    global widget_manager
    widget_manager = wm.WidgetManager(window_obj.window, port_manager=port_manager, minimal=True)
    widget_manager.add("Temperature")

def close_program():
    # calls the self.quit_program function when the window is closed using the cross.
    widget_manager.stop()
    window_obj.quit_program()


window_obj.window.mainloop()