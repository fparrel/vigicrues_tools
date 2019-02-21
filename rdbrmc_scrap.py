#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import json
import re
import datetime
from serialize import saveValues, loadStations, getLastUpdateTime

stations_ids_to_ignore = (235,260,1327)

cotes_re = re.compile(r', derni&egrave;re valeur (-?[0-9 ]*\.?[0-9]*) m le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')
debits_re = re.compile(r', derni&egrave;re valeur (-?[0-9 ]*\.?[0-9]*) m3/s le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')
cumul_horare_re = re.compile(r', dernier cumul horaire (-?[0-9 ]*\.?[0-9]*) mm le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')

def findValue(regex,t):
    for found in regex.findall(t):
        val,dd,mm,yyyy,hour,minute = found
        return (datetime.datetime(int(yyyy),int(mm),int(dd),int(hour),int(minute)),float(val.replace(' ','')))

def process(code_station, minfreq):
    lasts = filter(lambda x:not(x is None),(getLastUpdateTime('rdbrmc','pluie_%s'%code_station),getLastUpdateTime('rdbrmc','cote_%s'%code_station),getLastUpdateTime('rdbrmc','debit_%s'%code_station)))
    if len(lasts)>0:
        last_upd = min(lasts)
        if minfreq==-1:
            minfreq = 5
        #print 'Must not be updated before',last_upd+datetime.timedelta(minutes=minfreq)
        if last_upd+datetime.timedelta(minutes=minfreq)>datetime.datetime.now():
            print('Skip %s: %s > %s'%(code_station,last_upd+datetime.timedelta(minutes=minfreq),datetime.datetime.now()))
            return
    else:
        print('%s: no previous values' % code_station)
    url = 'http://www.rdbrmc.com/hydroreel2/station.php?codestation=%d'%code_station
    print(url)
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    value_pluie = findValue(cumul_horare_re,t)
    value_cote = findValue(cotes_re,t)
    value_debit = findValue(debits_re,t)
    if value_pluie!=None:
        saveValues('rdbrmc', 'pluie_%s' % code_station,[value_pluie])
    if value_cote!=None: 
        saveValues('rdbrmc', 'cote_%s' % code_station,[value_cote])
    if value_debit!=None:
        saveValues('rdbrmc', 'debit_%s' % code_station,[value_debit])

if __name__=='__main__':
    freq4id = {}
    for station in loadStations('rdbrmc'):
        station_id = station['id']
        if station_id in stations_ids_to_ignore:
            continue
        if station_id not in freq4id:
            freq4id[station_id] = station['freq']
        else:
            if station['freq'] < freq4id[station_id]:
                freq4id = station['freq']
    for station_id,minfreq in freq4id.iteritems():
        process(station_id,minfreq)

