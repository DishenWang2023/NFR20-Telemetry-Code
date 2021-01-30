import time
import struct
import serial
import serial.tools.list_ports
import numpy as np
import telemetry_csv as tc
import sensor_list as sl

# from digi.xbee.devices import XBeeDevice
csv_name = "Telemetry_Data/test_data.csv"


def select_serial_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # index 1 of p is the name of the port, this works only for windows, MacOS uses 0
        if 'Serial Port' in p[1]:
            return serial.Serial(p[0], 9600)


try:
    device.close()
except:
    None

''' Establish serial device connection '''
# device = serial.Serial('\\dev\\tty.usbserial-D306E0R6', 9600)
device = select_serial_port()
# print(device)


''' Wait for connection to establish '''
while (device.inWaiting() == 0):
    print('waiting')
    time.sleep(2)
    pass

''' ack '''
print("Data received!")
time.sleep(1)

index = 0
start_time = time.time()
size = 37 * 2
id_bytes = b'\x80\x01'
sig_list = np.array([0, 0, 1, 2, 0, 0, 1, 2,
                    1, 1, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 3, 3, 3, 2, 1,
                    0, 0, 0, 0, 0, 0, 0, 0,
                    4, 1, 2, 1])  # multiplications for each sensor values turning short back to float

tc.csv_create_header(csv_name, sl.sensor_names)

"""___TODO___

1. Send 36 values

"""
while True:
    current_time = round(time.time() - start_time, 2)
    ''' read input stream, works like a stack '''
    raw_values = device.read_until(id_bytes, size)
    # MAKE SURE THE STRING FILE HAS THE CORRECT SIZE, OTHERWISE ABANDON DATA
    if (raw_values[len(raw_values) - 2:len(raw_values)] != id_bytes) | (len(raw_values) < size):
        # print("Warning, incorrect identifier, second chance")
        raw_values += device.read_until(id_bytes, size)
        if raw_values[len(raw_values) - 2:len(raw_values)] != id_bytes:
            print("Second chance fail at: " + current_time)
            print(raw_values)
            time.sleep(0.1)
            device.flushInput()
            continue
    ''' decoode "byte" type and remove newline char '''
    # v = raw_values.decode('utf-8', errors='ignore').strip('\n').strip('\r')
    tuple_values = struct.unpack('>'+'h'*(size//2), raw_values[len(raw_values)-size:len(raw_values)])  # data type: tuple
    sensor_values = np.asarray(tuple_values[:len(tuple_values)-1]) / (10 ** sig_list)
    print(current_time)

    csv_list = np.concatenate((np.array([index, current_time]), sensor_values))
    index += 1
    tc.csv_store_data(csv_name, sl.sensor_names, csv_list)
    print(csv_list)

    ''' wait '''
    time.sleep(0.1)  # default 0.1
    ''' flush input stream '''
    device.flushInput()
