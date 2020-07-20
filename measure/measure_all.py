"""Measure Position as a Gaussian, implementing 1/2 of KF

Starting as a modification of measure_gaussian, here we will step through the
 linear kalman filter based upon Chapter 3 of Probabilistic Robotics and online
 resources.

Run on linux  as 'python3 -m measure.measure_linear_gaussian'

Manual Settings Area:
  routes to choose:
  drive_inst_1, drive_inst_2, drive_inst_3, drive_mini_1, drive_mini_2 drive_pause_1
  
  forward_cal_1

For test path 1 use init_x = 0, init_y = 0 with drive_inst_1
For test path 2 use init_x = 250, init_y 50 with drive_inst_3
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

# imports for plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.seterr(all='raise')

# Setup Manual Inputs (HARD CODES)
test_drive_instr = routes.drive_mini_1
attempt_return = False
saving_data = True
draw_path = True
init_x, init_y = 0, 0

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
def update_position(left_prev, right_prev, vel_prev, mu_control_prev, mu_sensor_prev, cov, time_prev):
    """Update position using two sources of information; control and sensors.
    The sensor data comes from the imu/gyroscope and the control comes from the
    odometers.

    nu is translational velocity in cm per second
    omega is Rotational Velocity in radians per second

    scales is a tuned parameter that turns the incoming odometer units to
    centimeters.

    :param left_prev:
    :param right_prev:
    :param vel_prev:
    :param mu_control_prev:
    :param mu_sensor_prev:
    :param cov:
    :param time_prev:
    :return:
    """
    # Get new measurements
    new_reading = get_reading(read_mag=False)
    # pprint(new_reading)
    delta_time = (new_reading.get('time') - time_prev).total_seconds()

    # Initialize
    # Get 'r' from encoders and scale to centimeters
    theta_control_prev = mu_control_prev[2, 0]
    theta_sensor_prev = mu_sensor_prev[2, 0]
    scale = 0.0577 * 2 * 10e-3  # Odometer units to centimeters, 20e-3 is magic number
    left_delta = new_reading.get('left_enc') - left_prev
    right_delta = new_reading.get('right_enc') - right_prev
    # scale * average encoder advancement / time_elapsed
    nu_control = scale * (left_delta + right_delta) / (2 * delta_time)  # should be cm/s

    # TODO: Test the below decompositions, then refactor
    # Calibration from 7/19 [0.554, -0.235, 1.755]
    accel_forward = (new_reading.get('accel_z') - 1.755) 
    accel_side = (new_reading.get('accel_x') - 0.554)
        
    vel_now = vel_prev + delta_time * np.array([
        accel_forward * np.sin(theta_sensor_prev) + accel_side * np.cos(theta_sensor_prev),
        accel_forward * np.cos(theta_sensor_prev) + accel_side * np.sin(theta_sensor_prev)
    ])
    
    # TODO: Decompose back to velocity in forward direction
    # Total velocity is L2 Norm
    # nu_sensor?
    # nu_sensor = np.sqrt(vel_now[0]**2 + vel_now[1]**2)
    nu_sensor = np.abs(np.sin(theta_sensor_prev) * vel_now[0]) + np.abs(np.cos(theta_sensor_prev) * vel_now[1])

    # Theta from Odometer
    rotation_scale = 5.5
    theta_delta_control = (left_delta - right_delta) / rotation_scale
    theta_control_new = theta_control_prev + theta_delta_control
    omega_control = theta_delta_control * np.pi / (180 * delta_time)

    # Theta from Gyroscope
    omega_sensor = -1 * new_reading.get('gyro_y') * np.pi / 180
    theta_delta_sensor = omega_sensor * delta_time
    theta_sensor_new = theta_sensor_prev + theta_delta_sensor

    if np.abs(omega_control) > 10e-4:
        omega_control_star = omega_control
        theta_control_new_star = theta_control_prev + theta_delta_control
    else:
        omega_control_star = 10e-4
        theta_control_new_star = theta_control_prev + 10e-4 * delta_time

    r_control = nu_control / omega_control_star

    if np.abs(omega_sensor) > 10e-4:
        omega_sensor_star = omega_sensor
        theta_sensor_new_star = theta_sensor_prev + theta_delta_sensor
    else:
        omega_sensor_star = 10e-4
        theta_sensor_new_star = theta_sensor_prev + 10e-4 * delta_time

    r_sensor = nu_sensor / omega_sensor_star

    # r_control = nu_control / omega_control_star if np.abs(omega_control) > 10e-6 else nu_control / 10e-6
    # r_sensor = nu_sensor / omega_sensor if np.abs(omega_sensor) > 10e-6 else nu_sensor / 10e-6
    # r_control = nu_control * delta_time
    # r_sensor = nu_sensor * delta_time

    mu_control_new = mu_control_prev + np.array([
        [r_control * (np.sin(theta_control_new_star) - np.sin(theta_control_prev))],
        [r_control * (np.cos(theta_control_prev) - np.cos(theta_control_new_star))],
        [omega_control * delta_time]
    ])

    mu_sensor_new = mu_sensor_prev + np.array([
        [r_sensor * (np.sin(theta_sensor_new_star) - np.sin(theta_sensor_prev))],
        [r_sensor * (np.cos(theta_sensor_prev) - np.cos(theta_sensor_new_star))],
        [omega_sensor * delta_time]
    ])

    if i % 10 == 0:
        print("Control", nu_control, omega_control)
        print(mu_control_prev, mu_control_new)

        print("Sensor", nu_sensor, omega_sensor)
        print(mu_sensor_prev, mu_sensor_new)

    velocities = {
        'nu_control': nu_control,
        'omega_control': omega_control,
        'nu_sensor': nu_sensor,
        'omega_sensor': omega_sensor,
    }

    return (
        new_reading.get('left_enc'),
        new_reading.get('right_enc'),
        vel_now,
        mu_control_new,
        mu_sensor_new,
        cov,  # Sigma
        new_reading.get('time'),
        velocities
    )


# Initialize Measurements for drive
i = 0
data = []
drive_messages = []
init_pose = np.array([
    [init_x],
    [init_y],
    [get_reading().get('euler_x') * np.pi / 180]
])
print(init_pose)
pose_sensor = init_pose
pose_control = init_pose

velocity = np.array([0, 0])
cov = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
left_prev = 0
right_prev = 0
curr_time = datetime.now()

# Start Driving
drive_process.start()

# Measure while driving loop
while i < 100:
    # mu is 3 x 1 pose
    left_prev, right_prev, velocity, pose_control, pose_sensor, cov, curr_time, velocities = update_position(
        left_prev, right_prev, velocity, pose_control, pose_sensor, cov, curr_time
    )
    # print(pose)
    data.append({
        # "t": str(curr_time),
        "t": curr_time.timestamp(),
        "x_control": pose_control[0][0],
        "y_control": pose_control[1][0],
        "theta_control": pose_control[2][0],
        "x_sensor": pose_sensor[0][0],
        "y_sensor": pose_sensor[1][0],
        "theta_sensor": pose_sensor[2][0],
        "nu_control": velocities.get('nu_control', 0),
        "omega_control": velocities.get('omega_control', 0),
        "nu_sensor": velocities.get('nu_sensor', 0),
        "omega_sensor": velocities.get('omega_sensor', 0),
    })

    while not q.empty():
        message = q.get()
        print(message)
        drive_messages.append(message)

    # Prepare for next iteration
    i += 1
    time.sleep(.0625)

if draw_path:
    max = 0
    for element in data:
        if np.abs(element.get('x_control')) > max:
            max = np.abs(element.get('x_control'))
        if np.abs(element.get('y_control')) > max:
            max = np.abs(element.get('y_control'))
        if np.abs(element.get('x_sensor')) > max:
            max = np.abs(element.get('x_sensor'))
        if np.abs(element.get('y_sensor')) > max:
            max = np.abs(element.get('y_sensor'))
    
    # Save a plot and pandas generated csv
    plt.style.use('seaborn-whitegrid')
    df = pd.DataFrame(data)
    fig = plt.figure()
    plt.xlim(-max * 1.1, max * 1.1)
    plt.ylim(-max * 1.1, max * 1.1)
    plt.plot(df.y_sensor, df.x_sensor, 'o', color='blue')
    plt.plot(df.y_control, df.x_control, 'o', color='green')
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
    with open('data.json', 'w') as f:
        json.dump(data, f)
        
    with open('drive_messages.json', 'w') as f:
        json.dump(drive_messages, f)
