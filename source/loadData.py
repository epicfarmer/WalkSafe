import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv("data/BPD_Part_1_Victim_Based_Crime_Data.csv")
latlong_data = data.loc[:,"Location 1"].str.split(',')
print(pd.DataFrame([latlong_data.str[0].str.replace("(",""),latlong_data.str[1].str.replace(")","")]))
#(latlong_data.str[0].str.replace("(","")
year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')

latlong_data[year>2014]
#fix this data from strings
#realdata = ???;
