import django
django.setup()

import numpy as np
import gmapsRequest as gRequest
import gridBaltimore
import itertools
import heapq
import time
import datetime
from directionsWithScores.models import Distance, Coordinates
import logging


class DistanceMatrixRequest:
	def __init__(self, p1, p2s=list()):

		assert (isinstance(p1, Coordinates))
		assert (gridBaltimore.within(p1))
		self._point1 = p1

		assert (len(p2s) <= 25)
		for p2 in p2s:
			assert (isinstance(p2, Coordinates))
			assert (gridBaltimore.within(p2))
		self._points2 = p2s

		self._results = None

	def add_point(self, point):
		if len(self._points2) >= 25:
			return False

		self._points2.append(point)

		return True

	def clear(self):
		self._points2 = []

	def length(self):
		return len(self._points2)

	def request(self):
		# googlemaps.exceptions.ApiError: INVALID_REQUEST
		assert (len(self._points2) <= 25)
		assert (len(self._points2) >= 1)
		axis1 = [(self._point1.lat, self._point1.lon)]
		axis2 = []

		for c in self._points2:
			if not Distance.objects.filter(src=self._point1, dst=c).exists():
				axis2.append((float(c.lat), float(c.lon)))

		if len(axis2) == 0:
			return 'Already requested'

		logging.info('Requesting distance matrix for')
		logging.info((axis1, axis2))

		self._results = gRequest.distance_matrix(axis1, axis2)

		logging.info("Finished request")
		
		assert(len(self._results['rows']) > 0)
		for r in self._results['rows']:
			src = self._point1
			assert(len(r['elements']) > 0)
			for idx, e in enumerate(r['elements']):
				logging.info(e['status'])
				dst = self._points2[idx]
				if Distance.objects.filter(src=src, dst=dst).exists():
					distance = Distance.objects.get(src=src, dst=dst)
				else:
					distance = Distance(src=src, dst=dst)
				distance.duration = datetime.timedelta(seconds=e['duration']['value'])
				distance.distance = e['distance']['value']
				distance.status = e['status']
				distance.save()
				logging.info("Saved distance between %s and %s" %  (src, dst))

		return self._results


class RequestState:
	def __init__(self, save_file='data/request_state'):
		self._save_file = save_file


class BaltimoreDistanceMatrix:
	def __init__(self):
		self._save_file = None
		self._matrix = None
		self._automatic_state = None

	def get_distance(self, point1, point2):
		pass

	def daily_import(self, point1, point2):
		pass


def save_results(results):
	# TODO
	pass


# Get distance matrix over all of baltimore
# input: RequestState
# output:
# locations	a set of (longitude,latitude) pairs for locations given by the grid defined by x_bins and y_bins (see getBaltimoreGrid. in source/gridBaltimore.py)
# distances	a numpy array where (i,j)th entry is the distance from from_locations[i] to to_locations[j]
def baltimore_distance_matrix():
	old_lon = []
	old_lat = []
	old_points = []

	new_lon = [gridBaltimore.LON_MIN, gridBaltimore.LON_MAX]
	new_lat = [gridBaltimore.LAT_MIN, gridBaltimore.LAT_MAX]

	while True:

		new_points = []
		for new_point in itertools.product(new_lat, old_lon):
			new_coords, created = Coordinates.objects.get_or_create(lat=Coordinates.round(new_point[0]),
			                                                        lon=Coordinates.round(new_point[1]),
			                                                        defaults={'update_date': datetime.datetime.now()})
			if created:
				new_coords.save()
			new_points.append(new_coords)

		for new_point in itertools.product(old_lat, new_lon):
			new_coords, created = Coordinates.objects.get_or_create(lat=Coordinates.round(new_point[0]),
			                                                        lon=Coordinates.round(new_point[1]),
			                                                        defaults={'update_date': datetime.datetime.now()})
			if created:
				new_coords.save()
			new_points.append(new_coords)

		for new_point in itertools.product(new_lat, new_lon):
			new_coords, created = Coordinates.objects.get_or_create(lat=Coordinates.round(new_point[0]),
			                                                        lon=Coordinates.round(new_point[1]),
			                                                        defaults={'update_date': datetime.datetime.now()})
			if created:
				new_coords.save()
			new_points.append(new_coords)

		# request directions between all the old points and all the new points
		logging.info("Requesting directions between old points(%i) and new points(%i)" %
		             (len(old_points), len(new_points)))
		for o in old_points:
			if gridBaltimore.within(o):
				request = DistanceMatrixRequest(o)
				for n in new_points:
					if gridBaltimore.within(n):
						if not request.add_point(n):
							request.request()
							request.clear()
							assert (request.add_point(n))
						# yield o, n

				request.request()
				request.clear()

		# request directions between the new points
		logging.info("Requesting directions between new points(%i)" % len(new_points))
		for n1 in new_points:
			if gridBaltimore.within(n1):
				request = DistanceMatrixRequest(n1)
				for n2 in new_points:
					if gridBaltimore.within(n2) and n1 < n2:

						if not request.add_point(n2):
							request.request()
							request.clear()
							assert (request.add_point(n2))
						# yield n1, n2

				if request.length() > 0:
					request.request()
				request.clear()

		# mark as finished
		for o in old_points:
			o.finished = True
			o.save()

		for n in new_points:
			n.finished = True
			n.save()

		# update old points
		old_points = list(heapq.merge(old_points, new_points))
		old_lon = list(heapq.merge(old_lon, new_lon))
		old_lat = list(heapq.merge(old_lat, new_lat))

		# calculate new_x and new_lat
		new_new_lon = []
		for nlon in range(len(old_lon) - 1):
			new_new_lon.append((old_lon[nlon] + old_lon[nlon + 1]) / 2.0)
		new_lon = new_new_lon

		new_new_lon = []
		for nlon in range(len(old_lat) - 1):
			new_new_lon.append((old_lat[nlon] + old_lat[nlon + 1]) / 2.0)
		new_lat = new_new_lon


# Get distance matrix over all of baltimore which refines and updates over time
# output:
# locations	a set of (longitude,latitude) pairs for locations given by the grid defined by x_bins and y_bins (see getBaltimoreGrid. in source/gridBaltimore.py)
# distances	a numpy array where (i,j)th entry is the distance from from_locations[i] to to_locations[j]
def refining_baltimore_distance_matrix():
	try:
		baltimore_grid = np.load('data/baltimore_grid.npy')
		old_matrix = np.load('data/temp_distance_matrix.npy')
	except:
		print('creating new matrix')
		[old_matrix, baltimore_grid] = baltimore_distance_matrix(3, 3)

	latitudes, longitudes = sg.asLineString(baltimore_grid).xy
	locations = np.array([latitudes, longitudes]).T
	output = old_matrix

	if (np.prod(np.shape(np.where(np.isnan(old_matrix)))) == 0):
		new_xbins = (np.shape(np.unique(locations[:, 0]))[0] + 1) * 2
		new_ybins = (np.shape(np.unique(locations[:, 1]))[0] + 1) * 2
		new_baltimore_grid = gridBaltimore.getBaltimoreGrid(new_xbins, new_ybins)
		new_baltimore_grid.long, new_baltimore_grid.lat = sg.asLineString(new_baltimore_grid).xy
		new_locations = np.array([new_baltimore_grid.lat, new_baltimore_grid.long]).T

		a = np.tile(locations, [new_locations.shape[0], new_locations.shape[1], 1, 1])

		print(a.shape, locations.shape, new_locations.shape)
		# b = np.tile(new_locations,[1,1,locations.shape[0],locations.shape[1]])
		# output = np.zeros([new_locations.shape[0],new_locations.shape[0]],np.float32)*np.nan
		# a,b = np.meshgrid(locations,new_locations)
		# print( a.shape,b.shape )
		# print(locations.shape,new_locations.shape)
		# print(a.shape)
		quit()
		for row in np.arange(locations.shape[0]):
			new_row = np.where(np.sum(np.abs(locations[row, :] - new_locations), 1) == 0)
			for col in np.arange(locations.shape[0]):
				new_col = np.where(np.sum(np.abs(locations[col, :] - new_locations), 1) == 0)
				output[new_row, new_col] = old_matrix[row, col]
				print(new_locations[new_row, :])
				print(locations[row, :])
			# for col in np.arange(locations.shape[0]):
	print(np.where(np.isnan(output)))
	print(output)
	quit()
	from_matrix = np.zeros([5, 2])
	to_matrix = np.zeros([5, 2])
	for i in np.arange(0, len(locations), 5):
		from_matrix = locations[i:i + 5, :]
		for j in np.arange(0, len(locations), 5):
			to_matrix = locations[j:j + 5, :]
			# print("Here")
			# print(from_matrix.shape[0])
			# print(to_matrix.shape[0])
			try:
				request_result = GMAPS_CLIENT.distance_matrix(from_matrix, to_matrix, mode="walking")
			except googlemaps.exceptions.Timeout:
				np.save('data/baltimore_grid', test1, baltimore_grid)
				np.save('data/temp_distance_matrix.npy', old_matrix)
				return (output)
			print(i, j)
			time.sleep(1)
			# print(output)
			for k in np.arange(from_matrix.shape[0]):
				for l in np.arange(to_matrix.shape[0]):
					if (request_result['rows'][k]['elements'][l]['status'] == 'OK'):
						output[i + k, j + l] = request_result['rows'][k]['elements'][l]['distance']['value']
					else:
						np.save('data/baltimore_grid', baltimore_grid)
						np.save('data/temp_distance_matrix.npy', old_matrix)
						return (output)
						print(geocode_result['rows'][i + k]['elements'][j + l])
						output[i + k, j + l] = np.nan

	return (output)


if __name__ == '__main__':
	FORMAT = "%(levelname)s|%(asctime)-15s|%(message)s"
	logging.basicConfig(level=logging.DEBUG, format=FORMAT)

	num_points = 0
	points = set()
	logging.info("Starting script",)
	for point1, point2 in baltimore_distance_matrix():
		points.add(point1)
		points.add(point2)

		num_points += 1

		if num_points % 2500 == 0:
			print("2500!!!")
			break

		if num_points >= 28 * 2500:
			break
