
Code modified from files obtained at https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/

- campbellread.py: function to read TOA5 files and put data into a Pandas dataframe.
- db_tools.py: functions to create database from TOA5 file, do some data quality control or add calculated fields to dataframe, and write data to the database.
- db_config.py: create tag definitions for database
- diagdecode.py: decodes Campbell and Licor diagnostic codes.
- insertWLEF.py and insertKernza.py: two functions that are run by cron to insert data into the database.

