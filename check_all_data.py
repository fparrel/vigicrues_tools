#!/usr/bin/env python

from serialize import checkData,repairData
import os
import sys

disp_minmax = '--minmax' in sys.argv

for domain in os.listdir('data'):
    print(domain)
    for fname in os.listdir('data/%s'%domain):
        c,min_v,max_v = checkData(domain,fname[:-4])
        if c==False:
            print('Error in data/%s/%s'%(domain,fname))
            repairData(domain,fname[:-4])
        elif disp_minmax:
            print('%s/%s : %f %f' % (domain,fname,min_v,max_v))

