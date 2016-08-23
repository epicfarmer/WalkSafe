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
#reweight_linelist(dr.directions

	

twopoint = "{cynFjanrMoADoCJqCBoBFsFNaA@{CDsDHE?C?K@eBD"
#twopoint = dr.directions('615 N Wolfe Street,Baltimore, MD','Fells Point, Baltimore, MD')[0]['overview_polyline']['points']
line = pl.decode(twopoint)
try:
	raster_data = np.load("data/RasterCrimeData.npy")
	xinfo = np.load("data/xinfoCrimeData.npy")
	yinfo = np.load("data/yinfoCrimeData.npy")
except IOError as (errno,strerror):
	data = pd.read_csv("data/BPD_Part_1_Victim_Based_Crime_Data.csv")
	latlong_data = data.loc[:,"Location 1"].str.split(',')
	latlong_data = pd.DataFrame(np.matrix([latlong_data.str[0].str.replace("(",""),latlong_data.str[1].str.replace(")","")]).T,dtype=float)
	latlong_data.columns = ["y","x"]
	latlong_data = latlong_data[latlong_data["y"] < 40]
	year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')
	[raster_data,xinfo,yinfo] = ls.rasterizeData(latlong_data,.005)
	np.save("data/RasterCrimeData.npy",raster_data,False)
	np.save("data/xinfoCrimeData.npy",xinfo,False)
	np.save("data/yinfoCrimeData.npy",yinfo,False)

new_weight = reweight_linelist(line,raster_data,xinfo,yinfo)
test = sg.LineString(line)
test.y,test.x = test.xy
print(sg.LineString(line).length)
print(new_weight)
ls.plotRasterData(xinfo,yinfo,raster_data)
plt.plot(test.x,test.y)
#plt.show()
test = np.array([xinfo,yinfo])
points = test.reshape(2,35*37).T
