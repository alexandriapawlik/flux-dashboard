from src import FileManager
import logging

####admin new file types need to be added to source code before they can be used

# TODO command line option for filename

# set name of log output file (logs will be appended)
logging.basicConfig(filename='demo.log', level=logging.INFO)
logging.info() # TODO log date and passed filename


# instead: add driver scripts (new, update, both) with command line option for filenames
# easy to run from terminal script
# then if one file isn't there, it'll just move on to the next 