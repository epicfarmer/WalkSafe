import pprint
import googlemaps
import numpy as np
import time
import gridBaltimore as gb
import shapely.geometry as sg

import os.path

#Get key to use googlemaps from file
def _init_api_key():
    key_file = os.path.join(os.path.dirname(__file__), "../data/google_key")
    print key_file
    with open(key_file, 'r') as fh:
        return fh.read().strip()

API_KEY = _init_api_key()
GMAPS_CLIENT = googlemaps.Client(key=API_KEY)

#Get directions from one location to another location
#input:
	#JK: list of strings? unknown
#	origin	(string)	name of place to travel from
#	destination	(string)	name of place to travel to
#output:
#		(list:dict:various) the directions from google.  For our purposes, output[0]['overview_polyline']['points'] is a list of tuples of latlong coordinates
def directions(origin, destination):
    # Request walking directions via public transit
	directions_result = GMAPS_CLIENT.directions(origin,destination,mode="walking")
	return(directions_result)

#Get distance 'matrix' between a set of locations
#input:
#	locations	(list:string)	names of locations to get distances among
#output:
#	a numpy array
def distance_matrix(locations):
	output=np.zeros([len(locations),len(locations)],np.float32)*np.nan
	from_matrix = np.zeros([5,2])
	to_matrix = np.zeros([5,2])
	for i in np.arange(0,len(locations),5):
		from_matrix = locations[i:i+5,:]
		for j in np.arange(0,len(locations),5):
			to_matrix = locations[j:j+5,:]
			#print("Here")
			#print(from_matrix.shape[0])
			#print(to_matrix.shape[0])
			try:
				geocode_result = GMAPS_CLIENT.distance_matrix(from_matrix,to_matrix,mode="walking")
			except googlemaps.exceptions.Timeout:
				return(output)
			print(i,j)
			time.sleep(1)
			#print(output)
			for k in np.arange(from_matrix.shape[0]):
				for l in np.arange(to_matrix.shape[0]):
					if(geocode_result['rows'][k]['elements'][l]['status'] == 'OK'):
						output[i+k,j+l] = geocode_result['rows'][k]['elements'][l]['distance']['value']
					else:
						print(geocode_result['rows'][i+k]['elements'][j+l])
						output[i+k,j+l] = np.nan
	return(output)

#Get distance 'matrix' between a set of locations
#input:
#	locations	(list:string)	names of locations to get distances among
#output:
#	a numpy array
def assymetric_distance_matrix(to_locations,from_locations):
	geocode_result = GMAPS_CLIENT.distance_matrix(from_locations,to_locations,mode="walking")
	#except googlemaps.exceptions.Timeout:
	output=np.zeros([len(from_locations),len(to_locations)],np.float32)
	for i in range(len(from_locations)):
		for j in range(len(to_locations)):
			if(geocode_result['rows'][i]['elements'][j]['status'] == 'OK'):
				output[i,j] = geocode_result['rows'][i]['elements'][j]['distance']['value']
			else:
				print(geocode_result['rows'][i]['elements'][j])
				output[i,j] = np.nan
	return(output)

def baltimore_distance_matrix(xbins,ybins):
	baltimore_grid = gb.getBaltimoreGrid(xbins,ybins)
	baltimore_grid.long,baltimore_grid.lat = sg.asLineString(baltimore_grid).xy
	test1 = np.array([baltimore_grid.lat,baltimore_grid.long]).T
	test2 = distance_matrix(test1)
	np.save('data/distance_matrix',test2)
	np.save('data/baltimore_grid',test1)
	return([test2,test1])

def refining_baltimore_distance_matrix():
	try:
		baltimore_grid = np.load('data/baltimore_grid.npy',test1)
		old_matrix = np.load('data/temp_distance_matrix.npy')
	except:
		[old_matrix,baltimore_grid] = baltimore_distance_matrix(3,3)
	latitudes,longitudes = sg.asLineString(baltimore_grid).xy
	locations = np.array([latitudes,longitudes]).T
	output = old_matrix
	if(np.prod(np.shape(np.where(np.isnan(old_matrix)))) == 0):
		new_xbins = (np.shape(np.unique(locations[:,0]))[0]+1)*2
		new_ybins = (np.shape(np.unique(locations[:,1]))[0]+1)*2
		new_baltimore_grid = gb.getBaltimoreGrid(new_xbins,new_ybins)
		new_baltimore_grid.long,new_baltimore_grid.lat = sg.asLineString(new_baltimore_grid).xy
		new_locations = np.array([new_baltimore_grid.lat,new_baltimore_grid.long]).T
		
		a = np.tile(locations,[new_locations.shape[0],new_locations.shape[1],1,1])
		
		print(a.shape,locations.shape,new_locations.shape)
		#b = np.tile(new_locations,[1,1,locations.shape[0],locations.shape[1]])
		#output = np.zeros([new_locations.shape[0],new_locations.shape[0]],np.float32)*np.nan
		#a,b = np.meshgrid(locations,new_locations)
		#print( a.shape,b.shape )
		#print(locations.shape,new_locations.shape)
		#print(a.shape)
		quit()
		for row in np.arange(locations.shape[0]):
			new_row = np.where(np.sum(np.abs(locations[row,:] - new_locations),1) == 0)
			for col in np.arange(locations.shape[0]):
				new_col = np.where(np.sum(np.abs(locations[col,:] - new_locations),1) == 0)
				output[new_row,new_col] = old_matrix[row,col]
				print(new_locations[new_row,:])
				print(locations[row,:])
			#for col in np.arange(locations.shape[0]):
	print(np.where(np.isnan(output)))
	print(output)
	quit()
	from_matrix = np.zeros([5,2])
	to_matrix = np.zeros([5,2])
	for i in np.arange(0,len(locations),5):
		from_matrix = locations[i:i+5,:]
		for j in np.arange(0,len(locations),5):
			to_matrix = locations[j:j+5,:]
			#print("Here")
			#print(from_matrix.shape[0])
			#print(to_matrix.shape[0])
			try:
				geocode_result = GMAPS_CLIENT.distance_matrix(from_matrix,to_matrix,mode="walking")
			except googlemaps.exceptions.Timeout:
				np.save('data/baltimore_grid',test1,baltimore_grid)
				np.save('data/temp_distance_matrix.npy',old_matrix)
				return(output)
			print(i,j)
			time.sleep(1)
			#print(output)
			for k in np.arange(from_matrix.shape[0]):
				for l in np.arange(to_matrix.shape[0]):
					if(geocode_result['rows'][k]['elements'][l]['status'] == 'OK'):
						output[i+k,j+l] = geocode_result['rows'][k]['elements'][l]['distance']['value']
					else:
						np.save('data/baltimore_grid',baltimore_grid)
						np.save('data/temp_distance_matrix.npy',old_matrix)
						return(output)
						print(geocode_result['rows'][i+k]['elements'][j+l])
						output[i+k,j+l] = np.nan
	#np.save('data/distance_matrix',output)
	#np.save('data/baltimore_grid',baltimore_grid)
	return(output)
		
	
#DISTANCE_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
#DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'
#
#locations = [
#	'615 N Wolfe Street, Baltimore, MD',
#	'501 E Pratt Street, Baltimore, MD',
#	'333 W Camden St, Baltimore, MD',
#	'1876 Mansion House Drive Druid Hill Park,, 1876 Mansion House Dr, Baltimore, MD 21217'
#]
#
#i=0
#j=1
#print(len(locations))
#print(distance_matrix(locations))
#print(distance_matrix(locations)['rows'][i]['elements'][j]['distance']['value'])
