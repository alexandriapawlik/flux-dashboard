"""Create tag definitions for database

author: Alex Pawlik - apawlik@umich.edu - github.com/alexandriapawlik
purpose: define tags and other metadata based on file name
source: code modified from db_config.py obtained at 
    https://ameriflux.lbl.gov/real-time-data-view-using-influxdb-and-grafana/
"""

def pick_config(fname):
    """Define tags and other metadata based on file name"""

    dbname = []
    measString = []
    tag_dict = []

    if fname.find('test_file') >= 0:
        dbname = 'testdb'
        measString = 'fastdata'
        tag_dict = {'site':'Ameriflux', 'level':'46m', 'datatype':'met'}

    # for each file type need to include a database name, measstring and tag_dict

    #     elif fname.find('WLEF_bot_ts')> = 0:
    #         dbname = 'wlefBotHF'
    #         measString = 'fastdata'
    #         tag_dict = {'project':'Ameriflux','site':'WLEF', 'level':'bottom', 'datatype':'ts'}

    #print(dbname,measString, tag_dict)
    return (dbname, measString, tag_dict)
