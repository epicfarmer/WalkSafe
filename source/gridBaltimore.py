import fiona
import shapely as sp
import shapely.geometry as sg
import matplotlib.pyplot as plt
import numpy as np

#This method returns a MultiPoint object (see shapely.geometry.Multipoint) containing the points in an appropriate grid with x_bins rows and y_bins columns. 
def getBaltimoreGrid(x_bins,y_bins):
	#This method beings with importing somethign called a shape file, which keeps track of the shape of baltimore.  Didn't want to learn fiona, so getting away from it as quickly as possible
	unknown_object = fiona.open("data/baltimore_city_polygon.shp")
	poly_shape = unknown_object.next()
	#We eventually want a polygon, but unfortunately the units aren't latitude and longitude.  Instead of messing around with the previous stuff, I just converted to numpy and back
	shapely_shape = sg.shape(poly_shape['geometry'])
	shapely_shape.x,shapely_shape.y=shapely_shape.exterior.xy
	array_shape = np.array(shape.exterior.xy)
	#Using the known latitude and longitude bounds, we convert the polygon
	array_shape = (array_shape- np.min(array_shape,1).reshape([array_shape.shape[0],1]))/(np.max(array_shape,1).reshape([array_shape.shape[0],1])- np.min(array_shape,1).reshape([array_shape.shape[0],1])) * np.array([[(-76.53144000000016+76.711439999999996) ],[(39.370410000000085 - 39.200409999999998) ]]) + np.array([[-76.711439999999996],[39.200409999999998]])
	#convert back to shapely shape
	final_shapely_shape = sg.Polygon(array_shape.T)
	final_shapely_shape.x,final_shapely_shape.y=final_shapely_shape.exterior.xy
	
	#Now we construct the grid.
	x_step = (np.max(shape.x)-np.min(shape.x))/x_bins
	y_step = (np.max(shape.x)-np.min(shape.x))/y_bins
	x_range = np.arange(np.min(shape.x),np.max(shape.x),x_step)
	y_range = np.arange(np.min(shape.y),np.max(shape.y),y_step)
	#meshgrid is a powerhorse method.  It basically takes the list of x's and the list of y's and makes the list of (x,y) pairs.
	X,Y = np.meshgrid(x_range,y_range)

	#convert them to shapely stuff to do the intersection, and then return
	rectanglearray = np.reshape(np.array([X,Y]),[2,np.prod(X.shape)]).T
	rectanglepointsarray = sg.MultiPoint(rectanglearray)
	output = rectanglepointsarray.intersection(shape)
	return(output)
