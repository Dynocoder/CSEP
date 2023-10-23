import window as w
import main_screen as ms
import portcom as pc
import widgetmanager as wm

title = "Load Cell"
port_manager = pc.PortCom()
window_obj = w.Window(title=title)

main_frame = ms.MainScreen(window_obj.window, serial=port_manager, save_file = False)
widget_manager = None
def connect():
    main_frame.connect()
    widget_manager = wm.WidgetManager(window_obj.window, port_manager=port_manager, minimal=True)
    widget_manager.add("Load Cell")



main_frame.connectbtn.bind("<ButtonRelease-1>", lambda x: connect())

window_obj.window.mainloop()