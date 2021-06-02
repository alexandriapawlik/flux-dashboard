from datetime import datetime, timedelta
from glob import glob 
import sys
sys.path.insert(2,'/home/jthom/influxDB_v2_0')
import os
from db_tools import *
from db_config import *
from campbellread_v2_0 import toa5head

# start time for operation
date = datetime.utcnow()
print('start time:',date)

# get some times to determine files to select
date00 = datetime.now()
date30 = datetime.now() - timedelta(minutes=30)

# select files
files=glob('/air/incoming/Kernza/current/Kernza_Time_Series*.dat')
# sort the list to a time order
files.sort()
fileTS=[]
# I think I'm grabbing the time stamp on the file metadata
for fn in files:
    fileTS.append(datetime.fromtimestamp(os.stat(fn).st_mtime))
fileIndx=[]
for i,ts in enumerate(fileTS):
    if ts<date00 and ts>date30:
        fileIndx.append(i)

for i in fileIndx:
    filepath=files[i]
    print(filepath)
    if os.path.exists(filepath):
        writedata_toa5(filepath) 
    else:
        print(filepath,' does not exist')

files=glob('/air/incoming/Kernza/current/Kernza_surfaceobs_*.dat')
files.sort()
fileTS=[]
for fn in files:
    fileTS.append(datetime.fromtimestamp(os.stat(fn).st_mtime))
fileIndx=[]
for i,ts in enumerate(fileTS):
    if ts<date00 and ts>date30:
        fileIndx.append(i)

for i in fileIndx:
    filepath=files[i]
    print(filepath)
    if os.path.exists(filepath):
        writedata_toa5(filepath) 
    else:
        print(filepath,' does not exist')

# give end time for operation
date = datetime.utcnow()
print('end time:',date)
