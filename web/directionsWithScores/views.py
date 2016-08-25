from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings

import os.path
import sys
sys.path.append(settings.SOURCE_DIR)

from loadData import loadRasterData
import polyline
from reweightLinelist import reweight_linelist
import directions


GOOGLE_KEY_FILE = os.path.join(settings.DATA_DIR, "google_key")
BROWSER_KEY = ""


# currently not used. Need to initialize Browser Key oabove
def _map(origin, destination):
	html = "<iframe width=\"600\" height=\"450\" frameborder=\"0\" style=\"border:0\""
	html += "src=\"https://www.google.com/maps/embed/v1/directions?"
	html += "origin=" + origin
	html += "&destination=" + destination
	html += "&key=" + BROWSER_KEY
	html += "\" allowfullscreen>"
	html += "</iframe> "
	return HttpResponse(html)


def directions_with_scores(request):

	if request.method == 'POST':
		params = request.POST
	elif request.method == 'GET':
		params = request.GET
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

	# check parameters
	if 'origin' not in params.keys() or 'destination' not in params.keys():
		return HttpResponseBadRequest('<h1>Bad Request</h1>origin and destination parameters required')

	# get directions
	directions_result = directions.directions(params['origin'], params['destination'])
	points = directions_result[0]['overview_polyline']['points']

	# calculate the safety_score
	line = polyline.decode(points)
	[crime, xinfo, yinfo] = loadRasterData()
	safety_score = reweight_linelist(line, crime, xinfo, yinfo)

	# form JSON response
	response = {'directions': directions_result, 'safety_score': safety_score}

	return JsonResponse(response)
