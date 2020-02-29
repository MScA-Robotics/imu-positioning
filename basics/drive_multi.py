#!/bin/sh
import multiprocessing
import time
import os
import atexit
from pprint import pprint

import os
import sys
import inspect

# or run as module from project root python3 -m basics.drive_multi
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from easygopigo3 import EasyGoPiGo3
# from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading

gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)


def drive_instructions():
    process_name = multiprocessing.current_process().name
    print("Starting Drive Process {}".format(process_name))
    gpg.drive_cm(10)
    gpg.turn_degrees(90)
    gpg.drive_cm(20)
    gpg.turn_degrees(-90)
    gpg.drive_cm(10)
    gpg.stop()


drive_process = multiprocessing.Process(
    name='drive',
    target=drive_instructions
)
drive_process.start()
num = 30
while num > 0:
    time.sleep(.10)
    measurements = get_reading()
    # pprint(measurements)
    print("Bearing: {}".format(measurements.get('euler_x')))
    num -= 1

drive_process.join()
