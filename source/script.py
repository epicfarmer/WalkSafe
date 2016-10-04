import numpy as np
import LevelSetEstimation as lse
import gmapsRequest as dr
import gridBaltimore as gb
import loadData as data
import polyline as pl
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

twopoint = "{cynFjanrMoADoCJqCBoBFsFNaA@{CDsDHE?C?K@eBD"
line = pl.decode(twopoint)

safety_score = rw.reweight_linelist(line,crime,xinfo,yinfo)

print(safety_score)


#print(crime)
#print(crime_data)
#print(distances)
#print(locations)



#distances = np.array([[0,1],[1,0]])

## function not yet written :(
#distances = reweight_distance_matrix(distances,locations,crime)
