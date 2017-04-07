import pprint
import googlemaps
import os.path


# Get key to use googlemaps from file
def _init_api_key():
	key_file = os.path.join(os.path.dirname(__file__), "../data/google_key")
	with open(key_file, 'r') as fh:
		return fh.read().strip()

API_KEY = _init_api_key()
GMAPS_CLIENT = googlemaps.Client(key=API_KEY)


# Get directions from one location to another location
# input:
#	origin	(string)	name of place to travel from
#	destination	(string)	name of place to travel to
# output:
#		(list:dict:various) the directions from google.
# 			For our purposes, output[0]['overview_polyline']['points'] is a list of tuples of latlong coordinates
def directions(origin, destination):
	# Request walking directions via public transit
	return GMAPS_CLIENT.directions(origin, destination, mode="walking")


# Get distance 'matrix' between a set of locations
# input:
#	locations	(list:string)	names of locations to get distances among
# output:
#	a numpy array where (i,j)th entry is the distance from locations[i] to locations[j]
def distance_matrix(src_locations, dst_locations):
	return GMAPS_CLIENT.distance_matrix(src_locations, dst_locations, mode="walking")
