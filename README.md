# a real-time dashboard for UMBS AmeriFlux Core Site data
Python scripts to connect Campbell LoggerNet data to influxDB and Grafana 
([inspiration](https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/))    
[Final product](https://umbsflux.grafana.net/d/VyqSwgR7k/umbs-ameriflux-stats?orgId=1&theme=dark)


## Outline:  
- src
    - [DataTable.py](src/DataTable.py) - contains DataTable superclass and one derived class per file type (data table format)
    - [FileManager.py](src/FileManager.py) - contains FileManager class which wraps a (derived) DataTable object to interact with influxDB
    - secret.py - stores Secret class containing confidential authentication data  
        &#8594; not uploaded to GitHub, recreate your own copy using [secret_copy.py](src/secret_copy.py)
- [new-db.py](new-db.py): driver script for creating a new database using the specificed file's template (hard-coded)  
    ```sh python3 new-db.py <filename> ```  
    &#8594; only run this once
- [update-db.py](update-db.py): driver for updating an existing database using the specificed file's template (hard-coded)  
    ```sh python3 update-db.py <filename> ```
- [config.py](config.py): contains a Config class with values that can be changed as often as needed (i.e. name of log file, etc.)


## Use Guide:
- *Database is used here as synonymous to influxDB's "bucket"*
- Use DataTable class to create derived classes for each file format to be uploaded. Lines where changes need to occur for a new file type are led by the string ####admin  
    - (####admin1) DataTable.py - new derived class for table type, use commented template (set class constants and QA/QC)
    - (####admin2) FileManager.py - set rules of identifying this table type from a file name
    - (####admin3) define new retention policy if needed (not used by production code)
    - (####admin4) config.py - define new configuration values if needed
- If a new database/bucket is needed, use python3 new-db.py <filename> in the home directory of the repository (one time per database name).
    - Production code doesn’t have this script. Future users should just create a bucket on the influx web interface.
- For daily service: (once) edit driver.py to include all files. LoggerNet is set to overwrite output files every time data is collected (5 minutes), so Task Scheduler needs to run this often to avoid losing data. This is the easiest way to ensure we don’t overload the tower PC. 
    - As long as the existing driver.py is edited, the Task Scheduler never needs to be changed. This also depends on the source code and Python packages staying in the same locations.
    - All log info will go to the file set in config.py, so there won’t be any output to the terminal. The log is also set to overwrite.
- If update frequency of Grafana isn’t sufficient, this can be affected by a number of settings:
    - LoggerNet data collection frequency
    - influxDB timestamp precision
    - Grafana update frequency


## Data Flow:
- Instantaneous data downloaded from Campbell data loggers to computer every 5 minutes
    - LoggerNet (on PC) sets this collection frequency, which must be the same for all output tables
    - LoggerNet sets output filename and method of writing (currently overwrites so filename won’t change)
    - Output file is .DAT with CRLF sequence, comma delimited
    - Timestamp is format yyyy-mm-dd HH:MM:ss
- Windows Task Scheduler calls Python code to upload new data to influxDB Cloud 2.0 (with AWS endpoint)
    - Filter and/or clean data to improve QA/QC
    - Convert to Pandas dataframe
    - Also if we need a new database/bucket because the existing ones don’t match, it needs to be configured and created (with python or web interface)
    - Insert dataframe into database/bucket (driver.py)
- influxDB cloud deletes old data after a fixed amount of time (retention policy tbd)
    - influxDB also has dashboard capabilities so we could potentially use this and skip Grafana?
- Grafana reads data from influxDB via http
    - Display things that help with QA/QC: comparison over heights, comparison between different sensors
- Users access dashboard through Grafana (Grafana sharing) 
    - We are currently using the free version, which allows 3 users. 




