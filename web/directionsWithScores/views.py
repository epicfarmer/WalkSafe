from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseBadRequest
import googlemaps

import sys
import os.path
HOME=os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(os.path.join(HOME, "source"))

from loadData import loadData, loadRasterData
import polyline
from reweightLinelist import reweight_linelist

import pprint

DISTANCE_MATRIX_URL ='https://maps.googleapis.com/maps/api/distancematrix/json'
DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'

ORIGIN='615 N Wolfe Street, Baltimore, MD'
DESTINATION = '501 E Pratt Street, Baltimore, MD'

THE_KEY_FILE = "/Users/Kathryn/Desktop/GoogleMapKey"
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


def _directions(origin, destination):
    API_KEY = _api_key()
    gmaps = googlemaps.Client(key=API_KEY)
    # Request directions via public transit
    return gmaps.directions(origin,
                                     destination,
                                     mode="walking")

def map(request):

    html = "<iframe width=\"600\" height=\"450\" frameborder=\"0\" style=\"border:0\""
    html += "src=\"https://www.google.com/maps/embed/v1/directions?origin=%s&destination=%s&key=%s\"" \
            "allowfullscreen>" \
            "</iframe> " % (ORIGIN, DESTINATION, BROWSER_KEY)
    return HttpResponse(html)

def index(request):

    params = {}
    if request.method == 'POST':
        params = request.POST
    elif request.method == 'GET':
        params = request.GET
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    if 'origin' not in params.keys() or 'destination' not in params.keys():
        return HttpResponseBadRequest('<h1>Bad Request</h1>origin and destination parameters required')


    directions_result = _directions(params['origin'],params['destination'])
    points = directions_result[0]['overview_polyline']['points']

    line = polyline.decode(points)

    [crime, xinfo, yinfo] = loadRasterData()

    safety_score = reweight_linelist(line, crime, xinfo, yinfo)

    response = {}
    response['directions'] = directions_result
    response['safety_score'] = safety_score

    return JsonResponse(response)
