import fiona
import shapely as sp
import shapely.geometry as sg
import matplotlib.pyplot as plt
import numpy as np

def getBaltimoreGrid(x_bins,y_bins):
	c = fiona.open("data/baltimore_city_polygon.shp")
	pol = c.next()
	shape = sg.shape(pol['geometry'])
	shape.x,shape.y=shape.exterior.xy
	polygonarray = np.array(shape.exterior.xy)
	polygonarray = (polygonarray - np.min(polygonarray,1).reshape([polygonarray.shape[0],1]))/(np.max(polygonarray,1).reshape([polygonarray.shape[0],1])- np.min(polygonarray,1).reshape([polygonarray.shape[0],1])) * np.array([[(-76.53144000000016+76.711439999999996) ],[(39.370410000000085 - 39.200409999999998) ]]) + np.array([[-76.711439999999996],[39.200409999999998]])
	shape = sg.Polygon(polygonarray.T)
	shape.x,shape.y=shape.exterior.xy
	
	x_step = (np.max(shape.x)-np.min(shape.x))/x_bins
	y_step = (np.max(shape.x)-np.min(shape.x))/y_bins
	x_range = np.arange(np.min(shape.x),np.max(shape.x),x_step)
	y_range = np.arange(np.min(shape.y),np.max(shape.y),y_step)
	
	X,Y = np.meshgrid(x_range,y_range)
	rectanglearray = np.reshape(np.array([X,Y]),[2,np.prod(X.shape)]).T
	rectanglepointsarray = sg.MultiPoint(rectanglearray)
	output = rectanglepointsarray.intersection(shape)
	return(output)
