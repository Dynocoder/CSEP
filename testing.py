import csv
import os


def save_data_csv(value):

    file_path = "data\data.csv"

    field_names = ["time", "value"]

    try:
        with open(file_path, 'r') as rdr:
            reader = csv.reader(rdr)
            # if any(reader):
            #     file_exists = True
        rdr.close()
    except FileNotFoundError or FileExistsError:
        with open(file_path, 'w', newline='') as wtr:
            write = csv.DictWriter(wtr, fieldnames=field_names)
            write.writeheader()
        wtr.close()

    # Read the Last time value
    with open(file_path, 'r') as read:
        reader = csv.DictReader(read)
        reader_list = list(reader)
        fields = reader.fieldnames

        # If the File is newly Created 
        if len(reader_list) >= 1:
            print(reader_list[-1][fields[0]])
            last_time = reader_list[-1]
            new_time = int(last_time[fields[0]]) + 1
        else:
            new_time = 0

    read.close()

    # Write the data in the csv file with a time increment of 1 second
    with open(file_path, 'a', newline='') as write:
        writer = csv.DictWriter(write, fieldnames=fields)
        writer.writerow({fields[0]: new_time, fields[1]: value})

    write.close()


    # **************************************
for i in range(0, 10):
    save_data_csv(i)
