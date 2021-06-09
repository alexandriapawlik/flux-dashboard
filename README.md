# flux-dashboard

Example: https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/
*eventually paste outline from GDrive here*

- Lines where changes need to occur for a new file type, etc. are led by the string ####admin
- /src/secret.py is not uploaded, recreate your own copy using [/src/secret_copy.py](src/secret_copy.py)

Code structure: *fix up this tree*
- src
    - DataTable - super class with one derived class per file type, don't access from driver
    - FileManager - wraps a (derived) DataTable object to interact with influxDB, acts as the only class the driver needs
- new-db.py: driver for creating a new database using the specificed file's template (hard-coded)  
    ```sh python3 new-db.py <filename> ```
- update-db.py: driver for updating an existing database with a new file  
    ```sh python3 update-db.py <filename> ```
- config.py: contains a Config class with values that can be changed as often as needed (ie. not things like url and db/bucket names)



