import tkinter as tk

win = tk.Tk()

win.geometry("500x500")

test_label = tk.Label(win)
test_label.pack(padx=20, pady=20)

value = 0


def update_val():
    global value
    test_label.config(text=value)
    value = value + 1
    # win.after(1000, func=update_val)

btn = tk.Button(win, text="Click", command=update_val)
btn.pack()

def close():
    win.destroy()

dt = tk.Button(win, text="destroy", command=close)
dt.pack()

# update_val()

win.mainloop()