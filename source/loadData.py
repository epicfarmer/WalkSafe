import pandas as pd
import numpy as np
import LevelSetEstimation as ls
import directions as dr
import gridBaltimore as gb
import shapely.geometry as sg
import os.path

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

# FORMAT OF CRIME DATA
#CrimeDate,CrimeTime,CrimeCode,Location,Description,Weapon,Post,District,Neighborhood,Location 1,Total Incidents
#05/28/2016,00:00:00,6E,2700 HARLEM AVE,LARCENY,,721,WESTERN,Mosher,"(39.2955200000, -76.6624700000)",1


# loads the file data/BPD_Part_1_Victim_Based_Crime_Data.csv
def loadBPD_Crime_Data():
	data_loc = os.path.join(DATA_DIR, "BPD_Part_1_Victim_Based_Crime_Data.csv")
	return pd.read_csv(data_loc)


# partially parses the file data/BPD_Part_1_Victim_Based_Crime_Data.csv
# only loads the latitudes and longitudes for each crime
def loadData():
	data = loadBPD_Crime_Data()
	latlong_data = data.loc[:, "Location 1"].str.split(',')
	latlong_data = pd.DataFrame(np.matrix([latlong_data.str[0].str.replace("(", ""),
										   latlong_data.str[1].str.replace(")", "")]).T,
								dtype=float)
	latlong_data.columns = ["y", "x"]
	latlong_data = latlong_data[latlong_data["y"] < 40]
	#year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')
	return latlong_data


# loads the rasterized crime data or rasterizes at the given scale
# If the data is rasterized at a scale of .005 degrees,
# then the histogram bins are .005 latitude by .005 longitude.
def loadRasterData(scale = .005):
	# Load if possible. Otherwise, calculate
	try:
		raster_data = np.load(os.path.join(DATA_DIR, "RasterCrimeData.npy"))
		xinfo = np.load(os.path.join(DATA_DIR, "xinfoCrimeData.npy"))
		yinfo = np.load(os.path.join(DATA_DIR, "yinfoCrimeData.npy"))
	except IOError:
		print("creating new raster data at scale: %i" % scale)
		# We get the crime data, the longitudes and the latitudes
		[raster_data, xinfo, yinfo] = ls.rasterizeData(loadData(), scale)
		# Save so next time we won't have to calculate
		np.save(os.path.join(DATA_DIR, "RasterCrimeData.npy"), raster_data, False)
		np.save(os.path.join(DATA_DIR, "xinfoCrimeData.npy"), xinfo, False)
		np.save(os.path.join(DATA_DIR, "yinfoCrimeData.npy"), yinfo, False)
	# WARNING: xinfo is the longitudes, and yinfo is the latitudes
	return [raster_data, xinfo, yinfo]

# loads the distance matrix.
def loadDistanceData():
	# Load if possible, but calculate if not possible
	try:
		distances = np.load(os.path.join(DATA_DIR, "distance_matrix.npy"))
		locations = np.load(os.path.join(DATA_DIR, "baltimore_grid.npy"))
	except IOError:
		# TODO: Replace this with a call to refine_baltimore_distance_matrix
		baltimore_grid = gb.getBaltimoreGrid(5, 5)
		baltimore_grid.long, baltimore_grid.lat = sg.asLineString(baltimore_grid).xy
		locations = np.array([baltimore_grid.lat, baltimore_grid.long]).T
		distances = dr.distance_matrix(locations)
		distances = np.save(os.path.join(DATA_DIR, "distance_matrix.npy"), distances, False)
		locations = np.save(os.path.join(DATA_DIR, "baltimore_grid.npy"), locations, False)
	return distances, locations
