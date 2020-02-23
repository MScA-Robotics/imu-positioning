#!/bin/sh
import time
import atexit
from pprint import pprint
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

# import sys
# print(sys.path)
from utils import get_reading

import os
print(os.getcwd())

gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

num = 5
while num > 0:
    gpg.drive_cm(10)
    time.sleep(.15)
    gpg.turn_degrees(10)
    measurements = get_reading()
    pprint(measurements)
    print("")
    num -= 1
