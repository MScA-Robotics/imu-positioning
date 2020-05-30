"""Measure Position based upon odometer

Working out of section 5.4 'Odometry Motion Model' in Probabilistic Robotics

Run on linux  as 'python3 -m measure.measure_odometer'
"""
from __future__ import print_function
from __future__ import division
import multiprocessing
import time
import atexit
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading
from drive.control import drive_home, return_to_point
import drive.routes as routes

# ## imports for plotting
import math as math
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Setup Manual Inputs (HARD CODES)
test_drive_instr = routes.drive_mini_1
attempt_return = False
saving_data = False
draw_path = True
init_x, init_y = 0, 0
# For test path 1 use 0, 0 with drive_inst_1
# For test path 2 use 250, 50 with drive_inst_3

# Setup Sensors
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr
)


def update_encoders(left_prev, right_prev, mu_prev):
    """Odometry Sensor Integration

    Integration of wheel encoder information to provide a continuous update of
     internal position. This state is never intended to be updated with other
     sensor information. Per 5.4 Odometry Motion Model - this is the function
     that will be reporting relative motion information such as advancement.

    :param left_prev: prior left encoder
    :param right_prev: prior right encoder
    :param mu_prev: prior internal pose - x_bar_t-1
    TODO: Add relative advancement in x and y to the return
     y_bar_prime - y_bar
     x_bar_prime - x_bar
     theta_bar_prime - theta_bar
    :return: current internal pose - x_bar_t
    """

    # Initialize data needed
    new_reading = get_reading(read_mag=False)

    # Update Encoders
    left_delta = new_reading.get('left_enc') - left_prev
    right_delta = new_reading.get('right_enc') - right_prev

    lr_delta = left_enc - right_enc

    lr_avg = (left_delta + right_delta) / 2

    if abs(lr_delta) > 2:
        
        theta_delta = euler_x - euler_x_prev
    else:
        theta_delta = 0

    theta_prev = mu_prev[2, 0]
    theta = theta_prev + theta_delta
    x = math.sin(theta*0.0174533) * lr_avg
    y = math.cos(theta*0.0174533) * lr_avg
    read_distance = 0
    res = {
        "x": x,
        "y": y
    }
    # print(res)
    return left_enc, right_enc, x, y, res, euler_x, theta

# Todo:
#  Initial Conditions are packed into pose 'mu'
# Initialize Measurements for drive
i = 0
t1 = datetime.now()
data = []
right_prev = 0
left_prev = 0
x_total = init_x
y_total = init_y
euler = imu.read_euler()
euler_x_prev = euler[0]
theta_prev = 0

# Start Driving
drive_process.start()

# Measure while driving loop
while i < 100:
    # Execute
    # #print_reading()
    # data.append(get_reading())
    
    t2 = datetime.now()
    left_enc, right_enc, x, y, res, euler_x, theta = get_position(right_prev, left_prev, euler_x_prev, theta_prev)
    euler_x_prev = euler_x
    theta_prev = theta
    right_prev = right_enc
    left_prev = left_enc
    x_total = x_total + x
    y_total = y_total + y
    # #print("x= %2.2f, y=%2.2f, dx= %2.2f, dy=%2.2f, euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44,x/44, y/44, euler_x,theta))
    print("x= %2.2f, y=%2.2f,  euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44, euler_x, theta))
    # #print(imu.read_euler()[0])
    # #print("Duration: {}".format(t2 - t1))
    # print(timedelta(t2, t1))
    res2 = {
        "t": str(t2),
        "x": x_total,
        "y": y_total
    }
    data.append(res2)
    
    # Prepare for next iteration
    i += 1
    t1 = t2
    time.sleep(.1)

print(data[1])
    

print("printing path")
plt.style.use('seaborn-whitegrid')
df = pd.DataFrame(data) 
# 'lr_delta': -1, 'euler_x': 240.4375, 'left_enc': 2585, 'y': 4.216956575971679, 'theta': -32.5, 'x_delta': 4,
#  'right_enc': 2586, 'x': -2.6864990668841138, 'y_delta': 6
# print(df[1])
print(df.head())
# df.columns = ['lr_delta','euler_x',"left_enc","y",'theta','x_delta','right_enc','x','y_delta']
fig = plt.figure()
plt.plot(df.x, df.y, 'o', color='black')
fig.savefig('plot.png')
df.to_csv("df.csv", index=False)      


if attempt_return:
    # #print(imu.read_euler()[0])
    distance_back = math.sqrt(x_total*x_total+y_total*y_total)

    direction_back = 90 - theta + 90 + 90

    print("Back direction= %8.2f dist=%8.2f" % (direction_back, distance_back/44))

    gpg.turn_degrees(direction_back)
    print("back inc= %8.2f back cm=%8.2f" % (distance_back / 44, distance_back / 44 * 2.54))
    # ##gpg.drive_cm(distance_back/44*2.54)
    gpg.stop()  
    # Save Out
    # with open('data.pkl', 'wb') as f:
        # pickle.dump(data, f)

if saving_data:
    # Save Out
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)

# run file python3 -m measure.measure_return_3
