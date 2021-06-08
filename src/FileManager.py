"""FileManager.py: FileManager class

author: Alexandria Pawlik (apawlik@umich.edu) 
project: github.com/alexandriapawlik/flux-dashboard"""


import os 
import sys
import logging # put error messages in log
import pandas as pd
import numpy as np
from influxdb import DataFrameClient, InfluxDBClient
import DataTable


class FileManager:
    """File manager: owns DataTable object and handles its access to influxDB.

    this is the only class that the driver should use - 
    driver should init then call new_db and/or update_db"""

    def __init__(self, filename):
        """Create FileManager obj: identify file type and create appropriate DataTable-derived class"""
        # check that file exists, log stack trace and exit if it doesn't
        if not os.path.isfile(filename):
            logging.exception("File path {} does not exist.".format(filename))
            sys.exit()

        # determine file type
        filetype = os.path.splitext(filename)

        # init the appropriate version of DataTable object and store it
        if filetype == '.tst':
            self.DT = DataTable.TestFile(filename)
        ### ADD NEW FILE TYPES HERE
        else:  # quit if we don't recognize the file type
            logging.exception("File type {} from file {} not accepted.".format(filetype, filename))
            sys.exit()


    # once driver has obj, two options: create a database or add data to db

    def new_db(self):
        """"Create new database based on file format:

        CAUTION: OVERWRITES EXISTING DB OF THE SAME NAME (only call once)""""
        # create new database that matches datatable format
        # TODO: what info should DataTable store to keep this at 1 param?
        # pick config - store this in DT objects

    def update_db(self):
        # add data from DataTable to appropriate existing database