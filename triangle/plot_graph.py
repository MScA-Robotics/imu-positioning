#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 08:44:53 2020

@author: gajananganji
"""

import csv
from matplotlib import pyplot as plt

def plot_graph(ts1, x1, y1, ts2, x2, y2):

    # x1 = [1, 2, 3, 4]
    # y1 = [2, 2.5, 5, 7.4]
    # x2 = [1.2, 2.9, 5.3, 8.9]
    # y2 = [0.9, 3.7, 6.2, 7.1]
    plt.plot(x1,y1,'bo-', x2,y2,'r^-')
    
    for i in range(len(ts1)):
        # plt.text(x1[i],y1[i],'({0},{1}) - s{3}'.format(x1[i],y1[i],ts1[i]))
        plt.annotate('({0},{1}) - {3}'.format(x1[i],y1[i],ts1[i]), # this is the text
                     (x1[i],y1[i]), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    
    for i in range(len(ts2)):
        # plt.text(x2[i],y2[i],'({0},{1}) - s{3}'.format(x2[i],y2[i],ts2[i]))
        plt.annotate('({0},{1}) - {3}'.format(x2[i],y2[i],ts2[i]), # this is the text
                     (x2[i],y2[i]), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.axis([0, 10, 0, 10])
    plt.show()


def main():
    ts1 = []
    x1  = []
    y1  = []
    ts2 = []
    x2  = []
    y2  = []
    
    with open('pi_positioning_bluetooth.tsv', 'r') as master:
        csvreader = csv.reader(master, quotechar="'", delimiter='\t', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        next(csvreader)
        for row in csvreader:
            ts1.append(row[0])
            x1.append(row[1])
            y1.append(row[2])
    
    with open('pi_positioning_rotation.tsv', 'r') as master:
        csvreader = csv.reader(master, quotechar="'", delimiter='\t', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        next(csvreader)
        for row in csvreader:
            ts2.append(row[0])
            x2.append(row[1])
            y2.append(row[2])
    
    plot_graph(ts1, x1, y1, ts2, x2, y2)
        
    
    
if __name__ == '__main__':
    main()
    