import tkinter as tk
import serial.tools.list_ports

class DropDownMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("COM Port Selector")

        self.com_ports = self.get_com_ports()
        self.selected_port = tk.StringVar(value=self.com_ports[0] if self.com_ports else "")

        self.create_widgets()

    def get_com_ports(self):
        com_ports = [port.device for port in serial.tools.list_ports.comports()]
        return com_ports

    def create_widgets(self):
        label = tk.Label(self, text="Select COM Port:")
        label.pack()

        dropdown = tk.OptionMenu(self, self.selected_port, *self.com_ports)
        dropdown.pack()

if __name__ == '__main__':
    app = DropDownMenu()
    app.mainloop()
