import tkinter as tk
import serial 
import tkinter.messagebox as mb
import time
import threading

class Main:

    def __init__(self) -> None:
        GUI_Title = "Temperature Sensor"
        self.sensor_cmd = str(['c1t0', 'c200', 'c300', 'c400']) 
        self.sensor_response_cmd = str(['c100', 'c200', 'c300', 'c400']) 
        self.sensor_connect_cmd = str(['c1c0', 'c200', 'c300', 'c400']) 

        self.root = tk.Tk()
        self.root.title(GUI_Title)




    # creating GUI components:
    def components(self):
        self.com_info_frame = tk.LabelFrame(self.root, text="COM information", padx=5, pady=5)
        self.com_entry_label = tk.Label(self.com_info_frame, text="Enter Port", padx=5, pady=5)
        self.com_entry_text = tk.Entry(self.com_info_frame)
        self.com_status_text = tk.Label(self.com_info_frame, text="Not Connected", fg="red", padx=5, pady=5)

        self.read_frame = tk.LabelFrame(self.root, text="Communication", padx=5, pady=5)
        self.read_delay_label = tk.Label(self.read_frame, text="Delay (s)")
        self.read_delay = tk.Entry(self.read_frame)
        self.start_btn = tk.Button(self.read_frame, text="Start", command=self.start, padx=5, pady=5)
        self.stop_btn = tk.Button(self.read_frame, text="Stop", command=self.stop, padx=5, pady=5)


        self.value_frame = tk.LabelFrame(self.root, text="Sensor Reading", height=300)
        self.value_label = tk.Label(self.value_frame, text="00.00", padx=20, pady=20, font=("Helvetica", 50))

        # placing the components:
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)
        self.com_info_frame.grid(row=0, column=0, sticky="nsew")
        self.com_entry_label.grid(row=0, column=0)
        self.com_entry_text.grid(row=0, column=1)
        self.com_status_text.grid(row=1, column=0, columnspan=2)
        self.read_frame.grid(row=0, column=1, sticky="nsew")
        self.read_delay_label.grid(row=0, column=0)

        self.read_delay.grid(row=0, column=1)
        self.start_btn.grid(row=1, column=0)
        self.stop_btn.grid(row=1, column=1)

        self.value_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.value_label.place(relx=0.5, rely=0.5, anchor="center")
        # self.value_label.grid()

        

    def start(self):

        self.com_port = self.com_entry_text.get()
        self.delay = self.read_delay.get()
        if self.com_port and self.delay:
            print(self.com_port, self.delay)
            try:
                self.connect()
                self.t1 = threading.Thread(
                target=self.read_thread, daemon=True)
                self.t1.start()

                 
            except Exception as e:
                mb.showerror(message=e) 
        else:
            mb.showerror(title="Values Missing", message="Enter the values")

        
    def stop(self):
        if self.arduino.is_open:
            self.arduino.close()
            self.t1.join()
        

    def connect(self):
        try:
            self.com_status_text.config(text="Connecting...", fg="orange")
            self.root.update()
            self.arduino = serial.Serial(port=self.com_port, baudrate=9600, timeout=10)
            # this delay is important to ensure that the port is properly allocated. Spent 5hrs figuring this out :(
            time.sleep(1)

            self.arduino.reset_input_buffer()

            self.arduino.write(self.sensor_connect_cmd.encode())

            response = self.arduino.readline().decode().rstrip()
            if response == self.sensor_response_cmd:
                # setting the timeout to wait for infinite time.
                self.arduino.timeout = None
                self.com_status_text.config(text="Connected", fg="green")

        except Exception as e:
            mb.showerror(message=e)


    def read_thread(self):
        while self.arduino.is_open:
            self.arduino.reset_input_buffer()
            self.arduino.write(self.sensor_cmd.encode())
            response = self.arduino.readline().decode()
            response_list = response.split(", ")
            value = (float)(response_list[0])
            self.update_gui(value)
            print(value)
            for i in threading.enumerate():
                print("thread: ", i)
            time_delay = (int)(self.read_delay.get())
            time.sleep(time_delay)
        else:
            print("Port Closed")
    

    def update_gui(self, value):
        self.value_label.config(text=value)
        self.root.update()

main = Main()
main.components()
main.root.mainloop()
