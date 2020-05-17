import numpy as np
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

imu = InertialMeasurementUnit(bus="GPG3_AD1")


class Pose:
    """
    x in cm
    y in cm
    theta in degrees clock wise of (0,1)
    """
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.theta)

    def __repr__(self):
        return "<({}, {}, {})>".format(self.x, self.y, self.theta)

    def get_pose(self):
        return self.x, self.y, self.theta

    def reset_position(self):
        self.x = 0
        self.y = 0

    def update_from_position(self, r):
        pass

    def return_to_point(self, return_loc):
        dx, dy = return_loc[0] - self.x, return_loc[1] - self.y
        distance_back = np.sqrt(dx ** 2 + dy ** 2)
        print(np.arctan2(dy, dx))
        direction_back = np.arctan2(dy, dx) + self.theta
        return distance_back, direction_back


def get_position(right_prev, left_prev):
    euler_x = imu.read_euler()[0]

    # Ensure gpg.read_encoders is returning tuple of (left, right)
    left_enc, right_enc = gpg.read_encoders()
    y_delta = left_enc - left_prev
    x_delta = right_enc - right_prev
    y = np.sin(euler_x * 0.0174533) * y_delta
    x = np.cos(euler_x * 0.0174533) * x_delta
    return left_enc, right_enc, x, y


def return_to_point(pose, destination=(0, 0)):
    """Determine bearing and distance to a point of return

    Numpy arctan2 reference
     https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html
    for now assuming 0, 0 is the destination
    :param pose: x, y, theta of origin position
    :param destination: x, y of destination or desired end pose
    :return:
    """
    dx, dy = destination[0] - pose.x, destination[1] - pose.y
    distance_back = np.sqrt(dx ** 2 + dy ** 2)
    direction_back = np.arctan2(dy, dx) + pose.theta
    return distance_back, direction_back


def drive_home(rot, dist):
    gpg.turn_degrees(rot)
    gpg.drive_cm(dist/10)
    # gpg.drive_cm(distance_back/44*2.54)
    gpg.stop()
