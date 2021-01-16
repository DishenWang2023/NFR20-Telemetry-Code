import csv

def csv_create_header(csv_name, sensor_names):
    with open(csv_name, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=sensor_names)
        csv_writer.writeheader()


def csv_store_data(csv_name, sensor_names, csv_list):
    with open(csv_name, 'a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=sensor_names)
        # creates a dictionary with sensor_names as key and telemetry data as values
        info = {sensor_names[i]: csv_list[i] for i in range(len(sensor_names))}
        csv_writer.writerow(info)

