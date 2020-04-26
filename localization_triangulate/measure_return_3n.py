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
from drive.routes import drive_inst_1, drive_inst_2
### imports for plotting
import math as math
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np


# Setup Manual Inputs (HARD CODES)
test_drive_instr = drive_inst_1
attempt_return = False
saving_data = False
draw_path=True

# Setup Sensors
imu = InertialMeasurementUnit(bus="GPG3_AD1")
gpg = EasyGoPiGo3()
gpg.reset_encoders()
atexit.register(gpg.stop)

drive_process = multiprocessing.Process(
    name='drive',
    target=test_drive_instr
)


def get_position(right_prev,left_prev,euler_x_prev,theta_prev):

    euler = imu.read_euler()
    euler_x=euler[0]

    encoder = gpg.read_encoders()
    left_enc=encoder[0]
    right_enc= encoder[1]
    lr_delta=left_enc-right_enc
    y_delta=left_enc-left_prev
    x_delta=right_enc-right_prev
    lr_avg=(x_delta+y_delta)/2
    if(abs(lr_delta)>2):
        
        theta_delta=euler_x-euler_x_prev
    else:
        theta_delta=0
    theta=theta_prev+theta_delta
    x=math.sin(theta*0.0174533)*lr_avg
    y=math.cos(theta*0.0174533)*lr_avg
    read_distance = 0
    res = {


        "x": x,
        "y": y

        
    }
    ##print(res)
    return left_enc,right_enc,x,y,res,euler_x,theta


# Initialize Measurements for drive
i=0
t1 = datetime.now()
data = []
right_prev=0
left_prev=0
x_total=0
y_total=0
euler = imu.read_euler()
euler_x_prev=euler[0]
theta_prev=0

# Start Driving
drive_process.start()

# Measure while driving loop
while  i<100:
    # Execute
    ##print_reading()
    #data.append(get_reading())
    
    t2 = datetime.now()
    left_enc,right_enc,x,y,res,euler_x,theta=get_position(right_prev,left_prev,euler_x_prev,theta_prev)
    euler_x_prev=euler_x
    theta_prev=theta
    right_prev=right_enc
    left_prev=left_enc
    x_total=x_total+x
    y_total=y_total+y
    ##print("x= %2.2f, y=%2.2f, dx= %2.2f, dy=%2.2f, euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44,x/44, y/44, euler_x,theta))
    print("x= %2.2f, y=%2.2f,  euler==%2.2f  theta==%2.2f " % (x_total/44, y_total/44, euler_x,theta))
    ##print(imu.read_euler()[0])
    ##print("Duration: {}".format(t2 - t1))
    # print(timedelta(t2, t1))
    res2 = {

        "t":str(t2),
        "x": x_total  ,
        "y": y_total

        
    }
    data.append(res2)
    
    # Prepare for next iteration
    i += 1
    t1 = t2
    time.sleep(.1)

print (data[1])
    

print ("printing path")
plt.style.use('seaborn-whitegrid')
df = pd.DataFrame(data) 
#'lr_delta': -1, 'euler_x': 240.4375, 'left_enc': 2585, 'y': 4.216956575971679, 'theta': -32.5, 'x_delta': 4, 'right_enc': 2586, 'x': -2.6864990668841138, 'y_delta': 6
##print(df[1])
print(df.head())
##df.columns = ['lr_delta','euler_x',"left_enc","y",'theta','x_delta','right_enc','x','y_delta']
fig = plt.figure()
plt.plot(df.x, df.y, 'o', color='black')
fig.savefig('plot.png')
df.to_csv("df.csv", index=False)      


if attempt_return:
    ##print(imu.read_euler()[0]) 
    distance_back=math.sqrt(x_total*x_total+y_total*y_total)

    direction_back=90-theta+90+90

    print("Back direction= %8.2f dist=%8.2f" % (direction_back, distance_back/44))


    gpg.turn_degrees(direction_back)
    print("back inc= %8.2f back cm=%8.2f" % (distance_back/44, distance_back/44*2.54))
    ###gpg.drive_cm(distance_back/44*2.54)  
    gpg.stop()  
    # Save Out
    #with open('data.pkl', 'wb') as f:
        #pickle.dump(data, f)

if saving_data:
    # Save Out
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)


#### run file python3 -m measure.measure_return_3
