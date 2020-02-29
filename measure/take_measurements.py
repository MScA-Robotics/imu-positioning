"""Continuous Reading of Sensors During Constant Drive

This file is meant to be run from the root directory with -m module option
python3 -m measure.take_measurements
"""
from __future__ import print_function
from __future__ import division
import time
import pickle
import atexit
from pprint import pprint
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading
from drive.routes import drive_inst_1, drive_inst_2

# Setup Manual Inputs (HARD CODES)
test_drive_instr = drive_inst_1
file_out = 'test_229.pkl'

# Setup Sensors
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

# Setup Standard Drive
drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr

)

drive_process.start()

i = 0
data = []
while i < 100:
    data.append(get_reading())
    i += 1
    time.sleep(.10)

# Wrap up processes, print and save
drive_process.join()
pprint(data)

output_file_name = os.path.join(os.getcwd(), 'offline', 'data', file_out)
with open(output_file_name, 'ab') as f:
    pickle.dump(data, f)

# 'wb' for write bytes
# 'ab' for append bytes
