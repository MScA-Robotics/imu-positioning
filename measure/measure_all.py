"""Measure Position as a Gaussian, implementing 1/2 of KF

Starting as a modification of measure_gaussian, here we will step through the
 linear kalman filter based upon Chapter 3 of Probabilistic Robotics and online
 resources.

Run on linux  as 'python3 -m measure.measure_linear_gaussian'
"""
import sys
import multiprocessing
import time
import atexit
import json
from pprint import pprint
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from drive.utils import get_reading
from drive.control import drive_home, return_to_point
import drive.routes as routes
# some route names:
# drive_inst_1, drive_inst_2, drive_inst_3, drive_mini_1, drive_mini_2 drive_pause_1

# ## imports for plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.seterr(all='raise')

# Setup Manual Inputs (HARD CODES)
test_drive_instr = routes.drive_mini_1
attempt_return = False
saving_data = False
draw_path = True
init_x, init_y = 0, 0
# For test path 1 use init_x = 0, init_y = 0 with drive_inst_1
# For test path 2 use init_x = 250, init_y 50 with drive_inst_3

# Setup Sensors
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


# noinspection PyPep8Naming
def update_position(left_prev, right_prev, vel_prev, mu_prev, cov, time_prev):
    """

    nu is translational velocity in cm per second
    omega is Rotational Velocity in radians per second

    :param left_prev:
    :param right_prev:
    :param mu_prev:
    :param cov:
    :param time_prev:
    :return:
    """
    theta_prev = mu_prev[2, 0]
    # Initialize data needed
    new_reading = get_reading(read_mag=False)
    delta_time = (new_reading.get('time') - time_prev).total_seconds()

    # Get 'r' from encoders and scale to centimeters
    scale = 0.0577
    left_delta = new_reading.get('left_enc') - left_prev
    right_delta = new_reading.get('right_enc') - right_prev
    # scale * average encoder advancement / time_elapsed
    nu = scale * (left_delta + right_delta) / (2 * delta_time)

    # TODO: Test the below decompositions, then refactor
    accel_forward = new_reading.get('accel_z')
    accel_side = new_reading.get('accel_x')

    nu_accel = vel_prev + delta_time * np.array([
        [accel_forward * np.sin(theta_prev) + accel_side * np.cos(theta_prev)],
        [accel_forward * np.cos(theta_prev) + accel_side * np.sin(theta_prev)]
    ])

    # TODO: Decompose back to velocity in forward direction
    # Total velocity is L2 Norm
    total_velocity = np.sqrt(nu_accel[0]**2 + nu_accel[1]**2)

    # Theta from Odometer
    rotation_scale = 5.5
    theta_od_delta = (left_delta - right_delta) / rotation_scale

    # Theta from Gyroscope
    omega = -new_reading.get('gyro_y') * np.pi / 180
    theta_gy_delta = omega * delta_time
    theta_new = theta_prev + theta_gy_delta

    r_od = nu / omega if np.abs(omega) > 10e-6 else nu / 10e-6
    r_sensor = nu_accel / omega if np.abs(omega) > 10e-6 else nu_accel / 10e-6

    mu_new = mu_prev + np.array([
        [r_od * (np.sin(theta_new) - np.sin(theta_prev))],
        [r_od * (np.cos(theta_prev) - np.cos(theta_new))],
        [omega * delta_time]
    ])

    mu_sensors_prev = np.array([0, 0, 0]).T
    mu_sensors_new = mu_sensors_prev + np.array([
        [r * (np.sin(theta_new) - np.sin(theta_prev))],
        [r * (np.cos(theta_prev) - np.cos(theta_new))],
        [omega * delta_time]
    ])

    if i % 10 == 0:
        print(mu_prev)
        print(mu_new)
        print(nu)
        print(omega)

    return (
        new_reading.get('left_enc'), new_reading.get('right_enc'),
        accel_velocity,
        mu_new, Sigma, new_reading.get('time')
    )


# Initialize Measurements for drive
i = 0
data = []
pose = np.array([
    [init_x],
    [init_y],
    [get_reading().get('euler_x') * np.pi / 180]
])
cov = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
left_prev = 0
right_prev = 0
curr_time = datetime.now()

# Start Driving
drive_process.start()

# Measure while driving loop
while i < 100:
    # mu is 3 x 1 pose
    left_prev, right_prev, vel_prev, pose, cov, curr_time = update_position(
        left_prev, right_prev, pose, cov, curr_time
    )
    # print("x= %2.2f, y=%2.2f, theta==%2.2f " % (pose[0], pose[1], pose[2]))
    # print(pose)
    data.append({
        "t": str(curr_time),
        "x": pose[0],
        "y": pose[1],
        "theta": pose[2],
        "cov": cov,
    })

    while not q.empty():
        print(q.get())

    # Prepare for next iteration
    i += 1
    time.sleep(.0625)

if draw_path:
    # Save a plot and pandas generated csv
    plt.style.use('seaborn-whitegrid')
    df = pd.DataFrame(data)
    fig = plt.figure()
    plt.plot(df.x, df.y, 'o', color='black')
    fig.savefig('plot.png')
    df.to_csv("df.csv", index=False)

# if attempt_return:
#     distance_back = np.sqrt(x_total * x_total + y_total * y_total)
#     direction_back = 90 - theta + 90 + 90
#     print("Back direction= %8.2f dist=%8.2f" % (direction_back, distance_back / 44))
#     gpg.turn_degrees(direction_back)
#     print("back inc= %8.2f back cm=%8.2f" % (distance_back / 44, distance_back / 44 * 2.54))
#     gpg.drive_cm(distance_back/44*2.54)
#     gpg.stop()

if saving_data:
    # Save Out
    with open('data.json', 'wb') as f:
        json.dump(data, f)
