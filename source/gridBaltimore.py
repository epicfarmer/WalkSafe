import fiona
import shapely as sp
import shapely.geometry as sg
import matplotlib.pyplot as plt
import numpy as np

# returns a Polygon (see shapely.geometry.Polygon) of Baltimore
def baltimore_grid():
	#This method beings with importing a shape file, which keeps track of the shape of baltimore.
	# Didn't want to learn fiona, so getting away from it as quickly as possible
	# fiona_obj = fiona.open("data/Baltimore City Line/geo_export_3fc95e5f-74e6-4614-ab5d-bb96b8ed773d.shp")
	fiona_obj = fiona.open("data/Baltimore City Line/Baltimore City Line.geojson")
	poly_shape = fiona_obj.next()

	# We eventually want a polygon, but unfortunately the units aren't latitude and longitude.
	# Instead of messing around with the previous stuff, just convert to numpy and back
	multiline_shape = sg.shape(poly_shape['geometry'])

	return sg.Polygon(multiline_shape[0])

BALTIMORE_GRID = baltimore_grid()

def within(point):
	return BALTIMORE_GRID.contains(point)

# returns a MultiPoint object (see shapely.geometry.Multipoint) containing the points in an appropriate grid with x_bins rows and y_bins columns.
# input is baltimore_grid() output
def bins(num_bins):
	x, y = BALTIMORE_GRID.exterior.xy

	'''
	# Using the known latitude and longitude bounds, we convert the polygon
	array_shape = np.array(BALTIMORE_GRID.exterior.xy)
	array_shape = (array_shape - np.min(array_shape,1).reshape([array_shape.shape[0],1])) /\
				  (np.max(array_shape,1).reshape([array_shape.shape[0],1])- np.min(array_shape,1).reshape([array_shape.shape[0],1])) \
				  * np.array([[(-76.53144000000016+76.711439999999996) ],[(39.370410000000085 - 39.200409999999998) ]]) + \
				  np.array([[-76.711439999999996],[39.200409999999998]])

	# Convert back to shapely shape
	final_shapely_shape = sg.Polygon(array_shape.T)
	final_shapely_shape.x, final_shapely_shape.y = final_shapely_shape.exterior.xy
	'''

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
