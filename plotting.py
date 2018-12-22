from gmplot import gmplot

API_KEY = 'AIzaSyDpADSuP30VRsIDPMc6orgqjej-v2AIaBc'

gmap = gmplot.GoogleMapPlotter(43.659761, -79.420423, 13, API_KEY)

with open("points_to_plot.txt") as f:
	for line in f:
		#print(line)
		w, h = (str(line).replace("(", "").replace(")", "").split(','))
		
		gmap.marker(float(w), float(h), 'blue')

# Draw
gmap.draw("my_map.html")