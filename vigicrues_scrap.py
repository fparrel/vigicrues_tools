#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests #for http requests
import datetime #for datetime parsing
import os #for seeking in file
import struct #for serialization
import time #for datetime serialization
import json

def parse_values(t):
    i = t.find('<map name="__mapname')
    while i!=-1:
        j = t.find('title="',i)
        if j!=-1:
            k = t.find('alt="',j)
            if k!=-1:
                v = map(str.strip,t[j+6:k].strip('" ').split('Valeur mesurée ='))
                yield datetime.datetime.strptime(v[0],'%d/%m/%Y %H:%M'),float(v[1])
        else:
            k=-1
        i = k

def save_values(station_id,values):
    # Be low tech: I could have put the data in a db like MongoDB. But this code lead to the minimal disk access needed

    # So here is how we will serialize: an unsigned integer representing the timestamp, and a float representing the value
    serialisation='<Lf'
    value_size = struct.calcsize(serialisation)

    # Open the file for appending, create new file is needed. 'b' (binary) flag is needed on windows
    f=open('%s.dat'%station_id,'a+b')

    # Seek to the end (it seems that a+b opening do not seek to the end)
    f.seek(0,os.SEEK_END)

    # Find the values already in the file
    minidx = 0
    if f.tell()>value_size:
        # Read and parse last value
        f.seek(-value_size,os.SEEK_END)
        last_value = struct.unpack(serialisation,f.read(value_size))
        last_datetime = datetime.datetime.fromtimestamp(last_value[0])
        # Discard values from scraping that are older than last value from file
        for dt,v in values:
            if last_datetime<dt:
                break
            minidx+=1

    # Seek back to the end: even if we did seek(-value_size) and read(value_size), seeking is mandatory on windows bettween read and write
    f.seek(0,os.SEEK_END)
    # Append data to the file
    buffer = ''.join(map(lambda v: struct.pack(serialisation,time.mktime(v[0].timetuple()),v[1]),list(values)[minidx:]))
    f.write(buffer)
    f.close()

def process(station_id):
    r = requests.get('http://www.vigicrues.gouv.fr/niveau3.php?CdEntVigiCru=22&CdStationHydro=%(station_id)s'%{'station_id':station_id})
    t = r.text.encode(r.encoding)
    values = parse_values(t)
    save_values(station_id,values)

if __name__=='__main__':
    f=open('viewer/stations.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        process(station['id'])
