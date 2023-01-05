#!/bin/env python3

from hvcontrol import *

import sys
import time
from ROOT import TFile, TTree, TObject
from array import array
import datetime
import os.path

rootfile = 'mpodlog.root'
rootfile_exists = os.path.isfile(rootfile)

if rootfile_exists:
    print('appending to ',rootfile)
    f = TFile( rootfile, 'update' )
    MPOD = f.Get("MPOD")
else:
    print('creating new ',rootfile)
    f = TFile( rootfile, 'recreate' )
    MPOD = TTree( 'MPOD', 'HCAL bias' )

start = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

t = array( 'd', [ 0.0 ] )
slot = array( 'i', [0] )
channel = array( 'i', [0] )
vset = array( 'd', [0] )
vmeas = array( 'd', [0] )
ilimit = array( 'd', [0] )
imeas = array( 'd', [0] )

if rootfile_exists:
    MPOD.SetBranchAddress('time',t);
    MPOD.SetBranchAddress('slot',slot);
    MPOD.SetBranchAddress('channel',channel);
    MPOD.SetBranchAddress('vset',vset);
    MPOD.SetBranchAddress('vmeas',vmeas);
    MPOD.SetBranchAddress('ilimit',ilimit);
    MPOD.SetBranchAddress('imeas',imeas);
else:
    MPOD.Branch( 'time', t, 'time/D' )  
    MPOD.Branch( 'slot', slot, 'slot/I' )  
    MPOD.Branch( 'channel', channel, 'channel/I' )  
    MPOD.Branch( 'vset', vset, 'vset/D' )  
    MPOD.Branch( 'vmeas', vmeas, 'vmeas/D' )  
    MPOD.Branch( 'ilimit', ilimit, 'ilimit/D' )  
    MPOD.Branch( 'imeas', imeas, 'imeas/D' )  

properties = ['outputVoltage', 'outputMeasurementSenseVoltage', 'outputCurrent', 'outputMeasurementCurrent']

nslots = 8
ip = 'a.b.c.d'

t[0] = time.time()

all_readings = []
for s in range(nslots):
    for c in range(8):
        channel_data = []
        channel_data.append( s )
        channel_data.append( c )
        for p in properties:
            if 'current' in p.lower(): 
                channel_data.append( readchannel(p,s,c,ip)*1000000 )
            else:
                channel_data.append( readchannel(p,s,c,ip) )
        print(channel_data)   
        slot[0] = int(channel_data[0])
        channel[0] = int(channel_data[1])
        vset[0] = float(channel_data[2])
        vmeas[0] = float(channel_data[3])
        ilimit[0] = float(channel_data[4])
        imeas[0] = float(channel_data[5])
        MPOD.Fill()

f.Write("",TObject.kOverwrite)
f.Close()
