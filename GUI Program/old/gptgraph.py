import matplotlib.pyplot as plt

# Create a figure and subplot
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Create an empty line for the plot

# Set up the plot parameters
ax.set_xlim(0, 10)  # Initial x-axis limits
ax.set_ylim(0, 100)  # Initial y-axis limits
ax.set_title("Dynamic Plot")

# Function to update the plot
def update_plot():
    x_data.append(time.time())  # Example x-data (time)
    y_data.append(np.random.randint(0, 100))  # Example y-data (random)

    # Update the line with new data
    line.set_data(x_data, y_data)

    # Adjust the x-axis limits to show the most recent data points
    ax.set_xlim(max(0, x_data[-1] - 10), x_data[-1])

    # Redraw the figure
    fig.canvas.draw()

# Continuously update the plot (for demonstration purposes)
while True:
    update_plot()
    plt.pause(1)  # Pause for 1 second between updates