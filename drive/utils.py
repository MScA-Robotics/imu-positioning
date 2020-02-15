from __future__ import print_function
from __future__ import division
import time
import pickle
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

import numpy as np
import math as math

# Setup Sensors
imu = InertialMeasurementUnit(bus = "GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()


def print_reading():
    mag = imu.read_magnetometer()
    gyro = imu.read_gyroscope()
    euler = imu.read_euler()
    accel = imu.read_accelerometer()
    temp = imu.read_temperature()
    encoder = gpg.read_encoders()

    string_to_print = "Magnetometer X: {:.1f}  Y: {:.1f}  Z: {:.1f} " \
                      "Gyroscope X: {:.1f}  Y: {:.1f}  Z: {:.1f} " \
                      "Accelerometer X: {:.1f}  Y: {:.1f} Z: {:.1f} " \
                      "Euler Heading: {:.1f}  Roll: {:.1f}  Pitch: {:.1f} " \
                      "Temperature: {:.1f}C " \
                      "Left Encoder: {:.1f} " \
                      "Right Encoder: {:.1f}".format(mag[0], mag[1], mag[2],
                                                     gyro[0], gyro[1], gyro[2],
                                                     accel[0], accel[1], accel[2],
                                                     euler[0], euler[1], euler[2],
                                                     temp, encoder[0], encoder[1])
    print(string_to_print)


def get_reading():
    mag = imu.read_magnetometer()
    gyro = imu.read_gyroscope()
    euler = imu.read_euler()
    accel = imu.read_accelerometer()
    # temp = imu.read_temperature()
    encoder = gpg.read_encoders()
    res = {
        "mag_x": mag[0],
        "mag_y": mag[1],
        "mag_z": mag[2],
        "gyro_x": gyro[0],
        "gyro_y": gyro[1],
        "gyro_z": gyro[2],
        "accel_x": accel[0],
        "accel_y": accel[1],
        "accel_z": accel[2],
        "euler_x": euler[0],
        "euler_y": euler[1],
        "euler_z": euler[2],
        # "temp": temp,
        "left_enc": encoder[0],
        "right_enc": encoder[1],
    }

    return res
