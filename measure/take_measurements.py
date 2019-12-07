"""Continuous Reading of Sensors

Make continuous readings from the sensors and begin
a take measurements function.

We Believe the Following:
Magnet x: 
Magnet y:
Magnet z:
Euler Heading: Dir w/ 0 being North 90 East, 180 South, 270 West
Euler Roll:
Euler Pitch: Angle up 
Accel x:
Accel y:
Accel z:
Euler x:
Euler y:
Euler z:
Thermometer: Temperature in Celcius
Left Encoder: Odometer of left wheel
Right Encoder: Odometer of right wheel
"""
from __future__ import print_function
from __future__ import division
import time
import pickle
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

# Setup Sensors
imu = InertialMeasurementUnit(bus = "GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()


def print_reading():
    mag   = imu.read_magnetometer()
    gyro  = imu.read_gyroscope()
    euler = imu.read_euler()
    accel = imu.read_accelerometer()
    temp  = imu.read_temperature()
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
    mag   = imu.read_magnetometer()
    gyro  = imu.read_gyroscope()
    euler = imu.read_euler()
    accel = imu.read_accelerometer()
    temp  = imu.read_temperature()
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


# gpg.forward()
# gpg.drive_cm(50,True)

i=0
t1 = datetime.now()
data = []
while  i<100:
    # Execute
    print_reading()
    data.append(get_reading())
    t2 = datetime.now()
    print("Duration: {}".format(t2 - t1))
    # print(timedelta(t2, t1))
    
    
    # Prepare for next iteration
    i += 1
    t1 = t2
    time.sleep(.1)
  
gpg.stop()


# Save Out
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

