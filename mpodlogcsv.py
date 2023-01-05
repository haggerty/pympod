#!/bin/env python3

# John Haggerty, BNL
# 2021-04-29

import time
import asyncio
from hvcontrol import *
import csv

mpod_ip = 'a.b.c.d'
nslots = 8

properties = ['outputVoltage', 'outputMeasurementSenseVoltage', 'outputCurrent', 'outputMeasurementCurrent']
while True:
    file = open('mpod.csv', 'a', newline ='')
    all_channels = []
    utime = time.time()    
    for s in range(nslots):
        for c in range(8):
            channel_data = []
            channel_data.append(utime)
            channel_data.append(s)
            channel_data.append(c)
            for p in properties:
                channel_data.append( float(readchannel(p,s,c,mpod_ip)) )
            all_channels.append( channel_data )    
#            print(channel_data)   
    with file:    
        write = csv.writer(file)
        write.writerows(all_channels)

    time.sleep(10)       
