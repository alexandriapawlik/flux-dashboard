"""FileManager.py: FileManager class

author: Alexandria Pawlik (apawlik@umich.edu) 
project: github.com/alexandriapawlik/flux-dashboard"""


import os 
import sys
import logging # put error messages in log
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient, BucketRetentionRules
from influxdb_client.client.write_api import SYNCHRONOUS
from . import DataTable
from .secret import Secret  # REQUIRED make your own copy of this using secret_copy.py


class FileManager:
    """File manager: wraps DataTable-derived object and handles its access to influxDB"""

    def __init__(self, filename):
        """Create FileManager obj: identify file type and create appropriate DataTable-derived class"""
        # check that file exists, log stack trace and exit if it doesn't
        if not os.path.isfile(filename):
            logging.error("File path {} does not exist.".format(filename))
            sys.exit()

        # determine file type
        filetype = os.path.splitext(filename)
        filetype = filetype[1]

        # init the appropriate version of DataTable object and store it
        if filetype == '.tst':
            self.dt = DataTable.DemoFile(filename)
        ####admin ADD IF CLAUSE FOR EACH NEW FILE TYPE HERE
        else:  # quit if we don't recognize the file type
            logging.error("File type {} from file {} not yet templated.".format(filetype, filename))
            sys.exit()


    def new_db(self):
        """"Create new database matching DataTable (derived class) format

        CAUTION: (probably) will not work if a database with the same name already exists"""

        # chose retention policy by measurement type
        if self.dt.msrmnt == 'Ameriflux_fastdata':
            rp = BucketRetentionRules(type = "expire", every_seconds = 2592000)  # 2.5 mil seconds - about 1 month
        ####admin create and assign new retention policies here if needed
       
        # create connection
        client = InfluxDBClient(url = Secret.url, token = Secret.token, org = Secret.org)
        
        # try to add new bucket/database
        buckets_api = client.buckets_api()
        try:
            org = client.organizations_api().find_organizations(org = Secret.org)[0]  # get Org ID from API (different than org name)
            new_bucket = buckets_api.create_bucket(bucket_name = self.dt.dbname, retention_rules=rp, org_id=org.id)
            logging.info("SUCCESS - created bucket {}".format(new_bucket))
        except:  
            # if new bucket cannot be added for some reason
            logging.error("FAIL - could not create new bucket/database {}".format(self.dt.dbname))
            logging.info("Here are the buckets that currently exist:")
            buckets = buckets_api.find_buckets().buckets
            logging.info("\n".join([f" ---\n ID: {bucket.id}\n Name: {bucket.name}\n Retention: {bucket.retention_rules}"
                for bucket in buckets]))
    
        # close the client connected to the db
        client.close()


    def update_db(self):
        """Update appropriate existing database with data from file"""

        # get clean dataframe
        df = self.dt.create_df()

        # create connection
        client = InfluxDBClient(url = Secret.url, token = Secret.token, org = Secret.org)

        # try to write panda dataframe to the database
        try:
            write_client = client.write_api(write_options = SYNCHRONOUS)
            write_client.write(self.dt.dbname, Secret.org, record = df, data_frame_measurement_name = self.dt.msrmt)
            logging.info("SUCCESS - data from file {} was added to bucket {}".format(self.dt.filename, self.dt.dbname))
        except:
            # if upload fails for some reason
            logging.error("FAIL - data from file {} could not be added to bucket {}".format(self.dt.filename, self.dt.dbname))

        # TODO use tags?

        # close the database
        client.close()


        