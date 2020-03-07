import math as math
import numpy as np
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

imu = InertialMeasurementUnit(bus="GPG3_AD1")


class Demo:
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta

    def get_pose(self):
        return self.x, self.y, self.theta

    def reset_position(self):
        self.x = 0
        self.y = 0

    def update_from_position(self, r):
        pass



def get_position(right_prev, left_prev):
    euler_x = imu.read_euler()[0]

    # Ensure gpg.read_encoders is returning tuple of (left, right)
    left_enc, right_enc = gpg.read_encoders()
    y_delta = left_enc - left_prev
    x_delta = right_enc - right_prev
    y = math.sin(euler_x * 0.0174533) * y_delta
    x = math.cos(euler_x * 0.0174533) * x_delta
    return left_enc, right_enc, x, y


def return_to_point(curr_pose, destination):
    """Determine bearing and distance to a point of return

    for now assuming 0, 0 is the destination
    :param curr_pose: x, y, theta of origin position
    :param destination: x, y of destination
    :return:
    """
    # TODO: Incorporate specific coordinate of return
    # TODO: ensure current heading is taken into account for return
    distance_back = math.sqrt(curr_pose[0] ** 2 + curr_pose[1] ** 2)
    direction_back = np.arctan2(curr_pose[0], curr_pose[1])
    return distance_back, direction_back


def drive_home(rot, dist):
    gpg.turn_degrees(rot)
    gpg.drive_cm(dist/10)
    # gpg.drive_cm(distance_back/44*2.54)
    gpg.stop()
