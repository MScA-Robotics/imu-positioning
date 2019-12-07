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
    try:
        mag   = imu.read_magnetometer()
        gyro  = imu.read_gyroscope()
        euler = imu.read_euler()
        accel = imu.read_accelerometer()
        temp  = imu.read_temperature()
        encoder   = gpg.read_encoders()
        quat      = imu.read_quaternion()
        lin_accel = imu.read_linear_acceleration()
        now   = datetime.now()

            
        string_to_print = "Magnetometer X: {:.1f}  Y: {:.1f}  Z: {:.1f} " \
                          "Gyroscope X: {:.1f}  Y: {:.1f}  Z: {:.1f} " \
                          "Accelerometer X: {:.1f}  Y: {:.1f} Z: {:.1f} " \
                          "Linear Accel: X: {:.1f}  Y: {:.1f} Z: {:.1f} " \
                          "Euler Heading: {:.1f}  Roll: {:.1f}  Pitch: {:.1f} " \
                          "Quaternion: 1: {:.1f}  2: {:.1f} 3: {:.1f} 4: {:.1f} " \
                          "Temperature: {:.1f}C " \
                          "Left Encoder: {:.1f} " \
                          "Right Encoder: {:.1f} " \
                          "Timestamp: {}".format(mag[0], mag[1], mag[2],
                                                      gyro[0], gyro[1], gyro[2],
                                                      accel[0], accel[1], accel[2],
                                                      lin_accel[0], lin_accel[1], lin_accel[2],
                                                      euler[0], euler[1], euler[2],
                                                      quat[0], quat[1], quat[2], quat[3],
                                                      temp, encoder[0], encoder[1], now)
        print(string_to_print)
    except IOError:
        print("Skipped Measurement, IOError")

def get_reading():
    try:
        mag   = imu.read_magnetometer()
        gyro  = imu.read_gyroscope()
        euler = imu.read_euler()
        accel = imu.read_accelerometer()
        temp  = imu.read_temperature()
        encoder = gpg.read_encoders()
        quat  = imu.read_quaternion()
        lin_accel = imu.read_linear_acceleration()
        now = datetime.now()

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
            "lin_a_x": lin_accel[0], 
            "lin_a_y": lin_accel[1],
            "lin_a_z": lin_accel[2], 
            "quaterntion 1": quat[0],
            "quaterntion 2": quat[1],
            "quaterntion 3": quat[2],
            "quaterntion 4": quat[3],
            "euler_x": euler[0],
            "euler_y": euler[1],
            "euler_z": euler[2],
            # "temp": temp, 
            "left_enc": encoder[0],
            "right_enc": encoder[1],
            "timestamp": str(now) 
        }
        
        return res
    except IOError:
        return None


# gpg.forward()
# gpg.drive_cm(50,True)

i=0
t1 = datetime.now()
data = []
while  i<400:
    # Execute
    print_reading()
    # data.append(get_reading())
    t2 = datetime.now()
    print("Duration: {}".format(t2 - t1))
    # print(timedelta(t2, t1))
        
    # Prepare for next iteration
    i += 1
    t1 = t2
    time.sleep(20/1000)
  
gpg.stop()


# Save Out
with open('test.pkl', 'wb') as f:
    pickle.dump(data, f)

