#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import json
import re
import datetime
from serialize import save_values, get_lastupdatetime

cotes_re = re.compile(r', derni&egrave;re valeur (-?[0-9 ]*\.?[0-9]*) m le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')
debits_re = re.compile(r', derni&egrave;re valeur (-?[0-9 ]*\.?[0-9]*) m3/s le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')
cumul_horare_re = re.compile(r', dernier cumul horaire (-?[0-9 ]*\.?[0-9]*) mm le ([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) - ([0-9][0-9]):([0-9][0-9])')


def find_value(regex,t):
    for found in regex.findall(t):
        val,dd,mm,yyyy,hour,minute = found
        return (datetime.datetime(int(yyyy),int(mm),int(dd),int(hour),int(minute)),float(val.replace(' ','')))


def process(code_station, minfreq):
    lasts = filter(lambda x:not(x is None),(get_lastupdatetime('rdbrmc','pluie_%s'%code_station),get_lastupdatetime('rdbrmc','cote_%s'%code_station),get_lastupdatetime('rdbrmc','debit_%s'%code_station)))
    if len(lasts)>0:
        last_upd=min(lasts)
        if minfreq==-1:
            minfreq = 5
        #print 'Must not be updated before',last_upd+datetime.timedelta(minutes=minfreq)
        if last_upd+datetime.timedelta(minutes=minfreq)>datetime.datetime.now():
            print 'Skip %s: %s > %s'%(code_station,last_upd+datetime.timedelta(minutes=minfreq),datetime.datetime.now())
            return
    else:
        print '%s: no previous values'%code_station
    #return
    url = 'http://www.rdbrmc.com/hydroreel2/station.php?codestation=%d'%code_station
    print url
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    value_pluie = find_value(cumul_horare_re,t)
    value_cote = find_value(cotes_re,t)
    value_debit = find_value(debits_re,t)
    #print value_debit
    if value_pluie!=None:
        save_values('rdbrmc','pluie_%s'%code_station,[value_pluie])
    if value_cote!=None: 
        save_values('rdbrmc','cote_%s'%code_station,[value_cote])
    if value_debit!=None:
        save_values('rdbrmc','debit_%s'%code_station,[value_debit])

toignore = (235,260,1327)

if __name__=='__main__':
    #process(692,5)
    #exit()
    f=open('stations_rdbrmc.json','r')
    stations = json.load(f)
    f.close()
    freq4id={}
    for station in stations:
        id = station['id']
        if id in toignore:
            continue
        if id not in freq4id:
            freq4id[id]=station['freq']
        else:
            if station['freq']<freq4id[id]:
                freq4id = station['freq']
    for id,minfreq in freq4id.iteritems():
        process(id,minfreq)

