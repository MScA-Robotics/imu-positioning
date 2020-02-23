#!/bin/sh
# iterated path drive

import time
import atexit
from pprint import pprint
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
import pickle

# import sys
# print(sys.path)

from utils import get_reading

import os
print(os.getcwd())

gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

data = []

num = 5
while num > 0:
    gpg.drive_cm(25)
    time.sleep(.01)
    gpg.turn_degrees(10)
    measurement = get_reading()
    pprint(measurement)
    data.append(measurement)
    print("")
    num -= 1
    
with open('test_drive_2_data_5.pkl', "ab") as f:
    pickle.dump(data, f)
