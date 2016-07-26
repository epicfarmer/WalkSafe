import pprint
import googlemaps
import numpy as np

#Get key to use googlemaps from file
def api_key():
	with open('KEYFILE', 'r') as fh:
		return fh.read().strip()

API_KEY = api_key()
gmaps = googlemaps.Client(key=API_KEY)

#Get directions from one location to another location
#input:
	#JK: list of strings? unknown
#	origin	(string)	name of place to travel from
#	destination	(string)	name of place to travel to
#output:
#		(list:dict:various) the directions from google.  For our purposes, output[0]['overview_polyline']['points'] is a list of tuples of latlong coordinates
def directions(origin, destination):
	# Request directions via public transit
	directions_result = gmaps.directions(origin,destination,mode="walking")
	return(directions_result)

#Get distance 'matrix' between a set of locations
#input:
#	locations	(list:string)	names of locations to get distances among
#output:
#	a numpy array
def distance_matrix(locations):
	geocode_result = gmaps.distance_matrix(locations,locations,mode="walking")
	output=np.zeros([len(locations),len(locations)],np.float32)
	for i in range(len(locations)):
		for j in range(len(locations)):
			output[i,j] = geocode_result['rows'][i]['elements'][j]['distance']['value']
	return(output)
	
DISTANCE_MATRIX_URL ='https://maps.googleapis.com/maps/api/distancematrix/json'
DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'

locations = [
	'615 N Wolfe Street, Baltimore, MD',
	'501 E Pratt Street, Baltimore, MD',
	'333 W Camden St, Baltimore, MD',
	'1876 Mansion House Drive Druid Hill Park,, 1876 Mansion House Dr, Baltimore, MD 21217'
]

i=0
j=1
print(len(locations))
print(distance_matrix(locations))
#print(distance_matrix(locations)['rows'][i]['elements'][j]['distance']['value'])
