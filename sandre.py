import requests
from lxml import etree
import pyproj

lambert = pyproj.Proj('+init=EPSG:27572')
proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')

def getLatLonFromSandreId(station_id):
    r = requests.post('http://hydro.eaufrance.fr/presentation/procedure.php',{'categorie':'rechercher','station[]':[station_id],'procedure':'FICHE-STATION'})
    html = r.text.encode(r.encoding)
    tree = etree.HTML(html)
    try:
        x, y = map(float, tree.xpath('//h3[.="Localisation"]/following::td/text()')[:2])
    except:
        return None, None
    lon,lat = pyproj.transform(lambert,proj_latlon,x,y)
    return lat,lon

