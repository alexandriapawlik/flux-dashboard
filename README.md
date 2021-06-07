# flux-dashboard

Example: https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/
*eventually paste outline from GDrive here*

Code structure:
- DataTable - super class with one derived class per file type, don't access from driver
- FileManager - wraps a (derived) DataTable object to interact with influxDB, acts as the only class the driver needs
- driver - creates a FileManager for each file to be used, for each file chooses to create a new db and/or update an existing db
