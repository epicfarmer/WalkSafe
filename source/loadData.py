import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import LevelSetEstimation as ls

data = pd.read_csv("data/BPD_Part_1_Victim_Based_Crime_Data.csv")
latlong_data = data.loc[:,"Location 1"].str.split(',')
latlong_data = pd.DataFrame(np.matrix([latlong_data.str[0].str.replace("(",""),latlong_data.str[1].str.replace(")","")]).T,dtype=float)
latlong_data.columns = ["y","x"]
latlong_data = latlong_data[latlong_data["y"] < 40]
year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')
plt.plot(latlong_data['x'].values,latlong_data['y'].values,'r*')
#plt.show()
raster_data = ls.rasterizeData(latlong_data,.005)
ls.plotRasterData(raster_data)


#latlong_data[year>2014]
#fix this data from strings
#realdata = ???;
