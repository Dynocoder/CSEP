import serial

# Open a connection to the Arduino (change the port name as needed)
ser = serial.Serial('COM5', 9600)  # Change 'COM3' to the appropriate port

try:
    while True:
        if ser.in_waiting > 0:
            ser.reset_input_buffer()
        user_input = input("Enter a string to send to Arduino (or 'exit' to quit): ")

        if user_input == 'exit':
            break

        # Send the user input to Arduino
        ser.write(user_input.encode())  # Encode the string and send it

        # Read and print the response from Arduino
        response = ser.readline().decode().strip()
        print("Arduino response:", response)

finally:
    ser.close()  # Close the serial connection when done
