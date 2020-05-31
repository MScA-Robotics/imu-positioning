import easygopigo3 as easy
#import di_sensors
import time

gpg = easy.EasyGoPiGo3()

my_distance_sensor = gpg.init_distance_sensor()
print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
# my_imu = gpg.init_motion_sensor()
# my_imu.read()
#
# for i in range(100):
#    print(my_imu.read())
#     time.sleep(.1)
