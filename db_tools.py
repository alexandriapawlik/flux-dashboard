# -*- coding: utf-8 -*-

"""Import data from logger files into database

author: Alex Pawlik - apawlik@umich.edu - github.com/alexandriapawlik
purpose: create database from TOA5 file, do some data quality control or add calculated fields to dataframe, 
    and write data to the database
source: code modified from db_tools.py obtained at 
    https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/
"""

import pandas as pd
import numpy as np

from influxdb import DataFrameClient, InfluxDBClient
from campbellread import toa5head
from db_config import pick_config

# select statement for continous query
# write mean of variable into database with long retention policy and new measurment
# will use database with default policy from "measurement" and group the avearge from given duration
# "*" in GROUP BY will include tags from measurement into the new measurement (fastds4w)
# variable names in fastds4w are "mean_<variable_name>"
# cq_sc_tmpl  =  'SELECT mean({variable}) INTO {db}.{policy}.fastds4w FROM {db}.{defPolicy}.{measurement} GROUP BY time({duration}),*'
# cqname_tmpl  =  '{var}_{duration}_cq' 


def makedb_toa5(filepath):
    """Create database and retention policy, import variable names
    
    read toa5 file and use variable names to create database
    CAUTION: OVERWRITES EXISTING DB OF THE SAME NAME (only call once)

    structure:
    - database
    -- measurment (fastdata, slowdata)
       each measurement will have a set of tags associated with it to define its meta properties
       tags are defined in the db_config.py and are listed in the function pick_config 
       Pick_config uses filepath name to pick the correct tags
    --- fields (variables in the database)
    """

    # import variable names and data, parse
    (dbname,measurement,tag_dict) = pick_config(filepath)
    fpt = open(filepath, 'rt')
    line = []
    for i in range(2):
        line.append(fpt.readline())
    variables = line[1]
    variables = variables.replace('\n', '')
    variables = variables.replace('"', '')
    variables = variables.split(',')
    # read in the variables from the TOA5 file, do not include the RECORD number
    variables = variables[2:]

    # create db
    client = InfluxDBClient(host = 'localhost', port = 8086, database = dbname)
    # delete before creation, creates issues if you try to create over exisitng db
    client.drop_database(dbname)
    client.create_database(dbname)

    # add retention policies to db
    # long term retention policy, I think "shard" is the amount that is stored in memory,
    # data beyond a week old is pulled from disk.
    client.create_retention_policy('four_weeks', '4w', replication = 1, database = dbname, shard_duration = '1w')
    # short term retention policy
    # client.create_retention_policy('one_day','24h',replication = 1,database = dbname,default = True,shard_duration = '1h')

    # add continuous queries to db
    # create_continuous_query(name, select, database = None, resample_opts = None)
    # creating continuous queries for all fields ('*') in the measurement.
    # tmpl = cq_sc_tmpl
    # cqselect = tmpl.format(variable = '*',db = dbname,policy = 'four_weeks',measurement = measurement,defPolicy = 'one_day',duration = '1m')
    # print(cqselect)
    # tmpl = cqname_tmpl
    # cqname = tmpl.format(var = 'dsfast',duration = '1m')
    # print(cqname)
    # write the continuous queries to the database
    # client.create_continuous_query(name = cqname,select = cqselect,database = dbname,resample_opts = 'every 30m for 3h')

    # close the client connected to the database
    client.close()


def dataQC(data,tag_dict):
    """Quality check data

    format data into the proper format, remove any data points that exceed sensor limits
    can also be used to calculate wind speed/direction form u/v wind speeds, etc
    can store offsets in the tag_dict for the sensor
    """

    if tag_dict.get('site') == '1' and tag_dict.get('datatype') == 'met':
        # TODO
        # data.u = data.u/100.
        # data.v = data.v/100.
        # data.w = data.w/100.
        # data.t = data.t/100.
        # data.u[data.u<-30] = np.nan
        # data.u[data.u>30] = np.nan
        # data.v[data.v<-30] = np.nan
        # data.v[data.v>30] = np.nan
        # data.w[data.w<-30] = np.nan
        # data.w[data.w>30] = np.nan
        # data.t[data.t<-30] = np.nan
        # data.t[data.t>60] = np.nan
    return data


def writedata_toa5(filepath):
    """Write data to db"""

    (dbname, measurement, tag_dict) = pick_config(filepath)

    # fastdata goes into four_weeks
    if measurement == 'fastdata':
        rp = 'four_weeks'
    print(rp, measurement, dbname)
    protocol = 'line'

    # read data into Pandas dataframe
    data = toa5head(filepath)
    print(data)

    # if data is time series data from WLEF change the wind speed values to m/s
    # can add other checks on data for different sites as well
    # data = dataQC(data,tag_dict) 
    # TODO

    # create link to database
    client = DataFrameClient(host = 'localhost', port = 8086, database = dbname)

    # write panda dataframe to the database
    rtn_write = client.write_points(data, measurement = measurement, tags = tag_dict,
        database = dbname, retention_policy = rp, protocol = protocol)

    # close the database
    client.close()
