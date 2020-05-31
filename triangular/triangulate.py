#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 19:52:25 2020

@author: gajananganji
"""

#from matplotlib import pyplot as plt
import numpy as np
import warnings
import argparse
import time
import sys
import math
import csv
from statistics import mean
from datetime import datetime
from bt_proximity import BluetoothRSSI


warnings.filterwarnings('ignore')

cone_position_est = (34, 28)  # coordinates of sheet center
camera_locs = [(34.5, 57.5), (0, 0), (69, 0)]  # tbd based on real locations
#distances = [38.75, 48.5, 25.5]  # just a made-up sample
# find_position(cone_position_est, camera_locs, distances)

#['48:60:5F:F5:1E:1E'],['34:2D:0D:9B:5A:5D'] ['88:9F:6F:BA:C6:31']
# You can put your Bluetooth address here.  E.g: 'a4:70:d6:7d:ee:00'
bt_addr     = {0:'DC:A6:32:11:E7:D3'}#,
               #1:'DC:A6:32:30:AF:0C',
               #2:'DC:A6:32:11:EB:A7',
              #} 

n           = {0:1.5}#, 1:1.5, 2:1.5}
c           = {0:0}#, 1:0, 2:0}
A0          = {0:0.05}#, 1:0.05, 2:0.05}
actual_dist = {0:100}#, 1:100, 2:100}
sum_error   = {0:0}#, 1:0, 2:0}
count       = {0:0}#, 1:0, 2:0}


num_loop    = 30

def csv_list(string):
    return string.split(',')


def get_params():
    """
    Parse the arguments passed to program
    """

    parser = argparse.ArgumentParser(description='Triangulate using Bluetooth signal strength')
    parser.add_argument('-t', '--time', dest='duration', required=True, help='Time in minutes to keep the program running')
    # parser.add_argument('-o', '--out_dir', dest='out_dir', required=True, help='')
    # parser.add_argument('-d', '--dict', dest='dictionary', required=True, help='')
    # parser.add_argument('-y', '--yaml', dest='yaml_files', type=csv_list, default=[], help='')
    # parser.add_argument('-tt', '--term', dest='terms_file', action='store_true', help='')

    args = parser.parse_args()

    return args


# MSE equation
def mse_dist(cone_position_est, camera_locs, distances):
    '''
    Calulate MSE for estimated cone position and known camera locations
    -------------------------------------------------------------------
    cone_position = estimated cone coordinates (X, Y)
    camera_locs = (x_i, y_i) for each camera
    distances = d_i calculated from image for each camera

    Returns: MSE for the estimated cone position
    '''
    sse = float(0)
    for loc, dist in zip(camera_locs, distances):
        dist_est = np.sqrt((cone_position_est[0] - loc[0])**2 + (cone_position_est[1] - loc[1])**2)
        sse += (dist - dist_est)**2
    mse = sse/(len(distances))
    return mse


# minimization step
#def find_position(cone_position_est: tuple, camera_locs: list, distances: list):
def find_position(cone_position_est, camera_locs, distances):
    from scipy.optimize import minimize
    position = minimize(mse_dist, cone_position_est, args=(camera_locs, distances),
                        options={'ftol':1e-5, 'maxiter':1e+7})
    return position.x


def plot_graph(x1,y1,x2,y2):

    # x1 = [1, 2, 3, 4]
    # y1 = [2, 2.5, 5, 7.4]
    # x2 = [1.2, 2.9, 5.3, 8.9]
    # y2 = [0.9, 3.7, 6.2, 7.1]
    plt.plot(x1,y1,'b.', x2,y2,'r^')
    plt.ylabel('some numbers')
    plt.xlabel('some numberX')
    plt.axis([0, 10, 0, 10])
    plt.show()



def calc_distance(num_loop, bt_addr, n, c, A0, actual_dist, sum_error, count):
    btrssi = {}
    for k, bta in bt_addr.items():
        btrssi[k] = BluetoothRSSI(addr=bta)
    
    #n=1.5    #Path loss exponent(n) = 1.5
    #c = 10   #Environment constant(C) = 10
    #A0 = 2   #Average RSSI value at d0
    #actual_dist = 37   #Static distance between transmitter and Receiver in cm
    #sum_error = 0
    #count = 0
    print(btrssi)
    distances = {}
    
    for k in btrssi:
        distances[k]=[]
        
    for i in range(1, num_loop):
        rssi_bt = {}
        for k, btr in btrssi.items():
            #print k,btr
            try:
                btr_val = float(btr.get_rssi())
            except:
                btr_val = -999999
            print(btr_val)
            rssi_bt[k] = btr_val
        
        #if(rssi_bt1!=0 and i>10):                    #reduces initial false values of RSSI using initial delay of 10sec
        #    count=count+1
        #distance = []
        #avg_error = []
        #error = []
        
        for k, val in rssi_bt.items() :#range(len(rssi_bt)):
            if val != -999999:
                x = float( (val - A0[k]) / (-10 * n[k]) )         #Log Normal Shadowing Model considering d0 =1m where
                dist = ( math.pow(10,x) * 100 ) + c[k]
                distances[k].append(dist)
            
        #error = abs(actual_dist - distance)
        #sum_error = sum_error + error
        #avg_error = sum_error/count
        #print "Average Error=  " + str(avg_error)
        #print "Error=  " + str(error)
        #print btrssi
        #print bt_addr
        #print "Approximate Distance:" + str(dist)
        #print "RSSI: " + str(rssi_bt)
        #print "Count: " + str(count)
        #print " "
        #time.sleep(1)
    
    distances_list = []
    
    for k in sorted(distances.keys()):
        distances_list.append(mean(distances[k]))
    print ('distance_list', distances_list)
    return distances_list


#Shree Pi = {n:1.5, c: 0, A0:0.05}
'''
def main():

    temp_st_time = datetime.now()
    args         = get_params()

    duration       = args.duration
    # out_dir      = args.out_dir
    # dictionary   = args.dictionary
    # yaml_files   = args.yaml_files
    # terms_file   = args.terms_file
    
    calc_distance(num_loop, bt_addr, [1.5], [0], [0.05], [100], [0], [0])
    #calc_distance(num_loop, bt_addr, n, c, A0, actual_dist, sum_error, count)
    
    cycle_duration = 30  # identify how much time it takes to complete one round
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    num_cycles = int(math.ceil((int(duration) * 60) /cycle_duration))

    for i in range(num_cycles):
        print(i)
        # calculate distances
        # distances = calc_distance(num_loop, bt_addr, [1.5], [10], [2], [37], [0], [0])
        
        # calculate x, y
        coordinates = find_position(cone_position_est, camera_locs, distances)
        print(coordinates)

        x1.append(coordinates[0])
        y1.append(coordinates[1])

        print x1
        print y1
    # plot_graph(x1,y1,x2,y2)
    
    temp_fin_time = datetime.now()
    
    print 'Total time: ', str(temp_fin_time - temp_st_time)
    
    print 'sleeping now ...'
    time.sleep(5.73)
    
    print 'waking now ....'
    
    temp_t = datetime.now()
    
    print 'Total time: ', str(temp_t - temp_fin_time)
    
'''

def main():

    temp_st_time = datetime.now()
    time_diff    = temp_st_time - temp_st_time
    args         = get_params()

    duration       = int(args.duration)
    
    # calc_distance(num_loop, bt_addr, n, c, A0, actual_dist, sum_error, count)
    btrssi = BluetoothRSSI(addr=bt_addr[0])
    print(btrssi)
    print(btrssi.get_rssi())
    
    '''
    ts = []
    x1 = []
    y1 = []
    print('starting time diff', time_diff.total_seconds())
    while(time_diff.total_seconds() < (duration)): #* 60)):
        
        ts.append(str(datetime.now()))
        
        # calculate distances
        distances = calc_distance(num_loop, bt_addr, n, c, A0, actual_dist, sum_error, count)
        
        # calculate x, y
        coordinates = find_position(cone_position_est, camera_locs, distances)
        #print(coordinates)

        x1.append(coordinates[0])
        y1.append(coordinates[1])

        #print x1
        #print y1
    
        #time.sleep(10)
        temp_fin_time = datetime.now()
    
        time_diff = temp_fin_time - temp_st_time
        print('timediff now', time_diff.total_seconds(), duration * 60, time_diff.total_seconds()< duration*60, ts, x1, y1 )
    
    with open('pi_positioning_bluetooth.tsv', 'w+') as txt_file1:
        file_writer = csv.writer(txt_file1, delimiter='\t', lineterminator='\n')
        file_writer.writerow(['timestamp', 'X_coordinate','Y_coordinate'])
    
        for i in range(len(ts)):
            file_writer.writerow([ts[i], x1[i],y1[i]])
        
    print ('Total time: ', str(time_diff))

    # plot_graph(x1,y1,x2,y2)
    '''

    
if __name__ == '__main__':
    main()
