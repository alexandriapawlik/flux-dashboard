"""File manager: owns DataTable object and handles its access to influxDB.

this is the only class that the driver should use - 
driver should init then call new_db and/or update_db"""

import os # for path.splitext
import pandas as pd
# import numpy as np
from influxdb import DataFrameClient, InfluxDBClient
import DataTable

class FileManager:
    # DataTable member object

    def __init__(self, filename):
        # determine file type
        filetype = os.path.splitext(filename)
        # init the appropriate version of DataTable object and store it

    # once driver has obj, two options: create a database or add data to db

    def new_db(self):
        """"Create new database based on file format:

        CAUTION: OVERWRITES EXISTING DB OF THE SAME NAME (only call once)""""
        # create new database that matches datatable format
        # TODO: what info should DataTable store to keep this at 1 param?
        # pick config

    def update_db(self):
        # add data from DataTable to appropriate existing database