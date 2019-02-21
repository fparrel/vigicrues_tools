#!/usr/bin/env python

import requests
from lxml import etree
import json

def getHistXml(station_id,nb,letter):
    url = 'http://www.chguadalquivir.es/saih/saihhist2.aspx?s1=%s_%d%s&dia=1'%(station_id,nb,letter)
    print(url)
    r = requests.get(url)
    return etree.XML(r.text.encode(r.encoding))
  

def findSenal(station_id):
    if station_id.startswith('A'): # For Aforos, first check 211_X
        t = getHistXml(station_id,211,'_X')
        if t.find('uni').text=='Sin datos': # If 211_X doesn't work check for level instead of flow
            for nb in range(100,110):
                t = getHistXml(station_id,nb,'')
                if t.find('uni').text=='Sin datos':
                      continue
                else:
                      return nb,t.find('descr').text,'',t.find('uni').text
            return None,None,None,None
        else:
            return 211,t.find('descr').text,'_X',t.find('uni').text
    nb_chosen = None
    senal_chosen = None
    letter_chosen = None
    for letter in ('_X','_D',''):
        for nb in range(211,225): # For CentralesHidroelectricas, search for 'caudal circulante' or 'caudal turbinado'
            t = getHistXml(station_id,nb,letter)
            if t.find('uni')=='Sin datos':
                continue
            senal_desc = t.find('descr').text
            if senal_desc==None:
                #print 'Ignoring %s'%url
                continue
            if ('CAUDAL CIRCULANTE' in senal_desc) or ('CAUDAL TURBINADO' in senal_desc and nb_chosen==None) or \
               ('CAUDAL DESEMBALSADO' in senal_desc and nb_chosen==None): # caudal circulante is proritary
                nb_chosen = nb
                senal_chosen = senal_desc
                letter_chosen = letter
                uni = t.find('uni').text
        if letter=='_X' and nb_chosen!=None:
            break
    return nb_chosen,senal_chosen,letter_chosen,uni


def main():
    types = ['CentralesHidroelectricas','Aforos']

    stations = []
    for typ in types:
        url = 'http://www.chguadalquivir.es/saih/saihxml.aspx?id=%s'%typ
        r = requests.get(url)
        xmls = r.text.encode(r.encoding)
        xmlt = etree.XML(xmls)
        for aforo in xmlt:
            name = aforo.find('name').text
            print 'Processing %s'%name
            lat = float(aforo.find('lat').text)
            lon = float(aforo.find('long').text)
            desc1 = aforo.find('DescripcionRemota').text
            desc2 = aforo.find('DescripcionSenal').text
            if desc2=='CAUDAL TURBINADO':
                river = ' '.join(desc1.split(' ')[1:-1])
            if desc2==None:
                print 'Skip %s'%name
                continue
            elif desc2.startswith('CAUDAL EN RIO'):
                river = desc2[14:]
            elif desc2.startswith('CAUDAL RIO'):
                river = desc2[11:]
            elif desc2.startswith('CAUDAL ARROYO'):
                river = desc2[7:]
            station_id = name.split('_')[0]
            nb, senal, letter, uni = findSenal(station_id)
            uni = uni.strip()
            if nb==None:
                raise Exception('Caudal not found for %s'%station_id)
            station = {'id':station_id,'name':name,'lat':lat,'lon':lon,'river':river,'desc_alt':desc1, \
                      'desc':senal,'nb':nb,'letter':letter,'unit':uni, \
                      'url':'http://www.chguadalquivir.es/saih/saihhist2.aspx?s1=%s_%d%s&dia=1'%(station_id,nb,letter)}
            #print station
            stations.append(station)
    print('Found %d stations'%len(stations))
    f = open('stations_chguadalquivir.json','w')
    json.dump(stations,f)
    f.close()

if __name__=='__main__':
    main()

