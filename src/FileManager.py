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
from .secret import Secret  


class FileManager:
    """File manager: wraps DataTable-derived object and handles its access to influxDB
    
    handles all errors and logging for DataTable-derived classes"""

    def __init__(self, filename):
        """Create FileManager obj: identify file type and create appropriate DataTable-derived class"""
        # check that file exists, log stack trace and exit if it doesn't
        if not os.path.isfile(filename):
            logging.error("File path {} does not exist.".format(filename))
            sys.exit(1)

        # split file name into file type and other bits separated by _
        filestr = os.path.splitext(filename)
        filetype = filestr[1]
        filepieces = filestr[0].split("_")  # array of pieces of file name

        # init the appropriate version of DataTable object and store it
        if filetype == '.tst':
            self.dt = DataTable.DemoFile(filename)
        elif filepieces[0] == '46m':
            self.dt = DataTable.Test46m(filename)
        ####admin2 ADD IF CLAUSE FOR EACH NEW FILE TYPE HERE
        else:  # quit if we don't recognize the file type
            logging.error("File type {} from file {} not yet templated.".format(filetype, filename))
            sys.exit(1)


    # fn not needed
    # def get_bucketname(self):
    #     """Return the name of the bucket/db that this file type has been matched to"""
    #     return self.dt.dbname


    def _connect(self):
        """Attempt to establish connection with influxdb cloud, return InfluxDBClient object
        
        private function only to be utilized within this class"""
        i = 0
        tries = 3
        while i < tries:
            try:
                client = InfluxDBClient(url = Secret.url, token = Secret.token, org = Secret.org, gzip=True)
                return client
            except:
                (err_type, err_value, err_traceback) = sys.exc_info()
                logging.info("Could not connect to influxDB client, retrying... ")
                i += 1
                if i == tries:
                    logging.error("Could not connect to influxDB client \n{}\n{}".format(err_type, err_value))

        # if it deosn't return in 3 tries, quit this runtime
        
        sys.exit(1)
        

    def new_db(self):
        """"Create new database matching DataTable (derived class) format

        CAUTION: (probably) will not work if a database with the same name already exists"""

        # chose retention policy by measurement type
        if self.dt.msrmnt == 'Ameriflux_fastdata':
            rp = BucketRetentionRules(type = "expire", every_seconds = 2592000)  # 2.5 mil seconds - about 1 month
        ####admin3 create and assign new retention policies here if needed
       
        # create connection
        client = self._connect()
        
        # try to add new bucket/database
        buckets_api = client.buckets_api()
        try:
            org = client.organizations_api().find_organizations(org = Secret.org)[0]  # get Org ID from API (different than org name)
            new_bucket = buckets_api.create_bucket(bucket_name = self.dt.dbname, retention_rules=rp, org_id=org.id)
            logging.info("SUCCESS created bucket {}\n{}".format(self.dt.dbname, new_bucket))
        except:  
            # if new bucket cannot be added for some reason
            (err_type, err_value, err_traceback) = sys.exc_info()
            logging.error("Could not create new bucket {}\n{}\n{}".format(self.dt.dbname, err_type, err_value))
            
            # extra logging info for buckets
            # logging.info("Free version allows 2 new buckets. Buckets that currently exist:")
            # buckets = buckets_api.find_buckets().buckets
            # logging.info("\n".join([f" ---\n ID: {bucket.id}\n Name: {bucket.name}\n Retention: {bucket.retention_rules}"
            #     for bucket in buckets]))
            sys.exit(1)
    
        # close the client connected to the db
        client.close()


    def update_db(self):
        """Update appropriate existing database with data from file"""

        # get clean dataframe
        df = self.dt.build_df()
        print(df)

        # create connection
        client = self._connect()

        # try to write panda dataframe to the database
        try:
            write_client = client.write_api(write_options = SYNCHRONOUS)
            write_client.write(self.dt.dbname, Secret.org, record = df, time_precision = self.dt.time_precision, 
                data_frame_measurement_name = self.dt.msrmnt, data_frame_tag_columns = self.dt.tag_cols)
            logging.info("SUCCESS data was added to bucket {}".format(self.dt.dbname))
            write_client.close()
        except:
            # if upload fails for some reason
            (err_type, err_value, err_traceback) = sys.exc_info()
            logging.error("Could not add data to bucket {}\n{}\n{}".format(self.dt.dbname, err_type, err_value))
            sys.exit(1)

        # close the database
        client.close()


        