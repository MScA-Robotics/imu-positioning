"""Continuous Reading of Sensors During Constant Drive

This file is meant to be run from the root directory with -m module option
python3 -m measure.take_measurements
"""
from __future__ import print_function
from __future__ import division
import multiprocessing
import time
import pickle
import atexit
import os
from pprint import pprint
from datetime import datetime, timedelta
import csv

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading
from drive.routes import drive_inst_1, drive_inst_2

# Setup Manual Inputs (HARD CODES)
test_drive_instr = drive_inst_1
drive_name = 'sample_drive_3'
write_header = False
file_out = 'drives_1_229.csv'

# Setup Sensors
# imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

# Setup File


# Setup Standard Drive
drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr

)

drive_process.start()

i = 0
data = []
while i < 100:
    reading = get_reading()
    reading['drive name'] = drive_name
    data.append(reading)
    i += 1
    time.sleep(.10)

# Wrap up processes, print and save
drive_process.join()
# pprint(data)
print('done')

output_file_name = os.path.join(os.getcwd(), 'offline', 'data', file_out)
# keys = data[0].keys()
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
    # pickle.dump(data, f)
