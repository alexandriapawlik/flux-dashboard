#!/usr/bin/env python

import sys
import re
import logging
import struct
from datetime import datetime, timedelta
import binascii
import numpy as np

#
# input for all diagnostic decodes need to be arrays
# even a single item array [x, y, z, ....] or [z,]


#
# LI7700 diagnostics
#
#
#diag_7700 = tsarray[tskeys.index('Diag_li7700')]
def dd7700(stamp,diag_7700):
#
# initialize the variables
    records=[]
    variablenames=['not_ready_77', \
                   'nosignal_77', \
                   'refunlocked_77',\
                   'badtemp_77', \
                   'lasertunreg_77', \
                   'blocktunreg_77', \
                   'motorspin_77', \
                   'pumpon_77', \
                   'topheaton_77', \
                   'botheaton_77', \
                   'calibrating_77', \
                   'motorfail_77', \
                   'nominal7700_77']

    for i in range(len(diag_7700)):
        decoded=[0] * 13
        #32768 : not ready 2**15
        decoded[0]=((int(diag_7700[i]) & 32768) >>15)
        #16384 : nosignal 2**14
        decoded[1]=((int(diag_7700[i]) & 16384) >>14)
        #8192 : refunlocked 2**13
        decoded[2]=((int(diag_7700[i]) & 8192) >>13)
        #4096 : badtemp 2**12
        decoded[3]=((int(diag_7700[i]) & 4096) >>12)
        #2048 : lasertempunregulated 2**11
        decoded[4]=( (int(diag_7700[i]) & 2048) >>11)
        #1024 : blocktempunregulated 2**10
        decoded[5]=((int(diag_7700[i]) & 1024) >>10)
        #512 : motorspinning 2**9
        decoded[6]=((int(diag_7700[i]) & 512) >>9)
        #256 : pumpon 2**8
        decoded[7]=((int(diag_7700[i]) & 256) >>8)
        #128 : topHeateron 2**7
        decoded[8]=((int(diag_7700[i]) & 128) >>7)
        #64 : bottomheateron 2**6
        decoded[9]=((int(diag_7700[i]) & 64) >>6)
        #32 : calibrating 2**5
        decoded[10]=((int(diag_7700[i]) & 32) >>5)
        #16 : motorfailure 2**4
        decoded[11]=((int(diag_7700[i]) & 16) >>4)
        #14 : base number
        if int(diag_7700[i])==14:
           decoded[12]=1
#
        data={}
        for k,v in zip(variablenames,decoded):
            data[k]=v

        records.append((stamp[i],data)) 

    return records


#
# CSAT 3 diagnostics
#
#csat_diag=tsarray[tskeys.index('diag_csat')]

def ddcsat3(stamp,csat_diag):
#61502 : anemometer does not respond
#61440 : lost trigger
#61503 : no data available
#61441 : SDM Comms error
#61442 : Wrong CSAT3 embedded code
    records=[] 
    variablenames=['ux_range_c3', \
             'uy_range_c3', \
             'uz_range_c3', \
             'counter_c3', \
             'b12_c3', \
             'b13_c3', \
             'b14_c3', \
             'b15_c3' , \
             'csatdiag0_c3', \
             'csatdiag1_c3', \
             'csatdiag2_c3', \
             'csatdiag3_c3', \
             'csatdiag4_c3', \
             'csatdiag5_c3']
 
    for i in range(len(csat_diag)):
        decoded=[0]*14

        decoded[3] = int(csat_diag[i]) & 63
        decoded[2]=(int(csat_diag[i])&192) >> 6
        decoded[1]=(int(csat_diag[i])&768) >> 8
        decoded[0]=(int(csat_diag[i])&3072) >> 10
        decoded[4]=(int(csat_diag[i])&4096) >> 12
        decoded[5]=(int(csat_diag[i])&8192) >> 13
        decoded[6]=(int(csat_diag[i])&16384) >> 14
        decoded[7]=(int(csat_diag[i])&32768) >> 15

        if csat_diag[i]==61503:
            decoded[13]=1 
            for j in range(8):
                decoded[j]=0
        elif csat_diag[i]==61502:
            decoded[12]=1 
            for j in range(8):
                decoded[j]=0
        elif csat_diag[i]==61442:
            decoded[11]=1 
            for j in range(8):
                decoded[j]=0
        elif csat_diag[i]==61441:
            decoded[10]=1 
            for j in range(8):
                decoded[j]=0
        elif csat_diag[i]==61440:
            decoded[9]=1 
            for j in range(8):
                decoded[j]=0
        else:
            decoded[8]=1 

        data={}
        for k,v in zip(variablenames,decoded):
            data[k]=v

        records.append((stamp[i],data)) 

    return records
#
# LI7500 diaganostics
#
# input the original diagnostic value direct from sensor
def dd7500(stamp,diag_irga):
#
# LI7500 diaganostics
#
# 
# 
    records=[]
    variablenames=['signalstrength_75', \
                   'sync_75', \
                   'PLL_75', \
                   'detect_75', \
                   'chopper_75']

    for i in range(len(diag_irga)):
        decoded=[0] * 5
        decoded[0]=((int(diag_irga[i]) & 15) * 6.67)
        decoded[1]=(int(diag_irga[i]) & 16) >> 4
        decoded[2]=(int(diag_irga[i]) & 32) >> 5
        decoded[3]=(int(diag_irga[i]) & 64) >> 6
        decoded[4]=(int(diag_irga[i]) & 128) >> 7


        data={}
        for k,v in zip(variablenames,decoded):
            data[k]=v

        records.append((stamp[i],data)) 

    return records

# 
# 
# for now: change the diagnostic value back to its default value (this may change in the future)
#
def dd7200(stamp,diag_irga):

    records=[]
    variablenames=['signalstrength_72', \
             'sync_72', \
             'PLL_72', \
             'detector_72', \
             'chopper_72', \
             'diffpres_72', \
             'auxinput_72', \
             'Tinlet_72', \
             'Toutlet_72', \
             'headdetect_72']

    ss_7200 = [0] * len(diag_irga)   # signal strength
    headdetect = [0] * len(diag_irga)
    Toutlet = [0] * len(diag_irga)
    Tinlet= [0] * len(diag_irga)
    Aux_input = [0] * len(diag_irga)
    delta_pres = [0] * len(diag_irga)
    chopper = [0] * len(diag_irga)
    detect = [0] * len(diag_irga)
    PLL = [0] * len(diag_irga)
    sync = [0] * len(diag_irga)
    for i in range(len(diag_irga)):
        decoded=[0]*10
        decoded[0]=((int(diag_irga[i]) & 15) * 6.67)
        decoded[1]=(int(diag_irga[i]) & 16) >> 4
        decoded[2]=(int(diag_irga[i]) & 32) >> 5
        decoded[3]=(int(diag_irga[i]) & 64) >> 6
        decoded[4]=(int(diag_irga[i]) & 128) >> 7
        decoded[5]=(int(diag_irga[i]) & 256) >> 8
        decoded[6]=(int(diag_irga[i]) & 512) >> 9
        decoded[7]=(int(diag_irga[i]) & 1024) >> 10
        decoded[8]=(int(diag_irga[i]) & 2048) >> 11
        decoded[9]=(int(diag_irga[i]) & 4096) >> 12


        data={}
        for k,v in zip(variablenames,decoded):
            data[k]=v

        records.append((stamp[i],data)) 

    return records

