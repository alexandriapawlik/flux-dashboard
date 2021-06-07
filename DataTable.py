"""DataTable superclass 

owns file info and access to data file
will not access influxDB at all
shouldn't be accessed by driver directly"""

import pandas as pd
import numpy as np


# superclass
class DataTable:
    # member vars
    filename = ""
    # header list
    # Pandas dataframe
    # doc reader - pick up where we left off when parsing entire table

    # constant
    # column #s we don't need - specific to file type

    # public fns
    def __init__(self, Filename):
        """Create a DataTable object

        Fix timestamp format, remove columns we don't want, and parse header
        """

        filename = Filename
        # fix timestamp format
        # remove columns that we don't want (use constant)
        # parse header

    # in derived classes: call super for parse data, then do personal qaqc
    def create_df(self):
        """Returns a Pandas dataframe with qc done"""

        l = []
        # parse data (put data from file into pandas df)
        # in derived classes: any qa/qc that needs to be done for this file type
    


## define derived classes, one per differing file type/format/variables