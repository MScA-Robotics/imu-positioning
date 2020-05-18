"""Measure Position as a Gaussian, implementing 1/2 of KF

This contains all of measure_gyro with changes being made to create
 matrices discussed in Probabilistic Robotics

nu - translational velocity
omega - rotational velocity

translation in a straight line (distance in cm - r) is lr_avg
translational_vel = lr_avg / delta_time * delta_theta

Run on linux  as 'python3 -m measure.measure_gaussian'
"""
from __future__ import print_function
from __future__ import division
import multiprocessing
import time
import atexit
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import print_reading, get_reading
from drive.control import drive_home, return_to_point
import drive.routes as routes
# some route names:
# drive_inst_1, drive_inst_2, drive_inst_3, drive_mini_1, drive_mini_2 drive_pause_1

# ## imports for plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Setup Manual Inputs (HARD CODES)
test_drive_instr = routes.drive_mini_2
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


def update_position(left_prev, right_prev, mu_prev, cov, time_prev):
    theta_prev = mu_prev[2, 0]
    # Initialize data needed
    new_reading = get_reading()
    delta_time = (new_reading.get('time') - time_prev).total_seconds()

    # Get 'r' from encoders and scale to centimeters
    scale = 0.0577
    left_delta = new_reading.get('left_enc') - left_prev
    right_delta = new_reading.get('right_enc') - right_prev
    r = (left_delta + right_delta) / 2 * scale
    nu = r / delta_time

    # Update theta based upon gyroscope
    omega = new_reading.get('gyro_y')
    theta_new = theta_prev - omega * delta_time
    vel_r = nu / omega if np.abs(omega) > 10e-4 else nu / 10e-4

    G_t = np.array([
        [1, 0, vel_r * (np.cos(theta_new) - np.cos(theta_prev))],
        [0, 1, vel_r * (np.sin(theta_new) - np.sin(theta_prev))],
        [0, 0, 1]
    ])

    V_t = np.array([
        [(-np.sin(theta_prev) + np.sin(theta_new)) / omega,
         nu * (np.sin(theta_prev) - np.sin(theta_new)) / omega**2 + (vel_r * np.cos(theta_new) * delta_time)],
        [(np.cos(theta_prev) - np.cos(theta_new)) / omega,
         -nu * (np.cos(theta_prev) - np.cos(theta_new)) / omega**2 + (vel_r * np.sin(theta_new) * delta_time)],
        [0, delta_time]
    ])

    # What to plugin to alpha 1-4?
    M_t = np.array([
        [nu**2 + omega**2, 0],
        [0, nu**2 + omega**2]
    ])

    # noinspection PyPep8Naming
    Sigma = G_t.dot(cov).dot(G_t.T) + V_t.dot(M_t).dot(V_t.T)

    delta_x = np.sin(theta_new * 0.0174533) * r
    delta_y = np.cos(theta_new * 0.0174533) * r
    mu_new = mu_prev + np.array([
        [vel_r * (np.sin(theta_new * np.pi / 180) - np.sin(theta_prev * np.pi / 180))],
        [vel_r * (np.cos(theta_prev * np.pi / 180) - np.cos(theta_new * np.pi / 180))],
        [omega * delta_time]
    ])
    return new_reading.get('left_enc'), new_reading.get('right_enc'), mu_new, Sigma, new_reading.get('time')


# Initialize Measurements for drive
i = 0
data = []
pose = np.array([
    [init_x],
    [init_y],
    [get_reading().get('euler_x')]
])
cov = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
left_prev = 0
right_prev = 0
curr_time = datetime.now()

# Start Driving
drive_process.start()

# Measure while driving loop
while i < 100:
    # mu is 3 x 1 pose
    left_prev, right_prev, pose, cov, curr_time = update_position(left_prev, right_prev, pose, cov, curr_time)
    # print("x= %2.2f, y=%2.2f, theta==%2.2f " % (pose[0], pose[1], pose[2]))
    print(pose)
    data.append({
        "t": str(curr_time),
        "x": pose[0],
        "y": pose[1],
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
    distance_back = np.sqrt(x_total * x_total + y_total * y_total)

    direction_back = 90 - theta + 90 + 90

    print("Back direction= %8.2f dist=%8.2f" % (direction_back, distance_back / 44))

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
