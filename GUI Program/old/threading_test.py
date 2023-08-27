import threading
import time

def non_daemon_thread():
    for i in range(5):
        print("Non-daemon thread working...")
        time.sleep(1)

def daemon_thread():
    while True:
        print("Daemon thread working...")
        time.sleep(1)

# Create a non-daemon thread
non_daemon = threading.Thread(target=non_daemon_thread)

# Create a daemon thread
daemon = threading.Thread(target=daemon_thread, daemon=True)

# Start both threads
non_daemon.start()
daemon.start()

# Let the threads run for a few seconds
time.sleep(3)

# When the program exits, the daemon thread will be terminated abruptly.
print("Main program exiting...")
