import pprint
import googlemaps

DISTANCE_MATRIX_URL ='https://maps.googleapis.com/maps/api/distancematrix/json'
DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'

def api_key():
    with open(THE_KEY_FILE, 'r') as fh:
        return fh.read().strip()

API_KEY = api_key()


gmaps = googlemaps.Client(key=API_KEY)

geocode_result = gmaps.distance_matrix(['615 N Wolfe Street, Baltimore, MD'],
                                       ['501 E Pratt Street, Baltimore, MD', '333 W Camden St, Baltimore, MD'],
                                       mode="walking")

pprint.pprint(geocode_result)

def directions(origin, destination):
    # Request directions via public transit
    directions_result = gmaps.directions(origin,
                                     destination,
                                     mode="walking")



