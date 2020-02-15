"""IMU Accelerometer Integration


"""
import os
import pickle
import numpy as np
import pandas as pd

pd.set_option('max_rows', 200)
pd.set_option('max_columns', 20)


class IMUReading:
    current_position = np.zeros(3)
    current_velocity = np.zeros(3)
    time_step = 0.05

    def __init__(self, sd):
        """Initialize with sensor dictionary

        :param sd:sensor dictionary
        """
        self.accel = np.array([sd['accel_x'], sd['accel_y'] - 9.81, sd['accel_z']])
        self.update_velocity()
        self.update_position()

    def __repr__(self):
        return (
            f'acceleration: {self.accel}\n'
            f'velocity: {IMUReading.current_velocity}\n'
            f'position: {IMUReading.current_position}'
        )

    @staticmethod
    def reset():
        IMUReading.current_position = np.zeros(3)
        IMUReading.current_velocity = np.zeros(3)

    def update_velocity(self):
        IMUReading.current_velocity += self.accel * IMUReading.time_step

    @staticmethod
    def update_position():
        IMUReading.current_position += IMUReading.current_velocity * IMUReading.time_step


file_path = os.path.join(os.getcwd(), 'exvivo', 'data')

with open(os.path.join(file_path, '2fn.pkl'), 'rb') as intpkl:
    forward_1 = pickle.load(intpkl)

f1df = pd.DataFrame(forward_1)
f1df

for reading in forward_1:
    imu_reading = IMUReading(reading)
    print(imu_reading)

IMUReading.reset()

with open(os.path.join(file_path, '2fe.pkl'), 'rb') as intpkl:
    forward_1 = pickle.load(intpkl)

for reading in forward_1:
    imu_reading = IMUReading(reading)
    print(imu_reading)


forward_1[0]

read_1 = IMUReading(forward_1[0])
read_1


read_2 = IMUReading(forward_1[1])
read_2
print(read_2)
