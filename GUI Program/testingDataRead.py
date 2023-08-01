import csv
import os

times = []
values = []


def createfile(filepath):
    # file_path = filepath
    print("create File: ", filepath)
    file_path = filepath + ".csv"
    field_names = ["time", "value"]

    # Checks whether the file exists or not. If it does, it removes it and calls the function again.
    try:
        with open(file_path, 'r') as rdr:
            reader = csv.reader(rdr)
            if any(reader):
                rdr.close()
                os.remove(file_path)
                createfile(filepath=filepath)
    except FileNotFoundError or FileExistsError:
        with open(file_path, 'w', newline='') as wtr:
            write = csv.DictWriter(wtr, fieldnames=field_names)
            write.writeheader()
            
        wtr.close()

createfile("data")