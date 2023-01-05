#!/bin/env python3

import pandas as pd
from hvcontrol import *

properties = ['outputVoltage', 'outputMeasurementSenseVoltage', 'outputCurrent', 'outputMeasurementCurrent']
nslots = 8
ip = 'a.b.c.d'
all_readings = []
for s in range(nslots):
    for c in range(8):
        channel_data = []
        for p in properties:
            channel_data.append( readchannel(p,s,c,ip) )
            print(channel_data)   
            all_readings.append(channel_data)
print(all_readings)        
dfreadings = pd.DataFrame(all_readings,columns=properties)
