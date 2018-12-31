import json

rivers = json.load(open("forRiverApp.json","r"))
stations = json.load(open("stations_chtajo.json","r"))

rs = {}
for s in stations:
    r = s.get('river')
    if r in rs:
        rs[r].append(s['id'])
    else:
        rs[r] = [s['id']]

