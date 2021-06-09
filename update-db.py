"""Update existing database with data from file <filename>, passed as command line arg"""

from src.FileManager import FileManager
from config import Config
import logging
import sys
import datetime


####admin new file types need to be added to source code before they can be used as an argument

if len(sys.argv) != 2:
    print("Requires file name to be passed as command line argument")
    print("Use: python3 update-db.py <filename>")
    sys.exit()

filename = sys.argv[1]

# set name of log output file (logs will be appended)
logging.basicConfig(filename = Config.logfile, level = logging.INFO)
# log info on this instance
logging.info("{}: updating db using file {}".format(datetime.datetime.now(), filename))

mgr = FileManager(filename)
mgr.update_db()

# log completion
logging.info("{}: task completion")