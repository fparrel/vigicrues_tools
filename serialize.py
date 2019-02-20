
import struct
import datetime
import os
import time

def mkdirp(path):
    try:
        os.makedirs(path)
    except:
        pass

# So here is how we will serialize: an unsigned integer representing the timestamp, and a float representing the value
serialisation = '<Lf'
value_size = struct.calcsize(serialisation)

def get_lastupdatetime(domain,station_id):

    # Open the file for appending, create new file is needed. 'b' (binary) flag is needed on windows
    try:
        f = open('data/%s/%s.dat' % (domain, station_id), 'rb')
    except:
        return None
        #return datetime.datetime.fromtimestamp(0)

    # Seek to the end (it seems that a+b opening do not seek to the end)
    f.seek(0, os.SEEK_END)

    # Find the values already in the file
    if f.tell() > value_size:
        # Read and parse last value
        f.seek(-value_size,os.SEEK_END)
        last_value = struct.unpack(serialisation,f.read(value_size))
        last_datetime = datetime.datetime.fromtimestamp(last_value[0])
        return last_datetime

    #return datetime.datetime.fromtimestamp(0)
    return None

def save_values(domain,station_id,values):
    # Be low tech: I could have put the data in a db like MongoDB. But this code lead to the minimal disk access needed

    # Open the file for appending, create new file is needed. 'b' (binary) flag is needed on windows
    mkdirp('data/%s' % (domain))
    f = open('data/%s/%s.dat' % (domain, station_id), 'a+b')

    # Seek to the end (it seems that a+b opening do not seek to the end)
    f.seek(0,os.SEEK_END)

    # Find the values already in the file
    minidx = 0
    if f.tell() > value_size:
        # Read and parse last value
        f.seek(-value_size, os.SEEK_END)
        last_value = struct.unpack(serialisation,f.read(value_size))
        last_datetime = datetime.datetime.fromtimestamp(last_value[0])
        print('last from .dat: %s, from http server: %s - %s' % (last_datetime, values[0][0], values[-1][0]))
        # Discard values from scraping that are older than last value from file
        for dt, v in values:
            if last_datetime < dt:
                break
            minidx += 1

    # Seek back to the end: even if we did seek(-value_size) and read(value_size), seeking is mandatory on windows bettween read and write
    f.seek(0,os.SEEK_END)
    # Append data to the file
    buf = ''.join(map(lambda v: struct.pack(serialisation,time.mktime(v[0].timetuple()),v[1]),list(values)[minidx:]))
    f.write(buf)
    f.close()

def check_data(domain,station_id):
    fname = 'data/%s/%s.dat' % (domain, station_id)
    f = open(fname, 'r')
    # check that we have t in growing order
    t_prev = 0
    min_v = None
    max_v = None
    while True:
        r = f.read(value_size)
        if len(r)<value_size:
            # end of file
            break
        t, v = struct.unpack(serialisation,r)
        if t < t_prev:
            print t,t_prev
            f.close()
            return False, min_v, max_v
        if min_v==None or min_v>v:
            min_v = v
        if max_v==None or max_v<v:
            max_v = v
        t_prev = t
    f.close()
    return True, min_v, max_v

def repair_data(domain,station_id):
    fname = 'data/%s/%s.dat' % (domain, station_id)
    f = open(fname, 'r')
    values = []
    while True:
        r = f.read(value_size)
        if len(r)<value_size:
            # end of file
            break
        values.append(struct.unpack(serialisation,r))
    if domain=='chgalicia':
	print len(values)
        values = filter(lambda tv:tv[1]!=-9999.0, values) # Filter undef
        print len(values)
    values.sort(key=lambda tv:tv[0])
    f = open(fname, 'w')
    f.write(''.join([struct.pack(serialisation,tv[0],tv[1]) for tv in values]))
    f.close()

