#!/bin/env python3
import subprocess
import re

ip_default = 'a.b.c.d'

def readmodule(  what = 'outputMeasurementVoltage', slot = 0, ip = ip_default ): 

    nchmod = 8
    getter = ['snmpget', 
   '-OqvU', 
   '-v', 
   '2c', 
   '-M', 
   '+/home/phnxrc/haggerty/MIBS', 
   '-m', 
   '+WIENER-CRATE-MIB', 
   '-c', 
   'public', 
   ip,
   'outputMeasurementSenseVoltage.u0']
    getter[-2] = ip

    readback = []
    for channel in range(nchmod):
        channel_id = slot*100 + channel
        getter[-1] = what+'.u'+str(channel_id)
#        print(getter)
        answer = subprocess.run(getter, 
                universal_newlines=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
#        print(answer.stdout)
        x = re.findall('\d*\.?\d+',answer.stdout)
        rb = float(x[0])
#        print(rb)
        readback.append(rb)

#    print(readback)
    return readback


def readchannel(  what = 'outputMeasurementVoltage', slot = 0, channel = 0, ip = ip_default ): 

    getter = ['snmpget', 
   '-OqvU', 
   '-v', 
   '2c', 
   '-M', 
   '+/home/phnxrc/haggerty/MIBS', 
   '-m', 
   '+WIENER-CRATE-MIB', 
   '-c', 
   'public', 
   ip,
   'outputMeasurementSenseVoltage.u0']
    getter[-2] = ip

    channel_id = slot*100 + channel
    getter[-1] = what+'.u'+str(channel_id)
#    print(getter)
    answer = subprocess.run(getter, 
            universal_newlines=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
#    print(answer.stdout)
    x = re.findall('\d*\.?\d+',answer.stdout)
    rb = float(x[0])
#    print(rb)

    return rb

def writechannel(  what = 'outputVoltage', 
    slot = 0, channel = 0, 
    type = 'F', value = 0.0, 
    ip = ip_default ): 

    setter = ['snmpset', 
   '-v', 
   '2c', 
   '-M', 
   '+/home/phnxrc/haggerty/MIBS', 
   '-m', 
   '+WIENER-CRATE-MIB', 
   '-c', 
   'guru', 
   ip,
   'ouputVoltage.u0',
   'F',
   '0.0']
    
    setter[-1] = str(value)
    setter[-2] = type
    setter[-3] = what
    setter[-4] = ip

    channel_id = slot*100 + channel
    setter[-3] = what+'.u'+str(channel_id)
#    print(setter)
    answer = subprocess.run(setter, 
             universal_newlines=True, 
             stdout=subprocess.PIPE, 
             stderr=subprocess.PIPE)
#    print(answer.stdout)
    x = re.findall('\d*\.?\d+',answer.stdout)
    rb = float(x[0])
#    print(rb)
    return rb

def main():

    what = 'outputVoltage'
    print(what)
    response = writechannel(what,0,0,'F',66.0)
    print(response)

    module = readmodule(what, 0) 
    print(module)
    
    channel = readchannel(what,0,0)
    print(channel)

if __name__ == "__main__":
    main()
