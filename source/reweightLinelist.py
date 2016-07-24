import numpy as np
import shapely.geometry as sg
import matplotlib.pyplot as plt
import polyline as pl
import LevelSetEstimation as ls
import pandas as pd
import directions


def reweight_linelist(linelist,raster,xinfo,yinfo):
	#Consider adding processing for the cases where linelist is a string, list of coordinates, or a geometry object
	path = sg.LineString(linelist)
	ans = 0
	for row in np.arange(0,raster.shape[0]-1):
		for col in np.arange(0,raster.shape[1]-1):
			square = sg.Polygon([(yinfo[row,col],xinfo[row,col]),(yinfo[row+1,col],xinfo[row+1,col]),(yinfo[row+1,col+1],xinfo[row+1,col+1]),(yinfo[row,col+1],xinfo[row,col+1])])
			length = smartIntersectLength(path,square)
			if(length > 0):
				ans = ans + raster[row,col]*length
	return(ans)

def smartIntersectLength(linelist,cell):
	if(not(linelist.intersects(cell))):
		return 0
	return(linelist.intersection(cell).length)

twopoint = "{cynFjanrMoADoCJqCBoBFsFNaA@{CDsDHE?C?K@eBD"
twopoint = directions.directions('615 N Wolfe Street,Baltimore, MD','333 W Camden St, Baltimore, MD')[0]['overview_polyline']['points']
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
	print(xinfo)
	np.save("data/RasterCrimeData.npy",raster_data,False)
	np.save("data/xinfoCrimeData.npy",xinfo,False)
	np.save("data/yinfoCrimeData.npy",yinfo,False)

new_weight = reweight_linelist(line,raster_data,xinfo,yinfo)
print(sg.LineString(line).length)
print(new_weight)
