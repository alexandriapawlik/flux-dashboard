# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from influxdb import DataFrameClient, InfluxDBClient
from campbellread_v2_0 import toa5head
from db_config import pick_config
# select statement for continous query
# write mean of variable into database with long retention policy and new measurment
# will use database with default policy from "measurement" and group the avearge from given duration
# "*" in GROUP BY will include tags from measurement into the new measurement (fastds4w)
# variable names in fastds4w are "mean_<variable_name>"
cq_sc_tmpl = 'SELECT mean({variable}) INTO {db}.{policy}.fastds4w FROM {db}.{defPolicy}.{measurement} GROUP BY time({duration}),*'
cqname_tmpl = '{var}_{duration}_cq' 

# read toa5 file and use variable names to create database
# data base structure:
# -database
# --measurment (fastdata, slowdata)
# each measurement will have a set of tags associated with it to define its meta properties
#    tags are defined in the db_config.py and are listed in the function pick_config. 
#    Pick_config uses filepath name to pick the correct tags
# --- fields (variables in the database)
#
def makedb_toa5(filepath):
# create db with continuous queries. Use variable names to create continuous queries. Write data to 
# short term retention policy and store mean values in long term retention policy
    (dbname,measurement,tag_dict)=pick_config(filepath)
    fpt=open(filepath,'rt')
    line=[]
    for i in range(4):
        line.append(fpt.readline())
    variables=line[1]
    variables=variables.replace('\n','')
    variables=variables.replace('"','')
    variables=variables.split(',')
# read in the variables from the TOA5 file, do not include the RECORD number
    variables=variables[2:]

# create db
    client=InfluxDBClient(host='localhost',port=8086,database=dbname)
# delete the dbname before creation, have issues if you try and create over an exisitng database
    client.drop_database(dbname)
    client.create_database(dbname)

# add retention policies to db
  # long term retention policy, I think "shard" is the amount that is stored in memory,
  # data beyond a week old is pulled from disk.
    client.create_retention_policy('four_weeks','4w',replication=1,database=dbname,shard_duration='1w')
  # short term retention policy
    client.create_retention_policy('one_day','24h',replication=1,database=dbname,default=True,shard_duration='1h')

# add continuous queries to db
#            create_continuous_query(name, select, database=None, resample_opts=None)
#  creating continuous queries for all fields ('*') in the measurement.
    tmpl=cq_sc_tmpl
    cqselect=tmpl.format(variable='*',db=dbname,policy='four_weeks',measurement=measurement,defPolicy='one_day',duration='1m')
    print(cqselect)
    tmpl=cqname_tmpl
    cqname=tmpl.format(var='dsfast',duration='1m')
    print(cqname)
         
# write the continuous queries to the database
    client.create_continuous_query(name=cqname,select=cqselect,database=dbname,resample_opts='every 30m for 3h')

# close the client connected to the database
    client.close()

# dataQC will format data into the proper format and remove any data points that exceed sensor limits
# can also be used to calculate wind speed/direction form u/v wind speeds, etc
# can store offsets in the tag_dict for the sensor.
def dataQC(data,tag_dict):
    if tag_dict.get('site')=='WLEF' and tag_dict.get('datatype')=='ts':
        data.u=data.u/100.
        data.v=data.v/100.
        data.w=data.w/100.
        data.t=data.t/100.
        data.u[data.u<-30]=np.nan
        data.u[data.u>30]=np.nan
        data.v[data.v<-30]=np.nan
        data.v[data.v>30]=np.nan
        data.w[data.w<-30]=np.nan
        data.w[data.w>30]=np.nan
        data.t[data.t<-30]=np.nan
        data.t[data.t>60]=np.nan
    return data


def writedata_toa5(filepath):
    (dbname,measurement, tag_dict)=pick_config(filepath)
# define retention policy where you need to write data
# slowdata goes into four_weeks, fastdata goes into default 1 day policy
    if measurement=='slowdata':
        rp='four_weeks'
    else:
        rp=''
    print(rp,measurement,dbname)
    protocol='line'
# read data into Pandas dataframe
    data=toa5head(filepath)
    #print(data)
    # if data is time series data from WLEF change the wind speed values to m/s
    # can add other checks on data for different sites as well
    data=dataQC(data,tag_dict) 
# create link to database
    client=DataFrameClient(host='localhost',port=8086,database=dbname)

# write panda dataframe to the database
    rtn_write=client.write_points(data,measurement=measurement,tags=tag_dict,database=dbname,retention_policy=rp,protocol=protocol)

# close the database
    client.close()
