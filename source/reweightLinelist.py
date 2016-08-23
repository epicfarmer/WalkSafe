import numpy as np
import shapely.geometry as sg
import matplotlib.pyplot as plt
import polyline as pl
import LevelSetEstimation as ls
import pandas as pd
import directions as dr


def reweight_linelist(linelist,raster,xinfo,yinfo):
	#Consider adding processing for the cases where linelist is a string, list of coordinates, or a geometry object
	path = sg.LineString(linelist)
	ans = 0
	for row in np.arange(0,raster.shape[0]-1):
		for col in np.arange(0,raster.shape[1]-1):
			square = sg.Polygon([(yinfo[row,col],xinfo[row,col]),(yinfo[row+1,col],xinfo[row+1,col]),(yinfo[row+1,col+1],xinfo[row+1,col+1]),(yinfo[row,col+1],xinfo[row,col+1])])
			length = smartIntersectLength(path,square)
			if(length > 0):
				ans = ans + (raster[row,col])*length
	return(ans)

def smartIntersectLength(linelist,cell):
	if(not(linelist.intersects(cell))):
		return 0
	return(linelist.intersection(cell).length)

def compute_closest_points(distance_matrix,locations):
	#This works because we assume a regularish grid
	threshold = np.min(distance_matrix[distance_matrix > 0])*1.9
	closest_pairs = distance_matrix < threshold;
	closest_pairs[np.tril_indices(closest_pairs.shape[0])] = False
	closest_pairs = np.array(np.where(closest_pairs)).T
	return(closest_pairs)

def reweight_distance_matrix(distance_matrix,locations,raster,xinfo,yinfo):
	numpoints = distance_matrix.shape[0]
	threshold = 1
	closest_point_pairs = compute_closest_points(distance_matrix,locations)

	test = np.zeros(distance_matrix.shape);
	test[:] = np.Inf;
	for point_pair in closest_point_pairs:
		tmp = reweight_linelist(sg.LineString(np.array([locations[point_pair[0],],locations[point_pair[1],]])),raster_data,xinfo,yinfo)
		test[point_pair[0],point_pair[1]] = tmp
		test[point_pair[1],point_pair[0]] = tmp
	print(test)
	#Use igraph to make test into a graph, and then compute the shortest paths
	#http://igraph.org/python/doc/igraph.Graph-class.html
	return(distance_matrix,locations)
