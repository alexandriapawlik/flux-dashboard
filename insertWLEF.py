"""Insert data into db

author: Alex Pawlik - apawlik@umich.edu - github.com/alexandriapawlik
purpose: run by cron to insert data into the database
source: code modified from insertWLEF.py obtained at 
    https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/
"""

from datetime import datetime, timedelta
from glob import glob 
import sys
sys.path.insert(2,'/home/jthom/influxDB_v2_0')
from db_tools import *
from db_config import *
from campbellread import toa5head

date = datetime.utcnow()
print('start time:',date)
date = datetime.utcnow()-timedelta(hours=1)
filepath=date.strftime('/air/incoming/WLEFFlux/Data/%Y_%m/%d/%H*')

files=glob(filepath + '/WLEF_*.dat')

for fn in files:
    if fn.find('ati')<0:
        print(fn)
        writedata_toa5(fn)

files=glob(filepath + '/newtrailer_[d,m]*.dat')
for fn in files:
    print(fn)
    writedata_toa5(fn)


date = datetime.utcnow()
print('end time:',date)
