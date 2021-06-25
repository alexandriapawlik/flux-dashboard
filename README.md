# UMBS AmeriFlux Core Site Data Dashboard

[Inspiration](https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/)   
[Dashboard access](https://umbsflux.grafana.net/d/VyqSwgR7k/umbs-ameriflux-core-site?from=1623161110000&to=1623161190000&orgId=1) (only works for existing Grafana org members)


## Outline:  
- src
    - [DataTable.py](src/DataTable.py) - contains DataTable superclass and one derived class per file type (data table format)
    - [FileManager.py](src/DataTable.py) - contains FileManager class which wraps a (derived) DataTable object to interact with influxDB
    - secret.py - stores Secret class containing confidential authentication data  
        &#8594; not uploaded to GitHub, recreate your own copy using [secret_copy.py](src/secret_copy.py)
- [new-db.py](new-db.py): driver script for creating a new database using the specificed file's template (hard-coded)  
    ```sh python3 new-db.py <filename> ```  
    &#8594; only run this once
- [update-db.py](update-db.py): driver for updating an existing database using the specificed file's template (hard-coded)  
    ```sh python3 update-db.py <filename> ```
- [config.py](config.py): contains a Config class with values that can be changed as often as needed (i.e. name of log file, etc.)


## Use Guide:
- Lines where changes need to occur for a new file type, etc. are led by the string ####admin
- Write a bash script to upload a series of files to influxDB (after creating each new database, then continually upload the new files to it)
- Database is used here as synonymous to influxDB's "bucket"
- What changes need to be made for a new table  
    - (admin1) DataTable.py - new derived class for table type, use commented template
    - (admin2) FileManager.py - set rules of identifying this table type from a file name
    - (admin3) define new retention policy if needed
    - (admin4) config.py - define new configuration values if needed


## Data Flow:
- Data goes from Campbell data loggers to tower PC
- Run upload scripts from the tower PC
    - Convert date in format (DOY, hour, minute) to a single field
    - Filter and/or clean data (basic stuff)
    - Convert to Pandas dataframe
- If this is the first time using a specific database, it needs to be configured and created
- Insert dataframe into database
- Grafana reads data from influxDB via http
    - Display things that help with QA/QC
- Users access dashboard with permissioned Grafana endpoint


