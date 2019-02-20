#!/usr/bin/env python

from serialize import check_data,repair_data
import os
import sys

disp_minmax = '--minmax' in sys.argv

for domain in os.listdir('data'):
    print domain
    for fname in os.listdir('data/%s'%domain):
        c,min_v,max_v = check_data(domain,fname[:-4])
        if c==False:
            print 'Error in data/%s/%s'%(domain,fname)
            repair_data(domain,fname[:-4])
        elif disp_minmax:
            print '%s/%s : %f %f' % (domain,fname,min_v,max_v)

