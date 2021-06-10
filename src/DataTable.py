"""DataTable.py: DataTable base class and all DataTable derived classes

author: Alexandria Pawlik (apawlik@umich.edu) 
project: github.com/alexandriapawlik/flux-dashboard"""


from datetime import datetime
import pytz
import pandas as pd
import ciso8601  # TODO use for parsing dates

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
        
    def create_df(self):
        """Parse file and return as pandas df (no column names)
        
        make sure that input nan values are in one of these formats: "NaN, "Nan", "nan" (or else they'll be left as strings)"""

        all_lines = []
        all_times = []
        # doc reader - automatically closes file when done
        with open(self.filename) as reader:
            # iterate through each line of file
            for line in reader:
                # clean line and convert to str array
                line = line.replace('\n','')
                line = line.replace('\r','')
                line = line.replace('"','')
                line = line.split(',')

                # parse timestamp
                # TODO can we just set it differently from logger?
                ts = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')

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
        self.time_array = pd.DatetimeIndex(all_times, tz = pytz.timezone('US/Eastern'))  # set timezone
        return pd.DataFrame(self.line_array, index = self.time_array)


############# define derived classes, one per differing file type/format/variables

class DemoFile(DataTable):
    """derived class for demo filetype (.tst)
    
    no header in file,
    input columns: (Timestamp, Status, Plot, Flux Value)
    output columns: (Plot, Flux_Value)"""


    # CONSTANT class vars, specific to this file type
    col_names = ["Plot", "Flux_Value"]   # names of cols we want to keep, without timestamp column
    tag_cols = ["Plot"]  # names of columns to use as tag columns - data fields that stay wide and not long format, must be string values
    delete_cols = [0]  # indices of cols we won't need, skipping indices of timestamp cols
    # db config options
    dbname = 'demo'  # represents a bucket
    msrmnt = 'Ameriflux_fastdata'  # tag for type of measurement


    def __init__(self, Filename):
        """Create a DemoFile object, store filename"""

        super().__init__(Filename)
        
    def create_df(self):
        """Parse file into clean Pandas dataframe"""

        # use base class to parse data in df
        df = super().create_df() 
        
        ### derived class stuff (specific to file type)

        # remove extra cols
        df.drop(df.columns[self.delete_cols], axis = 1, inplace = True)
        # add column names
        df.columns = self.col_names
        # mutate to create any new columns
        df['Sum'] = df['Plot'] + df['Flux_Value']
        # qa/qc that needs to be done for this file type
        # 
        return df


####admin ADD NEW DERIVED CLASS HERE FOR EACH NEW FILE TYPE
# if base class doesn't match your file format, just override fns in derived class

# TODO leave template for new derived classes