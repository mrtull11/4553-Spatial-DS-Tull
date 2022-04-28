import json
from pprint import pprint
import random

def randColor():
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r()))
  


def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {
      
    },
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
    else:
      feature['properties'][key] = val

  feature['properties']["marker-color"]= randColor()
  feature['properties']["marker-size"]= 'medium'
  return feature

  
def makeLineString(city):
  feature = {
    "type": "Feature",
    "properties": {
      "color":randColor()
    },
    "geometry": {
      "type": "LineString",
      "coordinates": []
    }
  }
  cords=[0,0]
  for key, val in city.items():
    if key == 'latitude':
       cords[1] = val
    elif key == 'longitude':
      cords[0] = val
  feature['geometry']['coordinates'].append(cords)
  return feature



with open("data.json") as f:
  data = json.load(f)

data_sorted = sorted(data, key=lambda x: x['population'], reverse = True)

#print(data_sorted)

states = {}

for city in data_sorted:
  if not city["state"] in states:
    states[city["state"]] = city

    
  #print(city['population'])



 
    
#print(len(states))  


points = {
            "type": "FeatureCollection",
            "features": []
        }
statesLine = makeLineString(states["Oregon"])

  
for state,Info in states.items():
  
  points['features'].append(makePoint(Info))
  statesLine['geometry']['coordinates'].append(points['features'][-1]['geometry']['coordinates'])

statesLine['geometry']['coordinates'] = sorted(statesLine['geometry']['coordinates'] , key=lambda k: [k[0], k[1]])
points['features'].append(statesLine)

with open("new4.geojson","w") as f:
  json.dump(points,f,indent=4)



print(statesLine)
