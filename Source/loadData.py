import pandas as pd
import numpu as np
import matplotlib.pyplot as plt
data = pd.read_csv("Data/BPD_Part_1_Victim_Based_Crime_Data.csv")
latlong_data = data.loc[:,"Location 1"];
year = data.loc[:,"CrimeDate"].str.split('/').str.get(2).astype('float')


latlong_data[year>2014]
#fix this data from strings
#realdata = ???;

