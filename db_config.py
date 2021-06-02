# for each file type need to include a database name, measstring and tag_dict

#WLEF Bot

def pick_config(fname):
    dbname=[]
    measString=[]
    tag_dict=[]

    if fname.find('WLEF_bot_slow')>=0:
        dbname='wlefBotLF'
        measString='slowdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'bottom', 'datatype':'met'}

    elif fname.find('WLEF_bot_ts')>=0:
        dbname='wlefBotHF'
        measString='fastdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'bottom', 'datatype':'ts'}

#WLEF Mid

    elif fname.find('WLEF_mid_slow')>=0:
        dbname='wlefMidLF'
        measString='slowdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'middle', 'datatype':'met'}
    
    elif fname.find('WLEF_mid_ts')>=0:
        dbname='wlefMidHF'
        measString='fastdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'middle', 'datatype':'ts'}


#WLEF Top

    elif fname.find('WLEF_top_slow')>=0:
        dbname='wlefTopLF'
        measString='slowdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'top', 'datatype':'met'}

    elif fname.find('WLEF_top_ts')>=0:
        dbname='wlefTopHF'
        measString='fastdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'top', 'datatype':'ts'}

# WLEF surface

    elif fname.find('newtrailer_metvalue')>=0:
        dbname='wlefnewtrailerM'
        measString='slowdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'surface', 'datatype':'met'}

    elif fname.find('newtrailer_diagnostics')>=0:
        dbname='wlefnewtrailerD'
        measString='slowdata'
        tag_dict={'project':'Ameriflux','site':'WLEF', 'level':'surface', 'datatype':'diag'}

# Kernza
    elif fname.find('Kernza_surfaceobs')>=0:
        dbname='Kernza'
        measString='slowdata'
        tag_dict={'project':'USDA','site':'Kernza', 'level':'surface', 'datatype':'met'}

    elif fname.find('Kernza_Time_Series')>=0:
        dbname='Kernza'
        measString='fastdata'
        tag_dict={'project':'USDA','site':'Kernza', 'level':'surface', 'datatype':'ts', 'wdOffset':170}
    #print(dbname,measString, tag_dict)
    return (dbname, measString, tag_dict)
