"""Update existing database with data from file <filename>, passed as command line arg"""

from src.FileManager import FileManager
from config import Config
import logging
import sys
import datetime


#### new file/table types need to be added to source code before they can be used as an argument
#### new databases need to be created with new-db.py before they can be updated

if len(sys.argv) != 2:
    print("Requires file name to be passed as command line argument")
    print("Use: python3 update-db.py <filename>")
    sys.exit(2)

filename = sys.argv[1]

# set name of log output file (logs will be appended)
logging.basicConfig(filename = Config.logfile, level = logging.INFO)
# log info on this instance
logging.info("START {}: updating db using file {}".format(datetime.datetime.now(), filename))

mgr = FileManager(filename)
mgr.update_db()

# log completion
logging.info("END {}: update complete".format(datetime.datetime.now()))