from __future__ import print_function
from __future__ import division
import multiprocessing
import time
from datetime import datetime, timedelta

from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import print_reading, get_reading
from drive.control import get_position, drive_home, return_to_point
from drive.routes import drive_inst_1
import numpy as np
import math as math


# Setup Sensors
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()

drive_process = multiprocessing.Process(
    name='drive',
    target=drive_inst_1
)

# Initialize Measurements for free drive
i = 0
t1 = datetime.now()
data = []
right_prev = 0
left_prev = 0
x_total = 0
y_total = 0

position = Pose(x=0, y=0, theta=0)
position.get_bearing()

pos_array = [0, 0, 0]


# Free Drive
while i < 100:
    # Execute
    # print_reading()
    # data.append(get_reading())
    t2 = datetime.now()
    left_enc, right_enc, x, y = get_position(right_prev, left_prev)
    
    right_prev, left_prev = right_enc, left_enc
    x_total += x
    y_total += y
    print("x (mm) = %8.2f y (mm) = %8.2f" % (x_total, y_total))
    # print(imu.read_euler()[0])
    # print("Duration: {}".format(t2 - t1))
    # print(timedelta(t2, t1))

    # Prepare for next iteration
    i += 1
    t1 = t2
    time.sleep(.1)

# Stop motors and calculate return
gpg.stop()

# print direction_back, aka pointing vector direction CW deg angle from north
# and distance back, aka pointing vector magnitude
# print(imu.read_euler()[0])
distance_back, direction_back = return_to_point((x_total, y_total, 0))
direction_back = np.arctan2(y_total, x_total)
print("return direction (deg CW from north) = %8.2f distance (mm) = %8.2f" % (direction_back, distance_back))

# may need to deal with dividing by zero when x_total = 0

#  find rotation, the CW rotation needed to go from pointing vector to return vector
# quadrant independent method
# euler heading = bearing = yaw CW from north
# x_total is x position in mm where x direction is north
# y is west
bearing = imu.read_euler()[0] * math.pi / 180
phi = np.arctan2(y_total, x_total)
# math.pi, bearing, and phi in radians, rotation in deg
rotation = -((math.pi + bearing + phi) * 180/math.pi)
rotation = rotation % 360
print("current yaw CW from north = %8.2f rotation = %8.2f" % (bearing, rotation))

# angle=imu.read_euler()[0]
# angle_delta=direction_back-angle
# print("current= %8.2f delta=%8.2f" % (angle, angle_delta))

# while angle_delta > 1:
#     angle = imu.read_euler()[0]
#     angle_delta = direction_back-angle
#     gpg.right()
#     time.sleep(.1)
#     gpg.stop()
#     print("current= %8.2f delta=%8.2f" % (angle, angle_delta))

print("return distance (mm) = %8.2f" % distance_back)
return_home(rotation, distance_back)

# Save Out
# with open('data.pkl', 'wb') as f:
#     pickle.dump(data, f)
