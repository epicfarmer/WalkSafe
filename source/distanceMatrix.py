import numpy as np
import gmapsRequest as gRequest
import gridBaltimore

def _r_increment(src, dst, scale):
	if (asdfasdf):
		return src

	if(defined):
		return next_point(src, dst, scale)

	if (src.x > BALTIMORE_X_MAX):
		src.x = BALTIMORE_X_MIN
		src.y = BALTIMORE_Y_MIN
		src.y += scale

	if(src.y > BALTIMORE_Y_MAX):
		src.x = BALTIMORE_X_MIN
		src.y = BALTIMORE_Y_MIN
		dst.x += scale

	if(dst.x > BALTIMORE_X_MAX):
		src.x = BALTIMORE_X_MIN
		src.y = BALTIMORE_Y_MIN
		dst.y += scale

	if(dst.y >= max):
		scale += 1.0
		src.x = BALTIMORE_X_MIN
		src.y = BALTIMORE_Y_MIN
		return _r_increment(src, dst, scale)

def _next_point(src, dst, scale):
	while not (gridBaltimore.within(src) and gridBaltimore.within(dst)):
		if is_max(src, dst):
			scale += 1.0

	return src, dst


#Get distance matrix between a set of locations
#input:
#	to_locations   (list:string)	names of locations to get distances to
#	from_locations (list:string)	names of locations to get distances from
#output:
#	a numpy array where (i,j)th entry is the distance from from_locations[i] to to_locations[j]
def assymetric_distance_matrix(to_locations,from_locations):
	geocode_result = gRequest.distance_matrix(from_locations,to_locations,mode="walking")
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

#Get distance matrix over all of baltimore
#input:
#	x_bins (integer)	number of columns in the grid to overlay on baltimore
#	y_bins (integer)	number of rows in the grid to overlay on baltimore
#output:
#locations	a set of (longitude,latitude) pairs for locations given by the grid defined by x_bins and y_bins (see getBaltimoreGrid. in source/gridBaltimore.py)
#distances	a numpy array where (i,j)th entry is the distance from from_locations[i] to to_locations[j]
def baltimore_distance_matrix(xbins, ybins):
	baltimore_grid = gb.getBaltimoreGrid(xbins,ybins)
	baltimore_grid.long,baltimore_grid.lat = sg.asLineString(baltimore_grid).xy
	locations = np.array([baltimore_grid.lat,baltimore_grid.long]).T
	distances = distance_matrix(locations)
	np.save('data/distance_matrix',distances)
	np.save('data/baltimore_grid',locations)
	return([distances,locations])

#Get distance matrix over all of baltimore which refines and updates over time
#input:
#output:
#locations	a set of (longitude,latitude) pairs for locations given by the grid defined by x_bins and y_bins (see getBaltimoreGrid. in source/gridBaltimore.py)
#distances	a numpy array where (i,j)th entry is the distance from from_locations[i] to to_locations[j]
def refining_baltimore_distance_matrix():
	try:
		baltimore_grid = np.load('data/baltimore_grid.npy')
		old_matrix = np.load('data/temp_distance_matrix.npy')
	except:
		print('creating new matrix')
		[old_matrix,baltimore_grid] = baltimore_distance_matrix(3,3)

	latitudes,longitudes = sg.asLineString(baltimore_grid).xy
	locations = np.array([latitudes,longitudes]).T
	output = old_matrix

	if (np.prod(np.shape(np.where(np.isnan(old_matrix)))) == 0):
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


import matplotlib.pyplot as plt

if __name__ == '__main__':
	nbins = 1
	processed = []
	while nbins < 4:
		nbins *= 2
		print nbins
		coord_list = gridBaltimore.bins(nbins)
		for coords in coord_list:
			coords = list(coords)
			if coords not in processed:
				processed.append(coords)

	print len(processed)
	print processed

	x = map(lambda i: i[0], processed)
	y = map(lambda i: i[1], processed)

	plt.scatter(x, y)
	plt.show()