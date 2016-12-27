import fiona
import shapely.geometry as sg
import numpy as np

import os.path

from directionsWithScores.models import Coordinates


# returns a Polygon (see shapely.geometry.Polygon) of Baltimore
def baltimore_grid():
	# fiona_obj = fiona.open("data/Baltimore City Line/geo_export_3fc95e5f-74e6-4614-ab5d-bb96b8ed773d.shp")
	fiona_obj = fiona.open("../data/Baltimore City Line/Baltimore City Line.geojson")
	poly_shape = fiona_obj.next()

	# We eventually want a polygon, but unfortunately the units aren't latitude and longitude.
	# Instead of messing around with the previous stuff, just convert to numpy and back
	multiline_shape = sg.shape(poly_shape['geometry'])

	return sg.Polygon(multiline_shape[0])

# shapely.geometry.Polygon of Baltimore
_BALTIMORE_GRID = baltimore_grid()

LON_MIN = np.min(_BALTIMORE_GRID.exterior.xy[0])
LON_MAX = np.max(_BALTIMORE_GRID.exterior.xy[0])
LAT_MIN = np.min(_BALTIMORE_GRID.exterior.xy[1])
LAT_MAX = np.max(_BALTIMORE_GRID.exterior.xy[1])

# assumes lat, lon coordinate
def within(point):
	if isinstance(point, Coordinates):
		p = [point.lat, point.lon]
		point = p
	print(point)

	assert(len(point) == 2)
	point = [point[1], point[0]]
	if not hasattr(point, '_geom'):
		point = sg.Point(point)
	return _BALTIMORE_GRID.contains(point)

# returns a MultiPoint object (see shapely.geometry.Multipoint) containing the points in an appropriate grid with x_bins rows and y_bins columns.
# input is baltimore_grid() output
def bins(num_bins):
	x, y = _BALTIMORE_GRID.exterior.xy

	# Now we construct the grid.
	xmin = np.min(x)
	xmax = np.max(x)
	ymin = np.min(y)
	ymax = np.max(y)
	xstep = (xmax - xmin) / num_bins
	ystep = (ymax - ymin) / num_bins
	xrange = np.arange(xmin, xmax, xstep)
	yrange = np.arange(ymin, ymax, ystep)

	# convert them to shapely stuff to do the intersection, and then return
	# Cartesian product of sets
	# meshgrid takes the list of x's and the list of y's and makes the list of (x,y) pairs.

	coords = np.array(np.meshgrid(xrange, yrange)).T.reshape(-1, 2)

	# rectanglepointsarray = sg.MultiPoint(coords)
	# output = rectanglepointsarray.intersection(BALTIMORE_GRID)

	return coords
