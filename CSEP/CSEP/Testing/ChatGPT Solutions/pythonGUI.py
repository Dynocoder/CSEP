import tkinter as tk

# Create the main window
window = tk.Tk()

# Set the window dimensions
window.geometry("800x600")

# Calculate the center position for the button
window.update()  # Updates window dimensions
window_width = window.winfo_width()
window_height = window.winfo_height()
button_width = 100
button_height = 50
button_x = 20
button_y = 20

# Create the button
button = tk.Button(window, text="Click Me")
button.place(x=button_x, y=button_y, width=button_width, height=button_height)

# Start the GUI event loop
window.mainloop()
