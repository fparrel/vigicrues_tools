#!/usr/bin/env python

import struct
import json
import datetime
import os
import sys

serialisation='<Lf'
value_size = struct.calcsize(serialisation)

def dat2csv(domain,station_id,min_date,do_last=False,nb_min=15):

    # Open the .dat file, ignore if not found
    fname = 'data/%s/%s.dat'%(domain,station_id)
    try:
        fdat = open(fname,'rb')
    except:
        print 'Warning: Cannot open %s'%fname
        return

    # Get last timestamp from csv file
    try:
        with open('viewer/%s.csv'%station_id,'r') as fcsvfull:
            fcsvfull.seek(-100,os.SEEK_END)
            for line in fcsvfull:
                last_line = line
            last_from_csv = int(last_line.split(',')[0])
    except:
        last_from_csv = 0
    #print station_id,last_from_csv

    if last_from_csv==0:
        # csv file doesn't exist, build it from scratch
        fcsvfull = open('viewer/%s/%s.csv'%(domain,station_id),'w')
        fcsvfull.write('datetime,value\n')
    else:
        # csv file exists, just append
        fcsvfull = open('viewer/%s/%s.csv'%(domain,station_id),'a')

    # open '-last.csv' file if asked
    if do_last:
        fcsvlast = open('viewer/%s/%s-last.csv'%(domain,station_id),'w')
        fcsvlast.write('datetime,value\n')

    nb_on_last = 0
    last_lines = []

    while True:

        # Read from .dat file
        buf = fdat.read(value_size)
        if len(buf)>0:

            # Deserialize
            timestamp,value = struct.unpack(serialisation,buf)

            # Append to csv if needed
            if timestamp>last_from_csv:
                csvline = '%s,%f\n'%(timestamp,value)
                fcsvfull.write(csvline)

            # Append to -last.csv file if asked
            if do_last:
                last_lines.append(csvline)
                last_lines=last_lines[:nb_min]
                if datetime.date.fromtimestamp(timestamp)>=min_date:
                    fcsvlast.write(csvline)
                    nb_on_last += 1
        else:
            break

    # Add last line to -last.csv if needed
    if do_last and nb_on_last<nb_min:
        fcsvlast.write(''.join(last_lines))

    # Close files
    fcsvfull.close()
    if do_last:
        fcsvlast.close()
    fdat.close()

if __name__=='__main__':
    if len(sys.argv)>1:
        domains = sys.argv[1:]
    else:
        domains = ['vigicrues','rdbrmc']
    if 'vigicrues' in domains:
        f = open('stations.json','r')
        stations = json.load(f)
        f.close()
        for station in stations:
            dat2csv('vigicrues',station['id'],datetime.date.today())
            dat2csv('vigicrues','%s-q'%station['id'],datetime.date.today())
    if 'rdbrmc' in domains:
        f = open('stations_rdbrmc.json','r')
        stations2 = json.load(f)
        f.close()
        ids = set(map(lambda s:s['id'],stations2))
        for id in ids:
            dat2csv('rdbrmc','pluie_%s'%id,datetime.date.today())
            dat2csv('rdbrmc','debit_%s'%id,datetime.date.today())
            dat2csv('rdbrmc','cote_%s'%id,datetime.date.today())

