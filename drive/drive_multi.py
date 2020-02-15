import atexit
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from drive.utils import get_reading


gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop())

num = 5
while num > 0:
    gpg.forward()
    gpg.sleep(.15)
    gpg.turn_degrees(10)
    num -= 1
