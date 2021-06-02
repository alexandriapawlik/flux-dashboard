#!/usr/bin/env python
#
# author: Alex Pawlik apawlik@umich
# read TOA5 files and update the storage of data into Pandas DataFrames
# code modified from campbellread_v2_0.py 
# obtained at https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/
# 
# this should help make it easier to input data into influxDB using influxDB-Python
# removed old read files for EDLOG dataloggers
# 20200205: toa5head has been updated
#
import sys
import re
import logging
import struct
import attr
from datetime import datetime, timedelta
import binascii
import numpy as np
import pandas as pd
# date used for base time on Campbell scientific data loggers.
csibasedate = '1990-01-01:000000'
csiepochstart=631152000  # seconds difference between unix epoch 1970-01-01,00:00:00 and CSI epoch 1990-01-01, 00:00:00

LOG = logging.getLogger(__name__)

def toa5head(filepth):
# included logic to handle TOACI1 files as well. These are not very common.

    lines=open(filepth,'rt').readlines()
    lineno=0
    line=lines[lineno]
    line=line[:-2]
    line=line.replace('"','')
    filetype=line.split(',')[0]
    
    lineno+=1
    line=lines[lineno]
    line=line[:-2]
    line=line.replace('"','')
    var_name=line.split(',') 
    lineno+=1
    if filetype=='TOA5':
        line=lines[lineno]
        line=line.replace('\n','')
        line=line.replace('\r','')
        line=line.replace('"','')
        units=line.split(',')
        lineno+=2
    data_only_var_name=var_name[2:]
    stamp=[]
    L=[]
    for i in range(len(data_only_var_name)): 
       L.append([]) 
    for line in lines[lineno:]:
        line=line.replace('"','')
        line=line.replace('\n','')
        line=line.replace('\r','')
        data_list=line.split(',')
        # time stamp for data
        stamp.append(data_list[0])
        # create a data only list
        data_only=data_list[2:]
 
# how do I deal with NAN in the data string
        for i,v in enumerate(data_only):
            try:
               dataval=float(v)
            except ValueError:
               dataval=float('nan')
        # fill in the list of list with data
            L[i].append(dataval)

    # make L a numpy array and transpose for insertion into Pandas dataframe
    L=np.transpose(np.array(L))
    stampIDX=pd.DatetimeIndex(stamp)
    records=pd.DataFrame(L,index=stampIDX,columns=data_only_var_name)
 #   records['ws']=np.sqrt(records.Ux * records.Ux + records.Uy * records.Uy)
 #   records['wd']=np.mod(np.arctan2(data.Uy,data.Ux) * 180/np.pi + 190,360)

    return records


def parse_csi_value(sval):
    """Parse a HEX string from data into a value using the CSI FP2 data format
    Each 16 bit hex values are defined as bit 1= polarity,
    bits 2-3 = decimal location
    bits 4-16 = data value
    """
    if sval:
       polarity=-1 if int(sval,16) & (1 << 15) else 1
       places = int(sval,16) >> 13 & 3
       value = float(int(sval,16) & 0x1FFF)

       return polarity*value/10**places
    else:
       return float('nan')


def readtob1file(fileptr):
    records=[]
    fileptr.seek(0)
    CSItypes = {'ULONG': 'I', 'IEEE4': 'f', 'FP2': '', 'UINT2': 'h', 'UINT4': 'I', 'IEEE4B':'f','USHORT':'H'}
    CSItypelen = {'ULONG': 4, 'IEEE4': 4, 'FP2': 2 ,'UINT2': 2, 'UINT4' : 4, 'IEEE4B':4,'USHORT':2}
    # read in the first five lines of file description
    infolines = []
    for i in range(5):
        line=fileptr.readline()
        #print(line)
        line=line.decode("utf-8")
        #print(line)
        infolines.append(line)
       # infolines.append(fileptr.readline())
    infolines[1] = infolines[1].replace('"','')
    infolines[1] = infolines[1].replace('\r\n','')
    varnames = infolines[1].split(',')
    infolines[2]=infolines[2].replace('"','')
    infolines[2]=infolines[2].replace('\r\n','')
    units=infolines[1].split(',')
    infolines[4] = infolines[4].replace('"','') 
    infolines[4] = infolines[4].replace('\r\n','') 
    types=infolines[4].split(',')
# read in the binary data
    data = fileptr.read()
# initialize the location in the string
    i=0
# move through the string reading each data type
    while i<len(data):
       dataline = []
       for dt in types:
           if dt.rfind('FP2')==0:
               dataline.append(parse_csi_value(binascii.hexlify(data[i:i+CSItypelen.get(dt)])))
           else:
               dataline.append(struct.unpack(CSItypes.get(dt),data[i:i+CSItypelen.get(dt)])[0])
           i=i+CSItypelen.get(dt)
# make the time stamp
       stamp = datetime.utcfromtimestamp(dataline[0] + csiepochstart)
       stamp = stamp.replace(microsecond=int(dataline[1]/1e3))
       datadict={}
       for k,v in zip(varnames[2:],dataline[2:]):
           datadict[k]=v
       records.append((stamp,datadict))
    return records

