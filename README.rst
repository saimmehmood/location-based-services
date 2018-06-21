python-google-places
=======================

.. _introduction:

**python-google-places** provides a simple wrapper around the experimental
Google Places API.


Installation
-----------------

.. _installation:

pip install https://github.com/slimkrazy/python-google-places/zipball/master

OR

pip install python-google-places

Download source and then:
python setup.py install


Prerequisites
-----------------
.. _prerequisites:

A Google API key with Google Places API Web Service and Google Maps Geocoding API activated against
it. Please check the Google API console, here: http://code.google.com/apis/console


Usage
------

.. _usage:

Code is easier to understand than words, so let us dive right in ::


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
            
                ### Commented some of this code to avoid computation cost. ###
                
				# # getting location of place's center
				# place_x = float(place.geo_location['lat'])
				# place_y = float(place.geo_location['lng'])
				
				# # getting location of place's center from the point we searched
				# distance = math.sqrt( math.pow(place_x - x, 2) + math.pow(place_y - y, 2) )

				# # if place's center is within our search and we haven't seen it before
				# if distance * 1000 < 1 and plId not in Id_of_places:
				
				if plId not in Id_of_places:	
					# save place		
					Id_of_places[plId] = True
				
				# # if place's center is far away and we haven't stored it, or we stored it incorrectly
				# elif distance * 1000 > 1 and (plId not in Id_of_places or Id_of_places[plId] == True):
				
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
			print(str(data["place_id"]))
			with open('scarborough\\'+ str(data["place_id"]) +'.json', 'w') as outfile:
			 	json.dump(place_details[i], outfile, indent=4, default=decimal_default)

	
	# store Id_of_places outside loop
	with open('storing_all_ID.json', 'a') as outfile:
		json.dump(Id_of_places, outfile, indent=2)



YOUR_API_KEY = ''

# using bigger step value to avoid reaching api limit

scanAreaForPOIs(43.766771, -79.324935, 43.757643, -79.169527, 0.001, YOUR_API_KEY)  

Reference
----------

::

    googleplaces.GooglePlacesError
    googleplaces.GooglePlacesAttributeError


    googleplaces.geocode_location(location, sensor=False, api_key=None)
      Converts a human-readable location to a Dict containing the keys: lat, lng.
      Raises googleplaces.GooglePlacesError if the geocoder fails to find the
      specified location.


    googleplaces.GooglePlaces
      nearby_search(**kwargs)
        Returns googleplaces.GooglePlacesSearchResult
          kwargs:
            keyword  -- A term to be matched against all available fields, including but
                        not limited to name, type, and address (default None)

            language -- The language code, indicating in which language the results
                        should be returned, if possble. (default en)

            lat_lng  -- A dict containing the following keys: lat, lng (default None)

            location -- A human readable location, e.g 'London, England' (default None)

            name     -- A term to be matched against the names of the Places.
                        Results will be restricted to those containing the passed name value. (default None)

            pagetoken-- Optional parameter to force the search result to return the next
                        20 results from a previously run search. Setting this parameter
                        will execute a search with the same parameters used previously. (default None)

            radius   -- The radius (in meters) around the location/lat_lng to restrict
                        the search to. The maximum is 50000 meters (default 3200)

            rankby   -- Specifies the order in which results are listed:
                        'prominence' (default) or 'distance' (imply no radius argument)

            sensor   -- Indicates whether or not the Place request came from a device
                        using a location sensor (default False)

            type     -- An optional type used for restricting the results to Places (default None)

            types    -- An optional list of types, restricting the results to Places (default []).
                        This kwarg has been deprecated in favour of the 'type' kwarg.



      text_search(**kwargs)
        Returns googleplaces.GooglePlacesSearchResult
          kwargs:
            query  --  The text string on which to search, for example:
                       "Restaurant in New York".

            lat_lng  -- A dict containing the following keys: lat, lng (default None)

            location -- A human readable location, e.g 'London, England' (default None)

            language -- The language code, indicating in which language the results
                        should be returned, if possble. (default en)

            pagetoken-- Optional parameter to force the search result to return the next
                        20 results from a previously run search. Setting this parameter
                        will execute a search with the same parameters used previously. (default None)

            radius   -- The radius (in meters) around the location/lat_lng to restrict
                        the search to. The maximum is 50000 meters (default 3200)

            type     -- An optional type used for restricting the results to Places (default None)

            types    -- An optional list of types, restricting the results to Places (default [])
                        This kwarg has been deprecated in favour of the 'type' kwarg.

      autocomplete(**kwargs):
        Returns googleplaces.GoogleAutocompleteSearchResult
          kwargs:
            input  --   The text string on which to search, for example:
                        "Hattie B's".

            lat_lng -- A dict containing the following keys: lat, lng (default None)

            location -- A human readable location, e.g 'London, England' (default None)

            radius   -- The radius (in meters) around the location to which the
                        search is to be restricted. The maximum is 50000 meters.
                        (default 3200)

            language -- The language code, indicating in which language the
                        results should be returned, if possible. (default lang.ENGLISH)

            types    -- A type to search against. See `types.py` "autocomplete types"
                        for complete list
                        https://developers.google.com/places/documentation/autocomplete#place_types.

            components -- An optional grouping of places to which you would
                        like to restrict your results. An array containing one or
                        more tuples of:
                        * country: matches a country name or a two letter ISO 3166-1 country code.
                        eg: [('country','US')]

      radar_search(**kwargs)
        Returns googleplaces.GooglePlacesSearchResult
          kwargs:
            keyword  -- A term to be matched against all available fields, including
                        but not limited to name, type, and address (default None)

            name     -- A term to be matched against the names of Places. Results will
                        be restricted to those containing the passed name value.

            opennow  -- Returns only those Places that are open for business at the time
                        the query is sent

            lat_lng  -- A dict containing the following keys: lat, lng (default None)

            location -- A human readable location, e.g 'London, England' (default None)

            language -- The language code, indicating in which language the results
                        should be returned, if possble. (default en)

            radius   -- The radius (in meters) around the location/lat_lng to restrict
                        the search to. The maximum is 50000 meters (default 3200)

            sensor   -- Indicates whether or not the Place request came from a
                        device using a location sensor (default False).

            type     -- An optional type used for restricting the results to Places (default None)

            types    -- An optional list of types, restricting the results to Places (default [])
                        This kwarg has been deprecated in favour of the 'type' kwarg.

      get_place(**kwargs)
        Returns a detailed instance of googleplaces.Place
          place_id  -- The unique Google identifier for the required place.

          language   -- The language code, indicating in which language the results
                        should be returned, if possble. (default en)

          sensor     -- Indicates whether or not the Place request came from a
                        device using a location sensor (default False).


      checkin(place_id, sensor=False)
        Checks in an anonymous user in to the Place that matches the place_id.
          kwargs:
            place_id   -- The unique Google identifier for the required place.

            sensor      -- Boolean flag denoting if the location came from a device
                           using its location sensor (default False).


      add_place(**kwargs)
        Returns a dict containing the following keys: place_id, id.
          kwargs:
            name        -- The full text name of the Place. Limited to 255
                           characters.

            lat_lng     -- A dict containing the following keys: lat, lng.

            accuracy    -- The accuracy of the location signal on which this request
                           is based, expressed in meters.

            types       -- The category in which this Place belongs. Only one type
                           can currently be specified for a Place. A string or
                           single element list may be passed in.

            language    -- The language in which the Place's name is being reported.
                           (default googleplaces.lang.ENGLISH).

            sensor      -- Boolean flag denoting if the location came from a device
                           using its location sensor (default False).


      delete_place(place_id, sensor=False)
        Deletes a place from the Google Places database.
          kwargs:
            place_id   -- The unique Google identifier for the required place.

            sensor      -- Boolean flag denoting if the location came from a
                           device using its location sensor (default False).


    googleplaces.GoogleAutocompleteSearchResult
      raw_response
        Returns the raw JSON response from the Autocomplete API.

      predictions
        Returns an array of prediction objects.


    googleplaces.GooglePlacesSearchResult
      raw_response
        The raw JSON response returned by the Google Places API.

      places
        A list of summary googleplaces.Place instances.

      has_attributions()
        Returns a flag indicating if the search result has html attributions that
        must be displayed.

      html_attributions()
        Returns a List of String html attributions that must be displayed along with
        the search results.


    googleplaces.Prediction
      description
        String representation of a Prediction location. Generally contains
        name, country, and elements contained in the terms property.

      id
        Returns a unique stable identifier denoting this Place. This identifier
        may not be used to retrieve information about this Place, but can be used
        to consolidate data about this Place, and to verify the identity of a
        Place across separate searches

      matched_substrings
        Returns the placement and offset of the matched strings for this search.
        A an array of dicts, each with the keys 'length' and 'offset', will be returned.

      place_id
        Returns the unique stable identifier denoting this place.
        This identifier may be used to retrieve information about this
        place.
        This should be considered the primary identifier of a place.

      reference
        Returns a unique identifier for the Place that can be used to fetch full
        details about it. It is recommended that stored references for Places be
        regularly updated. A Place may have many valid reference tokens.

      terms
        A list of terms which build up the description string
        A an array of dicts, each with the keys `offset` and `value`, will be returned.

      types
        Returns a List of feature types describing the given result.

      place
        Returns a Dict representing the full response from the details API request.
        This property will raise a googleplaces.GooglePlacesAttributeError if it is
        referenced prior to get_details()

      get_details(**kwargs)
        Retrieves full information on the place matching the reference.
          kwargs:
            language   -- The language code, indicating in which language the
                          results should be returned, if possible. This value defaults
                          to the language that was used to generate the
                          GooglePlacesSearchResult instance.


    googleplaces.Place
      reference
        (DEPRECATED) Returns a unique identifier for the Place that can be used to
        fetch full details about it. It is recommended that stored references for
        Places be regularly updated. A Place may have many valid reference tokens.

      id
        (DEPECATED) Returns a unique stable identifier denoting this Place. This
        identifier may not be used to retrieve information about this Place, but
        can be used to consolidate data about this Place, and to verify the identity
        of a Place across separate searches.

      place_id
        A textual identifier that uniquely identifies a place. To retrieve information
        about the place, pass this identifier in the placeId field of a Places API
        request.

      icon
        contains the URL of a suggested icon which may be displayed to the user when
        indicating this result on a map.

      types
        Returns a List of feature types describing the given result.

      geo_location
        Returns the geocoded latitude,longitude value for this Place.

      name
        Returns the human-readable name for the Place.

      vicinity
        Returns a feature name of a nearby location. Often this feature refers to a
        street or neighborhood.

      rating
        Returns the Place's rating, from 0.0 to 5.0, based on user reviews.

      details
        Returns a Dict representing the full response from the details API request.
        This property will raise a googleplaces.GooglePlacesAttributeError if it is
        referenced prior to get_details()

      photos
        returns a list of available googleplaces.Photo objects.

      formatted_address
        Returns a string containing the human-readable address of this place. Often
        this address is equivalent to the "postal address".
        This property will raise a googleplaces.GooglePlacesAttributeError if it is
        referenced prior to get_details()

      local_phone_number
        Returns the Place's phone number in its local format.
        This property will raise a googleplaces.GooglePlacesAttributeError if it is
        referenced prior to get_details()

      international_phone_number
        Returns the Place's phone number in international format. International
        format includes the country code, and is prefixed with the plus (+) sign.
        This property will raise a googleplaces.GooglePlacesAttributeError if it is
        referenced prior to get_details()

      website
        Returns the authoritative website for this Place, such as a business'
        homepage.

      url
        Returns the official Google Place Page URL of this Place.

      has_attributions
        Returns a flag indicating if the search result has html attributions that
        must be displayed. along side the detailed query result.

      html_attributions
        Returns a List of String html attributions that must be displayed along with
        the detailed query result.

      checkin()
        Checks in an anonynomous user in.

      get_details(**kwargs)
        Retrieves full information on the place matching the place_id.
          kwargs:
            language   -- The language code, indicating in which language the
                          results should be returned, if possible. This value defaults
                          to the language that was used to generate the
                          GooglePlacesSearchResult instance.

    googleplaces.Photo
      orig_height
        the maximum height of the origin image.

      orig_width
        the maximum height of the origin image.

      html_attributions
         Contains any required attributions. This field will always be present,
         but may be empty.

      photo_reference
         A string used to identify the photo when you perform a Photo request
         via the get method.

      get
        Fetches the actual photo data from the Google places API.

      mimetype
        Specifies the mimetype if the fetched image. This property is only
        available after the get API has been invoked.

      filename
        Specifies the filename of the fetched image. This property is only
        available after the get API has been invoked.

      data
        The binary data of the image. This property is only available after the
        get API has been invoked.

      url
        The url of the image. This property is only available after the get API
        has been invoked.
