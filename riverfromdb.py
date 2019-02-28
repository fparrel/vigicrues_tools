import pymongo
from math import sin,cos,atan2,sqrt

c = pymongo.MongoClient()
print('Loading rivers from db...')
rivers = list(c['wwsupdb']['osm'].find({},{'paths':True}))
print('Loaded %d rivers'%len(rivers))

def GeodeticDistGreatCircle(lat1,lon1,lat2,lon2):
    "Compute distance between two points of the earth geoid (approximated to a sphere)"
    # convert inputs in degrees to radians
    lat1 = lat1 * 0.0174532925199433
    lon1 = lon1 * 0.0174532925199433
    lat2 = lat2 * 0.0174532925199433
    lon2 = lon2 * 0.0174532925199433
    # just draw a schema of two points on a sphere and two radius and you'll understand
    a = sin((lat2 - lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1)/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # earth mean radius is 6371 km
    return 6372795.0 * c

def findRiver(lat,lon,hardcodedrivers={}):
    for latlon,name in hardcodedrivers.iteritems():
        if GeodeticDistGreatCircle(lat,lon,latlon[0],latlon[1])<10.0:
            return name
    m = None
    rid = None
    for river in rivers:
        for path in river['paths']:
            for pt in path:
                d = GeodeticDistGreatCircle(lat,lon,pt[0],pt[1])
                if m==None or d<m:
                    m = d
                    rid = river['_id']
                #if d<200.0:
                #    return river['_id']
    #print 'min=%f'%m
    if m<700.0:
        return rid
    return None

