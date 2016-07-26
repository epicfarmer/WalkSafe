from django.shortcuts import render

from django.http import HttpResponse
import googlemaps
import pprint

DISTANCE_MATRIX_URL ='https://maps.googleapis.com/maps/api/distancematrix/json'
DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'

ORIGIN='615 N Wolfe Street, Baltimore, MD'
DESTINATION = '501 E Pratt Street, Baltimore, MD'

THE_KEY_FILE = ""
BROWSER_KEY = ""

def _api_key():
    with open(THE_KEY_FILE, 'r') as fh:
        return fh.read().strip()

def _request_directions():
    API_KEY = _api_key()
    gmaps = googlemaps.Client(key=API_KEY)

    geocode_result = gmaps.distance_matrix(['615 N Wolfe Street, Baltimore, MD'],
                                           ['501 E Pratt Street, Baltimore, MD', '333 W Camden St, Baltimore, MD'],
                                           mode="walking")

    return geocode_result

def directions(origin, destination):
    API_KEY = _api_key()
    gmaps = googlemaps.Client(key=API_KEY)
    # Request directions via public transit
    directions_result = gmaps.directions(origin,
                                     destination,
                                     mode="walking")

def index(request):
    html = "<iframe width=\"600\" height=\"450\" frameborder=\"0\" style=\"border:0\""
    html += "src=\"https://www.google.com/maps/embed/v1/directions?origin=%s&destination=%s&key=%s\"" \
            "allowfullscreen>" \
            "</iframe> " % (ORIGIN, DESTINATION, BROWSER_KEY)
    return HttpResponse(html)