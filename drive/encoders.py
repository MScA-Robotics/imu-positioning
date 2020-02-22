import math as math
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

imu = InertialMeasurementUnit(bus="GPG3_AD1")


def get_position(right_prev, left_prev):
    euler_x = imu.read_euler()[0]

    # Ensure gpg.read_encoders is returning tuple of (left, right)
    left_enc, right_enc = gpg.read_encoders()
    y_delta = left_enc - left_prev
    x_delta = right_enc - right_prev
    y = math.sin(euler_x * 0.0174533) * y_delta
    x = math.cos(euler_x * 0.0174533) * x_delta
    return left_enc, right_enc, x, y
