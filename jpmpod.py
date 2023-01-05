#!/bin/env python3

# John Haggerty, BNL
# 2021.03.10

import justpy as jp
import pandas as pd
import time
import asyncio
from hvcontrol import *

mpod_ip = 'a.b.c.d'
nslots = 8

wp = jp.WebPage(delete_flag=False)
wp.title = 'HCAL Bias'

properties = ['outputVoltage', 'outputMeasurementSenseVoltage', 'outputCurrent', 'outputMeasurementCurrent']
column_names = properties.copy()
column_names.insert(0,'Channel')

header_div = jp.Div(text='HCAL Bias Supply', a=wp, classes = 'text-5xl text-white bg-blue-500 hover:bg-blue-700 m-1')
time_div = jp.Div(a=wp, classes = 'text-1xl text-white bg-blue-500 hover:bg-blue-700 m-1')
the_time = jp.P(a=time_div)

data_div = jp.Div(a=wp)
gridv = jp.AgGrid(a=data_div)
gridv.options.pagination = False
gridv.options.paginationAutoPageSize = True

async def voltages():
    while True:
        the_time.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
        all_readings = []
        for s in range(nslots):
            for c in range(8):
                channel_data = []
                channel_data.append('Slot '+str(s)+' Channel '+str(c))
                for p in properties:
                    channel_data.append( readchannel(p,s,c,mpod_ip) )
#                print(channel_data)   
                all_readings.append(channel_data)
#                print(all_readings)        
        dfreadings = pd.DataFrame(all_readings,columns=column_names)
        dfreadings[['outputCurrent']] *= 1000000
        dfreadings[['outputMeasurementCurrent']] *= 1000000
        gridv.load_pandas_frame(dfreadings)
        jp.run_task(wp.update())
        await asyncio.sleep(1)

async def voltages_init():
    jp.run_task(voltages())

async def voltages_test():
    return wp

jp.justpy(voltages_test, startup=voltages_init)
