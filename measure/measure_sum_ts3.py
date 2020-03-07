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
from di_sensors.distance_sensor import DistanceSensor

import numpy as np
import math as math
# establish communication with the DistanceSensor
ds = DistanceSensor()

# set the sensor in fast-polling-mode
ds.start_continuous()
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

def get_position(right_prev,left_prev,euler_x_prev,theta_prev):

    euler = imu.read_euler()
    euler_x=euler[0]

    encoder = gpg.read_encoders()
    left_enc=encoder[0]
    right_enc= encoder[1]
    lr_delta=left_enc-right_enc
    y_delta=left_enc-left_prev
    x_delta=right_enc-right_prev
    lr_avg=(x_delta+y_delta)/2
    if(abs(lr_delta)>2):
        
        theta_delta=euler_x-euler_x_prev
    else:
        theta_delta=0
    theta=theta_prev+theta_delta
    x=math.sin(theta*0.0174533)*lr_avg
    y=math.cos(theta*0.0174533)*lr_avg
    read_distance = ds.read_range_continuous()
    res = {

        "left_enc": left_enc,
        "right_enc": right_enc,
        "x": x,
        "y": y,
        "euler_x":euler_x,
        "y_delta":y_delta,
        "x_delta":x_delta,
        "theta":theta,
        "lr_delta":lr_delta
        
    }
    ##print(res)
    return left_enc,right_enc,x,y,res,euler_x,theta

##243.5625-341.6250

i=0
t1 = datetime.now()
data = []
right_prev=0
left_prev=0
x_total=0
y_total=0
euler = imu.read_euler()
euler_x_prev=euler[0]
theta_prev=0
while  i<100:
    # Execute
    ##print_reading()
    #data.append(get_reading())
    
    t2 = datetime.now()
    left_enc,right_enc,x,y,res,euler_x,theta=get_position(right_prev,left_prev,euler_x_prev,theta_prev)
    euler_x_prev=euler_x
    theta_prev=theta
    right_prev=right_enc
    left_prev=left_enc
    x_total=x_total+x
    y_total=y_total+y
    ##print("x= %2.2f, y=%2.2f, dx= %2.2f, dy=%2.2f, euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44,x/44, y/44, euler_x,theta))
    print("x= %2.2f, y=%2.2f,  euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44, euler_x,theta))
    ##print(imu.read_euler()[0])
    ##print("Duration: {}".format(t2 - t1))
    # print(timedelta(t2, t1))
    data.append(res)
    
    # Prepare for next iteration
    i += 1
    t1 = t2
    time.sleep(.1)
    

gpg.stop()

##print(imu.read_euler()[0]) 
distance_back=math.sqrt(x_total*x_total+y_total*y_total)

direction_back=90-theta+90+90




print("Back direction= %8.2f dist=%8.2f" % (direction_back, distance_back/44))







##while angle_delta>1:
  ##  angle=imu.read_euler()[0]
    ##angle_delta=direction_back-angle
  ##  gpg.right()
  ##  time.sleep(.1)
 ##   gpg.stop()
 ##   print("current= %8.2f delta=%8.2f" % (angle, angle_delta))
 
gpg.turn_degrees(direction_back)
print("back inc= %8.2f back cm=%8.2f" % (distance_back/44, distance_back/44*2.54))
###gpg.drive_cm(distance_back/44*2.54)  
gpg.stop()  
# Save Out
#with open('data.pkl', 'wb') as f:
    #pickle.dump(data, f)
# Save Out
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)
