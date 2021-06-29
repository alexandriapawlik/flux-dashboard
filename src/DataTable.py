"""DataTable.py: DataTable base class and all DataTable derived classes

author: Alexandria Pawlik (apawlik@umich.edu) 
project: github.com/alexandriapawlik/flux-dashboard"""


from datetime import datetime
import pytz
import pandas as pd

############ base class

class DataTable:
    """DataTable: common base class for all data table file types.

    (only its derived classes are meant to be used by FileManager)
    owns file info and access to data file,
    will not access influxDB at all,
    shouldn't be accessed by driver directly"""

    def __init__(self, Filename):
        """Create a DataTable object, store filename"""

        # set instance var
        self.filename = Filename    
        
    def build_df(self, headerlines, timeformat):
        """Parse file and return as pandas df

        ASSUME timestamp is first column
        headlerlines - int, number of lines to ignore at beginning of file (including line with column names)
        timeformat - string, date format that looks like '%Y-%m-%d %H:%M:%S'
        note: make sure that input nan values are in one of these formats: 
            "NaN, "Nan", "nan" (or else they'll be left as strings)"""

        all_lines = []
        all_times = []
        # doc reader - automatically closes file when done
        with open(self.filename) as reader:

            # skip header lines
            for i in range(headerlines):
                next(reader)

            # read file line by line
            for line in reader:
                # clean line and convert to str array
                line = line.replace('\n','')
                line = line.replace('\r','')
                line = line.replace('"','')
                line = line.split(',')

                # parse timestamp
                ts = datetime.strptime(line[0], timeformat)

                # extract timestamp
                all_times.append(ts)
                untyped_line = line[1:]

                # parse observation value by value: convert values to float/nan or leave as string
                temp_line = []
                for i,v in enumerate(untyped_line):
                    try:
                        dataval = float(v) 
                    except ValueError:
                        dataval = v
                    temp_line.append(dataval)
                # add line to list of lines
                all_lines.append(temp_line)

        # create df and return it
        self.line_array = all_lines
        self.time_array = pd.DatetimeIndex(all_times)  
        return pd.DataFrame(self.line_array, index = self.time_array)


############# define derived classes, one per differing file type/format/variables


class DemoFile(DataTable):
    """derived class for demo filetype (.tst)
    
    no header in file,
    input columns: (Timestamp, Status, Plot, Flux Value)
    output columns: (Plot, Flux_Value)"""


    ####### CONSTANT class vars, specific to this file type

    # number of lines to ignore at the beginning of file
    headerlines = 0
    # indices of cols we won't need, skipping indices of timestamp cols
    delete_cols = [0,1] 
    # names of cols we will to keep, without timestamp column
    col_names = ['Plot', 'Temp', 'Flux_Value', 'Code']   
    # names of fields/cols to use as tags - data fields that have string values that you want to group by (wont be stored in _field anymore)
    tag_cols = ['Plot', 'Code']  
    # format of timestamps in input file
    timeformat = '%Y-%m-%d %H:%M:%S'
    # influxdb config options 
    dbname = 'demo3'  # name of bucket/database this table belongs in
    msrmnt = 'Ameriflux_fastdata'  # type of measurement
    time_precision = 's'  # see docs for other options
    timezone = 'US/Eastern'  # see docs for other options


    def __init__(self, Filename):
        """Create a DemoFile object, store filename"""

        super().__init__(Filename)
        
    def build_df(self):
        """Parse file into clean Pandas dataframe"""

        # use base class to parse data in df, set timezone
        df = super().build_df(headerlines = self.headerlines, timeformat = self.timeformat).tz_localize(self.timezone)
        
        ### derived class stuff (specific to file type)

        # remove extra cols
        df.drop(df.columns[self.delete_cols], axis = 1, inplace = True)
        # add column names
        df.columns = self.col_names
        # mutate to create any new columns
        df['Sum'] = df['Temp'] + df['Flux_Value']

        return df



class Test46m(DataTable):
    """Test loggernet output"""

    ####### CONSTANT class vars, specific to this file type

    # number of lines to ignore at the beginning of file
    headerlines = 4
    # indices of cols we won't need, skipping indices of timestamp cols
    delete_cols = [0]
    # names of cols we will to keep, without timestamp column
    col_names =  ["PPFD", "Total_PPFD", "Diffuse_PPFD", "Calibration_PPFD", "Solar_Incidence"]
    # names of fields/cols to use as tags - data fields that have string values that you want to group by (wont be stored in _field anymore)
    tag_cols = ["Calibration_PPFD"] 
    # format of timestamps in input file
    timeformat = '%Y-%m-%d %H:%M:%S'
    # influxdb config options 
    dbname = 'testoutput'  # name of bucket/database this table belongs in
    msrmnt = 'Ameriflux_fastdata'  # type of measurement
    time_precision = 's'  # see docs for other options
    timezone = 'US/Eastern'  # see docs for other options


    def __init__(self, Filename):
        """Create object, store filename"""

        super().__init__(Filename)
        
    def build_df(self):
        """Parse file into clean Pandas dataframe"""

        # use base class to parse data in df, set timezone
        df = super().build_df(headerlines = self.headerlines, timeformat = self.timeformat).tz_localize(self.timezone)
        
        # remove extra cols
        df.drop(df.columns[self.delete_cols], axis = 1, inplace = True)

        # add column names
        df.columns = self.col_names

        # fix column types
        df["Calibration_PPFD"] = df["Calibration_PPFD"].astype(str)

        # qa/qc that needs to be done for this file type
        # 

        return df


####admin1 ADD NEW DERIVED CLASS HERE FOR EACH NEW FILE TYPE
# if base class doesn't match your file format for some reason, just override fns in derived class
###################################### template for new derived classes

# class NewClass(DataTable):
#     """describe file type"""

#     ####### CONSTANT class vars, specific to this file type

#     # number of lines to ignore at the beginning of file
#     headerlines = 0
#     # indices of cols we won't need, first non-timestamp column should be index 0
#     delete_cols = []
#     # names of cols we will to keep, without timestamp column
#     col_names =  []
#     # names of fields/cols to use as tags - data fields that have string values that you want to group by (wont be stored in _field anymore)
#     tag_cols = [] 
#     # format of timestamps in input file https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
#     timeformat = '%Y-%m-%d %H:%M:%S'
#     # influxdb config options 
#     dbname = ''  # name of bucket/database this table belongs in
#     msrmnt = 'Ameriflux_fastdata'  # type of measurement
#     time_precision = 's'  # see docs for other options
#     timezone = 'US/Eastern'  # see docs for other options


#     def __init__(self, Filename):
#         """Create object, store filename"""

#         super().__init__(Filename)
        
#     def build_df(self):
#         """Parse file into clean Pandas dataframe"""

#         # use base class to parse data in df, set timezone
#         df = super().build_df(headerlines = self.headerlines, timeformat = self.timeformat).tz_localize(self.timezone)
        
#         # remove extra cols
#         df.drop(df.columns[self.delete_cols], axis = 1, inplace = True)

#         # add column names
#         df.columns = self.col_names

#         # fix column types (ie. int that should be tag/string will be parsed as a number)
#         # 

#         # mutate to create any new columns
#         example: df['Sum'] = df['Temp'] + df['Flux_Value']

#         # qa/qc that needs to be done for this file type
#         # 

#         return df
