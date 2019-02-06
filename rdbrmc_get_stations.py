#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup # `pip install beautifulsoup4` or `apt install python-bs4`
import json

conv_freqs = {'Toutes les 12 heures':12*60, '3 heures hors crue, 1 heure en crue':60, 'trois fois par jour':4*60,
'Toutes les 12h, Horaire en crues':12*60, 'Toutes les heures':60, '12  heures hors crue ;1 heure en crue':60,
'Toutes les 12h':12*60, 'toutes les 30 minutes':30, 'toutes les 5mn':5, 'Mensuelle':24*60*30, '12H':12*60,
'toutes les heures en cotes, 1 à 2 fois par semaine pour les débits':60, 'Toutes les 15mn':5, 'Toutes les 15 mn':15,
'toutes les heures':60, '15 min':15, 'Trois fois par jour':4*60, 'toutes les 15mn':15, 'Quotidienne':24*60,
'Horaire':60, '3 fois par jour en situation normale (6h00, 14h00 et 22h00), toutes les 2 heures en crue.':2*60,
'Tous le jours':24*60, 'Toute les 15 mn':15, 'horaire':60, 'Toutes les 12 h et 1 h en crue':60, 'Toutes les 5mn':5,
'Une fois par jour':24*60, 'Tous les jours sauf week-end':24*60, '12 heures hors crue, 1 heure en crue;':60,
'Toutes les 5mn;':5, 'Journalière':24*60, '3 heures':3*60, 'le lundi':7*24*60,
'12 heures hors crue; 1 heure en crue;':60, '2 fois par jour (6h et 18h)':12*60, 'toutes les 6 heures':6*60,
'Toute les heures':60, '12h ':12*60, 'Toutes les 5 minutes':5, 'toutes les 24 heures (chaque jour) à 23 h 30.':24*60,
'24 heures':24*60, 'toutes les 15 minutes':15, 'toutes les 15 mn':15,
'3 fois par jour en situation normale (6h00, 14h00 et 22h00), toutes les 4 heures en crue.':4*60,
'12 heures hors crue, 1 heure en crues;':60, '3h en basses eaux,   30mn en hautes eaux':30, 'Toutes les 5 mn;':5,
'Toute les heures.':60, 'une fois par semaine':7*24*60, 'Toutes les 15 min':15,
'6h en basses eaux,   30mn en hautes eaux':30, '24 h à 13h30 utc (en attente fréquence + élevée)':24*60,
'2 fois par jour':12*60, '1h en basses eaux,   30mn en hautes eaux':30, '12 heures hors crue, 1 heure en crue':60,
'une fois par jour':24*60, 'Toutes les heures.':60, 'Hebdomadaire':7*24*60, '\tToutes les 15 mn':15,
'Toutes les 5 mn':5, '15mn':15, 'toutes les heures.':60, 'Deux fois par jour':12*60, '12':12*60,
'3h en basses eaux,    30mn en hautes eaux':30, '12h hors crue,1h en crue':60,
'12 heures hors crue;1 heure en crue':60, '1 h':60,
"24 h  à 13h30 utc  (provisoirement, en attente d'une fréquance + élevée)":24*60, '5mn':5,
'3 fois par jour (06h00, 14h00, 22h00) en situation normale, toutes les 4 heures en crue.':4*60, 'toutes les 30 mn':30,
'Toutes les 5 min':5, 'Toutes les 12H, Horaire en crue':60, '5 mn':5, 'toutes les 8 heures':8*60,
'Tous les jours':24*60, '30 min':30, 'Toutes les 15 minutes':15, '3 h en basses eaux,  30 mn en hautes eaux':30,
'toutes les 12 minutes':12, '15 minutes':15, 'toutes les 12h;1h en crue':60, 'toutes les 5 mn':5, '12 heures':12*60,
'2 fois par jour en situation normale (5h00 et 17h00)':12*60,
'Toutes les 5 min pour les hauteurs et les débits, toutes les heures pour la pluie':5, '2 fois par jour (6h et 18h).':12*60}

def getStations():
    url = "http://www.rdbrmc.com/hydroreel2/listestation.php"
    soup = BeautifulSoup(urllib2.urlopen(url), "lxml")
    prefix = 'station.php?codestation='
    for type in ('LIMNI','PLUVIO'):
        tbl = soup.find('a',attrs={'name':type}).find_parent().find_parent()
        links1 = [link.get('href') for link in tbl.find_all('a')]
        links = list(filter(lambda l: not(l is None), links1))
        names = [cell.get_text() for cell in tbl.find_all('td')]
        assert(len(links)*3==len(names))
        assert(links[0].startswith(prefix))
        for i in range(0,len(names),3):
            river = names[i].strip()
            station = names[i+1].strip()
            freq_str = names[i+2]
            if freq_str in conv_freqs:
                freq_min = conv_freqs[freq_str]
            else:
                freq_min = -1
            id = int(links[i/3][len(prefix):])
            yield(id,station,river,type,freq_str,freq_min)

def printFreqs():
    # Used to generate the `conv_freqs` dict
    freqs = set([])
    for id,station,river,type,freq_str,freq_min in getStations():
        freqs.add(freq_str)
    print(freqs)

def main():
    stations = []
    for id,station,river,type,freq_str,freq_min in getStations():
        stations.append({'id':id,'name':station,'river':river,'type':type,'freq':freq_min})

    json.dump(stations,open('stations_rdbrmc.json','w'))

if __name__=='__main__':
    main()
