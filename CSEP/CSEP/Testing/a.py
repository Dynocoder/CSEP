import tkinter as tk
from random import randint
root = tk.Tk()
lab = tk.Label(root)
lab.pack()

def update():
   lab['text'] = randint(0,1000)
   root.after(1000, update) # run itself again after 1000 ms

# run first time
update()

label = tk.Label(root, text="ha;skdjfhslkdajf")
label.pack()

root.mainloop()