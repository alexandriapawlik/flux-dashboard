"""File manager: owns DataTable object and handles access to influxDB

this is the only class that the driver should use
driver should init, then call new_db and/or update_db"""

import pandas as pd
# import numpy as np
from influxdb import DataFrameClient, InfluxDBClient
import DataTable

class FileManager:
    # DataTable member object

    def __init__(self, filename):
        # determine file type
        # init the appropriate version of DataTable object and store it

    # once driver has obj, two options: create a database or add data to db

    def new_db(self):
        # create new database that matches datatable format
        # TODO: what info should DataTable store to keep this at 1 param?

    def update_db(self):
        # add data from DataTable to appropriate existing database