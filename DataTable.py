"""DataTable base class and all DataTable derived classes"""

import os
import sys
import logging # put error messages in log
import datetime
import pandas as pd
import numpy as np


class DataTable:
    """DataTable: common base class for all data table file types.

    owns file info and access to data file,
    will not access influxDB at all,
    shouldn't be accessed by driver directly"""

    def __init__(self, Filename):
        """Create a DataTable object, store filename"""
        
        # check that file exists, log stack trace and exit if it doesn't
        if not os.path.isfile(Filename):
            logging.exception("File path {} does not exist.".format(Filename))
            sys.exit()

        # set instance var
        self.filename = Filename    
        
    def create_df(self):
        """Parse file into Pandas dataframe and return it"""

        all_lines = []
        all_times = []
        # doc reader - automatically closes file when done
        with open(self.filename) as reader:
            # iterate through each line of file
            for line in reader:
                line = line.split(',')
                temp = []

                # TODO fix timestamp format - can we just set it differently from logger?
                # extract timestamp
                all_times.append(line[0])
                line = line[1:]

                # parse observation value by value: convert values to float or NaN
                for i,v in enumerate(line):
                    try:
                        dataval = float(v)
                    except ValueError:
                        dataval = float('nan')
                    temp.append(dataval)
                # add line to list of lines
                all_lines.append(line)

        # convert list of lines to np array
        self.line_array = np.array(all_lines)
        self.time_array = pd.DatetimeIndex(all_times)
        return pd.DataFrame(self.line_array, index = self.time_array)


## define derived classes, one per differing file type/format/variables


class TestFile(DataTable):
    """derived class for test run filetype (.tst)
    
    no header in file,
    column order: (Timestamp, Status, Plot, Flux Value)"""

    # CONSTANT class vars, specific to this file type
    _col_names = ["Plot", "Flux_Value"]   # names of cols we want to keep, without timestamp column
    _delete_cols = [1]  # indices of cols we won't need
    # TODO: store db options based on file type, for public use

    def __init__(self, Filename):
        """Create a TestFile object, store filename"""

        super().__init__(Filename)
        
    def create_df(self):
        """Parse file into clean Pandas dataframe"""

        # use base class to parse data, but create different Pandas df than the one it returns
        super().create_df() 
        
        ### derived class stuff (specific to file type)

        # remove extra cols
        self.line_array = np.delete(self.line_array, self._delete_cols)
        # fix any data types here if necessary
        # TODO
        # create Pandas df
        df = pd.DataFrame(self.line_array, index = self.time_array, columns = self._col_names)
        # mutate to create any new columns
        df['Sum'] = df.Plot + df.Flux_Value
        # qa/qc that needs to be done for this file type
        # TODO
