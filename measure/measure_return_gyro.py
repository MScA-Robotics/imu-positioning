"""Measure Return 3n with Gyroscope

This contains all of measure_return_3n as of 5/9/20 with changes that
incorporate angular velocity from the gyroscope
"""
from __future__ import print_function
from __future__ import division
import multiprocessing
import time
import atexit
import math
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import print_reading, get_reading
from drive.control import drive_home, return_to_point
from drive.routes import drive_inst_1, drive_inst_2, drive_inst_3, drive_mini_1, drive_pause_1

# ## imports for plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

# Setup Manual Inputs (HARD CODES)
test_drive_instr = drive_pause_1
attempt_return = False
saving_data = False
draw_path = True
init_x, init_y = 0, 0  # For test path 2 use 250, 50

# Path 1
# drive_inst_1
# init_x, init_y = 0, 0

# Path 2
# drive_inst_3
# init_x, init_y = 250, 50 or 50, 250

# Setup Sensors
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr
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
    # print("x= %2.2f, y=%2.2f, dx= %2.2f, dy=%2.2f, euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44,x/44, y/44, euler_x,theta))
    print("x= %2.2f, y=%2.2f, theta==%2.2f " % (x_total/44, y_total/44, theta))
    data.append({
        "t": str(curr_time),
        "x": x_total,
        "y": y_total
    })
    
    # Prepare for next iteration
    i += 1
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
