import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import LevelSetEstimation as ls
import directions as dr
import gridBaltimore as gb
import shapely.geometry as sg
import os.path
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def loadData():
	data = pd.read_csv(os.path.join(DATA_DIR, "/BPD_Part_1_Victim_Based_Crime_Data.csv"))
	latlong_data = data.loc[:,"Location 1"].str.split(',')
	latlong_data = pd.DataFrame(np.matrix([latlong_data.str[0].str.replace("(",""),latlong_data.str[1].str.replace(")","")]).T,dtype=float)
	latlong_data.columns = ["y","x"]
	latlong_data = latlong_data[latlong_data["y"] < 40]
	year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')
	return latlong_data

def loadRasterData():
	try:
		raster_data = np.load(os.path.join(DATA_DIR, "RasterCrimeData.npy"))
		xinfo = np.load(os.path.join(DATA_DIR, "xinfoCrimeData.npy"))
		yinfo = np.load(os.path.join(DATA_DIR, "yinfoCrimeData.npy"))
	except IOError as (errno,strerror):
		[raster_data,xinfo,yinfo] = ls.rasterizeData(loadData(),.005)
		np.save(os.path.join(DATA_DIR, "RasterCrimeData.npy"),raster_data,False)
		np.save(os.path.join(DATA_DIR, "xinfoCrimeData.npy"),xinfo,False)
		np.save(os.path.join(DATA_DIR, "yinfoCrimeData.npy"),yinfo,False)
	return([raster_data,xinfo,yinfo])

def loadDistanceData():
	try:
		distances = np.load(os.path.join(DATA_DIR, "distance_matrix.npy"))
		locations = np.load(os.path.join(DATA_DIR, "baltimore_grid.npy"))
	except IOError as (errno,strerror):
		baltimore_grid = gb.getBaltimoreGrid(5,5)
		baltimore_grid.long,baltimore_grid.lat = sg.asLineString(baltimore_grid).xy
		locations = np.array([baltimore_grid.lat,baltimore_grid.long]).T
		distances = dr.distance_matrix(locations)
		distances = np.save(os.path.join(DATA_DIR, "distance_matrix.npy"),distances,False)
		locations = np.save(os.path.join(DATA_DIR, "baltimore_grid.npy"),locations,False)
	return(distances,locations)
