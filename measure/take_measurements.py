"""Continuous Reading of Sensors During Constant Drive

This file is meant to be run from the root directory with -m module option
python3 -m measure.take_measurements
"""
import os
import multiprocessing
import time
import csv
import atexit
from pprint import pprint

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading
import drive.routes as routes

# Setup Manual Inputs (HARD CODES)
test_drive_instr = routes.drive_mini_1
drive_name = 'acceleration_sample_1'
saving_data = True
write_header = True
file_out = 'accel_sample_7_19.csv'

# Setup Sensors
# imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

# Setup Standard Drive
q = multiprocessing.Queue()
drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr,
    args=(q,)
)

# drive_process.start()

i = 0
data = []
while i < 200:
    # if i == 100:
    #     drive_process.start()
        
    reading = get_reading(read_mag=False)
    reading['drive name'] = drive_name
    data.append(reading)
    i += 1
    while not q.empty():
        print(q.get())
    time.sleep(.0625)

# Wrap up processes, print and save
# drive_process.join()
pprint(data)
print('done')

if saving_data:
    output_file_name = os.path.join(os.getcwd(), 'offline', 'data', file_out)
    # keys = data[0].keys()
    for rec in data:
        rec['time'] = rec.get('time').timestamp()
    
    keys = ['drive name', 'time', 'left_enc', 'right_enc',
            'euler_x', 'euler_y', 'euler_z',
            'mag_x', 'mag_y', 'mag_z',
            'accel_x', 'accel_y', 'accel_z',
            'gyro_x', 'gyro_y', 'gyro_z',
            ]

    with open(output_file_name, 'a') as f:
        dict_writer = csv.DictWriter(f, keys)
        if write_header:
            dict_writer.writeheader()
        dict_writer.writerows(data)
