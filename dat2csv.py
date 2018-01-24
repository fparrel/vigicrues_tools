#!/usr/bin/env python

import struct
import json
import datetime
import os

serialisation='<Lf'
value_size = struct.calcsize(serialisation)

def dat2csv(station_id,min_date,do_last=False,nb_min=15):

    # Open the .dat file, ignore if not found
    try:
        fdat = open('data/%s.dat'%station_id,'rb')
    except:
        print 'Warning: Cannot open %s'%station_id
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
        fcsvfull = open('viewer/%s.csv'%station_id,'w')
        fcsvfull.write('datetime,value\n')
    else:
        # csv file exists, just append
        fcsvfull=open('viewer/%s.csv'%station_id,'a')

    # open '-last.csv' file if asked
    if do_last:
        fcsvlast = open('viewer/%s-last.csv'%station_id,'w')
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
    f = open('stations.json','r')
    stations = json.load(f)
    f.close()
    for station in stations:
        dat2csv(station['id'],datetime.date.today())
        dat2csv('%s-q'%station['id'],datetime.date.today())

