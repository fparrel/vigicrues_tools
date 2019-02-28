#!/usr/bin/env python

import requests
import re
import yaml
import json
import utm
from riverfromdb import findRiver

def getData(url):
    print(url)
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    i = t.find('data:')
    if i==-1:
        raise Exception('Cannot find begin')
    j = t.find('}',i)
    if j==-1:
        raise Exception('Cannot find end')
    return yaml.load('{'+t[i:j]+'}')

def main():
    url = 'http://www.arpa.piemonte.it/rischinaturali/tematismi/meteo/osservazioni/rete-meteoidrografica/rete-meteo-idrografica.html'
    print(url)
    r = requests.get(url)
    t = r.text.encode(r.encoding)
    pat = re.compile(r'var featurecircle = new OpenLayers.Feature.Vector\(origin, {\s*denominazione: "(.*)",\s*id_venue: "(.*)",\s*quota: "(.*)",\s*indirizzo: "(.*)",\s*tipo_staz: "(.*)",\s*utm_est: "(.*)",\s*utm_nord: "(.*)",\s*visibility: "(.*)"\s*}\s*\);')
    stations = []
    for name,station_id,alt,a,station_type,utm_x,utm_y,visible in pat.findall(t):
        alt = int(alt)
        utm_x = int(utm_x)
        utm_y = int(utm_y)
        lat, lon = utm.to_latlon(utm_x,utm_y,32,'T')
        station = {'name':name,'station_id':station_id,'alt':alt,'province':a,'type':station_type,'utm_x':utm_x,'utm_y':utm_y,'lat':lat,'lon':lon}
        # type:
        # I = water level
        if 'I' in station_type:
            url = "http://www.arpa.piemonte.it/rischinaturali/fn_chart/chart_factory_update.jsp?$ID_PROVINCIA$='ALL'&$ID_BACINO$='ALL'&$ID_FASCIA$='ALL'&$ID_PARAMETRO$='IDRO'&$ID_VENUE$=%s&$ID_AGGREGAZIONE$=54&CHART_ID=grafico_semplice_parametri_tutti&CHART_NAME=chart_dt_tr_one.ID_VENUE.ID_PARAMETRO.ID_AGGREGAZIONE" % station_id
            url = url.replace("'","%27")
            station['url'] = url
            try:
                d = getData(url)
            except:
                print 'ERROR for %s'%name
                d = None
            if d!=None:
                station['desc'] = d['name']
                river = findRiver(lat, lon)
                if river!=None:
                    station['river'] = river
                stations.append(station)

    json.dump(stations,open('stations_arpapiemonte.json','w'))

if __name__=='__main__':
    main()

