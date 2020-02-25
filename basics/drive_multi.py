#!/bin/sh
import multiprocessing
import time
import os
import atexit
from pprint import pprint

from easygopigo3 import EasyGoPiGo3
# from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading

gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)


def drive_instructions():
    pro_name = multiprocessing.current_process().name
    print(f"")
    gpg.drive_cm(10)
    gpg.turn_degrees(90)
    gpg.drive_cm(20)
    gpg.turn_degrees(-90)
    gpg.drive_cm(10)


drive_process = multiprocessing.Process(
    name='drive',
    target=drive_instructions
)

num = 5
while num > 0:
    gpg.drive_cm(10)
    time.sleep(.15)
    gpg.turn_degrees(10)
    measurements = get_reading()
    # pprint(measurements)
    print(f"{measurements.get('euler_x')}")
    num -= 1

drive_process.join()
