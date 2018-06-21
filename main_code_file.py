from googleplaces import GooglePlaces, types, lang
from decimal import Decimal
from pprint import pprint
import json
import math
import numpy as np
import urllib.request
import ast

# This function is needed to avoid json.dump decimal storage error 
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# given the coordinates of two points, step value and your api key
# this function will calculate all the unique point of interests (POIs)
# in the rectangle defined by the two points
# step must be given in float value
def scanAreaForPOIs(lat1, long1, lat2, long2, step, your_api):
	
	google_places = GooglePlaces(your_api)

	Id_of_places = {}
	place_details = []
	# sorting the given latitudes
	x_cords = [lat1, lat2]
	x_cords.sort()

	# sorting the given longitudes
	y_cords = [long1, long2]
	y_cords.sort()

    # storing all the latitude & longitude points 
	x_points = np.arange(x_cords[0], x_cords[1], float(step))
	y_points = np.arange(y_cords[0], y_cords[1], float(step))


	k = 0 # to keep in check google api limit of 1000 requests per 24h
	
	# traversing through all the latitude and longitude points
	for i in range(len(x_points)):
		x = x_points[i]		#lat
		for j in range(len(y_points)):
			y = y_points[j]		#long
			
			#print(x, y)

			# querying google api
			query_result = google_places.nearby_search(
				location=str(x) + ',' + str(y), radius=50)


			# getting ID's from the specified location
			for place in query_result.places:

				plId = str(place.place_id)
				place.get_details()
				place_details.append(place.details)

				
				
				if plId not in Id_of_places:	
					# save place		
					Id_of_places[plId] = True
				
				
				else:	
					# store it as a false place
					Id_of_places[plId] = False
				

			# Breaking both loops to avoid reaching limit		
			k += 1
			if (k == 100):
				print("breaking loop")
				break

		if (k == 100):
			print("breaking loop")
			break

	Id_of_places = [key for key, value in Id_of_places.items() if value]
	#pprint(Id_of_places)	
	
	for i in range(len(place_details)):
		data = json.loads(json.dumps(place_details[i], default=decimal_default))

		if str(data["place_id"]) in Id_of_places:
			#print(str(data["place_id"]))
			with open('scarborough\\'+ str(data["place_id"]) +'.json', 'w') as outfile:
			 	json.dump(place_details[i], outfile, indent=4, default=decimal_default)

	
	# store Id_of_places outside loop
	with open('storing_all_ID.json', 'a') as outfile:
		json.dump(Id_of_places, outfile, indent=2)



YOUR_API_KEY = 'AIzaSyAb_1rwhupc22kzQXzIAsybx6dz2RlT2uA'

# using bigger step value to avoid reaching api limit
scanAreaForPOIs(43.766771, -79.324935, 43.757643, -79.169527, 0.001, YOUR_API_KEY)  

