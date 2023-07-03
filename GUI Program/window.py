import tkinter as tk
import serial.tools.list_ports


class window():
    

    def __init__(self, res, title) -> None:
        self.window = tk.Tk()
        # self.window.geometry(res)
        self.window.title(title)
        self.window.update()
    
class mainScreen():


    def __init__(self, window) -> None:
        self.selected_port = None
        self.window = window
        self.mainlabel = tk.LabelFrame(self.window, text="Main Menu", padx=5, pady=5)

        self.text = tk.Label(self.mainlabel, text="Select a COM port: ")

        self.port_menu()


        self.publish()



    """
    @param self
    return none

    displays the port selection menu on the screen
    """
    def port_menu(self):
        # Port Selection Menu
        self.com_ports = self.get_serial_ports()
        self.com_dict = dict(self.com_ports)
        self.selected_value = tk.StringVar(self.mainlabel)
        self.selected_value.set(f"{self.com_ports[0][0]} ({self.com_ports[0][1]})")  # Set default port and device
        self.port_menu = tk.OptionMenu(self.mainlabel, self.selected_value, *[f"{port[0]} ({port[1]})" for port in self.com_ports], command=self.on_com_select)
        # port_menu.pack(pady=20)
        


    def publish(self):
        self.mainlabel.grid(row=0, column=0, padx=5, pady=5)
        self.text.grid(row=0, column=0)
        self.port_menu.grid(row=0, column=1)

# get all the serial ports as a list.
    def get_serial_ports(self):
        self.ports = serial.tools.list_ports.comports()
        self.port_list = []
        for port in self.ports:
            self.port_list.append((port.device, port.description))
        return self.port_list

# when a port is selected from the drowpdown menu.
    def on_com_select(self, event):
        self.selected_value = event.widget.get()
        self.selected_port, self.selected_device = self.selected_value.split(' (', 1)
        self.selected_device = self.selected_device[:-1]  # Remove the closing parenthesis
        print(f"Selected Port: {self.selected_port}")
        print(f"Selected Device: {self.selected_device}")
    
    def get_selected_port(self):
        return self.selected_port

if __name__ == "__main__":
    window()
