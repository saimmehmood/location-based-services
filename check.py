from gmplot import gmplot
import os, json
# Place map
gmap = gmplot.GoogleMapPlotter(43.659761, -79.420423, 13)


#import pandas as pd

def getData():

	path_to_json = 'C:\\Users\\saim\\Documents\\location_based_services\\toronto_new'
	json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
	data = []
	for i in range(len(json_files)):
		#print(json_files[i])
		with open(path_to_json + '\\' + str(json_files[i])) as file:
			data = json.load(file)
			print(data["geometry"]["location"]["lat"], data["geometry"]["location"]["lng"])

getData()
# 	return data

# gettingData = getData()

# print (gettingData)

# Polygon
#golden_gate_park_lats, golden_gate_park_lons = zip(*[
 #   (data["geometry"]["location"]["lat"], data["geometry"]["location"]["lng"])
    # (37.773495, -122.464830),
    # (37.774797, -122.454538),
    # (37.771988, -122.454018),
    # (37.773646, -122.440979),
    # (37.772742, -122.440797),
    # (37.771096, -122.453889),
    # (37.768669, -122.453518),
    # (37.766227, -122.460213),
    # (37.764028, -122.510347),
    # (37.771269, -122.511015)
#    ])
#gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)


# # Marker
# hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
# gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# Draw
#gmap.draw("my_map.html")



		 