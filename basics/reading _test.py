from __future__ import print_function
from __future__ import division
import time
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit


# print("Example program for reading a Dexter Industries IMU Sensor on a GoPiGo3 AD1 port.")
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()

# gpg.forward()

gpg.drive_cm(50,True)

i = 0
while i < 100:
    i += 1
  
    print(gpg.read_encoders())

    mag = imu.read_magnetometer()
    gyro = imu.read_gyroscope()
    euler = imu.read_euler()
    accel = imu.read_accelerometer()
    temp = imu.read_temperature()

    string_to_print = "Magnetometer X: {:.1f}  Y: {:.1f}  Z: {:.1f} " \
                      "Gyroscope X: {:.1f}  Y: {:.1f}  Z: {:.1f} " \
                      "Accelerometer X: {:.1f}  Y: {:.1f} Z: {:.1f} " \
                      "Euler Heading: {:.1f}  Roll: {:.1f}  Pitch: {:.1f} " \
                      "Temperature: {:.1f}C".format(mag[0], mag[1], mag[2],
                                                    gyro[0], gyro[1], gyro[2],
                                                    accel[0], accel[1], accel[2],
                                                    euler[0], euler[1], euler[2],
                                                    temp)
    print(string_to_print)

    time.sleep(0.1)

gpg.stop()
