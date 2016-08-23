import numpy as np
import LevelSetEstimation as lse
import directions as dr
import gridBaltimore as gb
import loadData as data
#import gridIntersect as gi
import reweightLinelist as rw



##Crime Map Estimation

crime_data = data.loadData()

##In theory, analysis should go here, but for now...

[crime,xinfo,yinfo] = data.loadRasterData()

##Distance Matrix
#[distances,locations]= data.loadDistanceData()
#[distances2,locations2] = rw.reweight_distance_matrix(distances,locations,crime_data,xinfo,yinfo)
#print(distances,distances2)

path = ""


#print(crime)
#print(crime_data)
#print(distances)
#print(locations)



#distances = np.array([[0,1],[1,0]])

## function not yet written :(
#distances = reweight_distance_matrix(distances,locations,crime)
