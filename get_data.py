
import requests
import os
import sys
import jinja2 as jin
import os
import sys
import csv
import json

MONTE_TOKEN = os.environ['STRAVA_MONTE']
HILARY_TOKEN = os.environ['STRAVA_HILARY']

template = jin.Template("""
<html>
  <head>
    <title>Hilary's summer</title>
  </head>

  <body>
    <script src="https://cdn.leafletjs.com/leaflet-0.7/leaflet.js"></script>
    <script type="text/javascript" src="https://rawgit.com/jieter/Leaflet.encoded/master/Polyline.encoded.js"></script>
    <link rel="stylesheet" href="https://cdn.leafletjs.com/leaflet-0.7/leaflet.css" />
    <div id="map" style="width: 100%; height: 100%"></div>

    <script>
    
   
    
    var map = L.map('map').setView([40.0150, -105.2705], 11);
    

    var Stamen_Watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        subdomains: 'abcd',
        minZoom: 1,
        maxZoom: 16,
        ext: 'png'
    }).addTo(map);
    
    var encodedRoutesRides = {{polyRides}};
    for (let encoded of encodedRoutesRides) {
      var coordinates = L.Polyline.fromEncoded(encoded).getLatLngs();
      L.polyline(
          coordinates,
          {
              color: 'darkblue',
              weight: 3,
              opacity: .5,
              lineJoin: 'round'
          }
      ).addTo(map);
    }

    var encodedRoutes = {{polylines}};
    for (let encoded of encodedRoutes) {
      var coordinates = L.Polyline.fromEncoded(encoded).getLatLngs();
      L.polyline(
          coordinates,
          {
              color: 'red',
              weight: 3,
              opacity: .5,
              lineJoin: 'round'
          }
      ).addTo(map);
      
      
    }
    </script>
  </body>
</html>
""")

if __name__ == "__main__":


    token = HILARY_TOKEN
    token = MONTE_TOKEN

    headers = {'Authorization': "Bearer {0}".format(token)}

    lines = []
    rides = []
    data = []
    page = 1
    current_length = 0
    while True:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities/?page={}".format(page), headers = headers)
        page += 1
        response = r.json()
        print(page, r.status_code, len(rides))
        
        for res in response:
            data.append(res)
            if res['type']=='Ride':
                rides.append(res['map']['summary_polyline'])
            else:
                lines.append(res['map']['summary_polyline'])
        if len(lines) + len(rides) == current_length:
            break
            
        current_length = len(lines) + len(rides)

    print(len(lines) + len(rides))


    with open('index.html', 'w') as outfile:
        outfile.write(template.render(polylines=json.dumps([ x for x in lines if x]),
                                      polyRides=json.dumps([ x for x in rides if x]),
                                    ))

