import gridBaltimore
import gmapsRequest as gRequest
import numpy as np
import googlemaps



#Get distance matrix between a set of locations
#input:
#	Google Maps Distance Matrix JSON result
#output:
#	a numpy array where (i,j)th entry is the distance from from_locations[i] to to_locations[j]
#   OR None if something went wrong
def json_result_to_array(result):

	from_locations = result['rows']
	to_locations = result['rows'][0]['elements']
	n_from = len(from_locations)
	n_to = len(to_locations)

	# initialize to 0's
	output = np.zeros([n_from, n_to], np.float32)

	for i in range(n_from):
		row = result['rows'][i]['elements']
		for j in range(n_to):
			if row[j]['status'] == 'OK':
				output[i,j] = row[j]['distance']['value']
			else:
				print(row[j])
				output[i,j] = np.nan

	return output

def valid_pair(c1, c2):
	# TODO false if c2 <= c1. x is higher priority
	pass
