import tkinter as tk
import serial.tools.list_ports


class window:
    

    def __init__(self, res, title) -> None:
        self.window = tk.Tk()
        self.window.geometry(res)
        self.window.title(title)

        self.mainscreen()
    
    def mainscreen(self):
        self.com_ports = self.get_serial_ports
        

    def get_serial_ports(self):
        self.ports = serial.tools.list_ports.comports()
        self.port_list = []
        for port in self.ports:
            self.port_list.append((port.device, port.description))
        return self.port_list

if __name__ == "__main__":
    window()
