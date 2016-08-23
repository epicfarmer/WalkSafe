import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import LevelSetEstimation as ls
import directions as dr
import gridBaltimore as gb
import shapely.geometry as sg

def loadData():
	data = pd.read_csv("data/BPD_Part_1_Victim_Based_Crime_Data.csv")
	latlong_data = data.loc[:,"Location 1"].str.split(',')
	latlong_data = pd.DataFrame(np.matrix([latlong_data.str[0].str.replace("(",""),latlong_data.str[1].str.replace(")","")]).T,dtype=float)
	latlong_data.columns = ["y","x"]
	latlong_data = latlong_data[latlong_data["y"] < 40]
	year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')
	return latlong_data

def loadRasterData():
	try:
		raster_data = np.load("data/RasterCrimeData.npy")
		xinfo = np.load("data/xinfoCrimeData.npy")
		yinfo = np.load("data/yinfoCrimeData.npy")
	except IOError as (errno,strerror):
		loadData()
		[raster_data,xinfo,yinfo] = ls.rasterizeData(latlong_data,.005)
		np.save("data/RasterCrimeData.npy",raster_data,False)
		np.save("data/xinfoCrimeData.npy",xinfo,False)
		np.save("data/yinfoCrimeData.npy",yinfo,False)
	return([raster_data,xinfo,yinfo])

def loadDistanceData():
	try:
		distances = np.load("data/distance_matrix.npy")
		locations = np.load("data/baltimore_grid.npy")
	except IOError as (errno,strerror):
		baltimore_grid = gb.getBaltimoreGrid(5,5)
		baltimore_grid.long,baltimore_grid.lat = sg.asLineString(baltimore_grid).xy
		locations = np.array([baltimore_grid.lat,baltimore_grid.long]).T
		distances = dr.distance_matrix(locations)
		distances = np.save("data/distance_matrix.npy",distances,False)
		locations = np.save("data/baltimore_grid.npy",locations,False)
	return(distances,locations)
