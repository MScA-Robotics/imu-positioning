"""Measure Return Updated to use the Gyroscope

This contains all of measure_return_3n as of 5/9/20 with changes that
incorporate angular velocity from the gyroscope

Turning is measured from the Gyroscope
Distance is measured from the Odometer

Run on linux  as 'python3 -m measure.measure_gyroscope'
"""
import multiprocessing
import time
import atexit
import math
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading
from drive.control import drive_home, return_to_point
import drive.routes as routes

# ## imports for plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

# Setup Manual Inputs (HARD CODES)
test_drive_instr = routes.drive_pause_1
attempt_return = False
saving_data = False
draw_path = True
init_x, init_y = 0, 0
# For test path 1 use init_x = 0,  init_y = 0 with drive_inst_1
# For test path 2 use init_x = 250, init_y 50 with drive_inst_3

# Setup Sensors
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

# Setup Standard Drive
q = multiprocessing.Queue()
drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr,
    args=(q,)
)


def update_position(left_prev, right_prev, theta_prev, time_prev):
    new_reading = get_reading()

    # Update Encoders
    left_delta = new_reading.get('left_enc') - left_prev
    right_delta = new_reading.get('right_enc') - right_prev
    
    # Scale factor to go from encoder to centimeter - 
    scale = 0.0577
    
    # Distance traveled in scaled units
    lr_avg = (left_delta + right_delta) / 2 * scale
    # translation in a straight line (distance in cm - r) is lr_avg
    # translational_vel = lr_avg / delta_time * delta_theta

    # Update theta based upon gyroscope
    delta_time = (new_reading.get('time') - time_prev).total_seconds()
    theta = theta_prev - new_reading.get('gyro_y') * delta_time

    delta_x = math.sin(theta * 0.0174533) * lr_avg
    delta_y = math.cos(theta * 0.0174533) * lr_avg
    return new_reading.get('left_enc'), new_reading.get('right_enc'), delta_x, delta_y, theta, new_reading.get('time')


# Initialize Measurements for drive
i = 0
data = []
left_prev = 0
right_prev = 0
x_total = init_x
y_total = init_y
theta = get_reading().get('euler_x')
curr_time = datetime.now()

# Start Driving
drive_process.start()

# Measure while driving loop
while i < 100:
    left_prev, right_prev, delta_x, delta_y, theta, curr_time = update_position(left_prev, right_prev, theta, curr_time)
    x_total = x_total + delta_x
    y_total = y_total + delta_y
    print("x= %2.2f, y=%2.2f, theta==%2.2f " % (x_total/44, y_total/44, theta))
    data.append({
        "t": str(curr_time),
        "x": x_total,
        "y": y_total
    })

    while not q.empty():
        print(q.get())

    # Prepare for next iteration
    i += 1
    time.sleep(.1)

if draw_path:
    plt.style.use('seaborn-whitegrid')
    df = pd.DataFrame(data)
    fig = plt.figure()
    plt.plot(df.x, df.y, 'o', color='black')
    fig.savefig('plot.png')
    df.to_csv("df.csv", index=False)

# if attempt_return:
#     distance_back = math.sqrt(x_total*x_total+y_total*y_total)
#     direction_back = 90 - theta + 90 + 90
#     print("Back direction= %8.2f dist=%8.2f" % (direction_back, distance_back/44))
#     gpg.turn_degrees(direction_back)
#     print("back inc= %8.2f back cm=%8.2f" % (distance_back / 44, distance_back / 44 * 2.54))
#     gpg.drive_cm(distance_back/44*2.54)
#     gpg.stop()

if saving_data:
    # Save Out
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)
