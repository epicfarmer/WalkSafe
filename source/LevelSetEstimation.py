import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
#from sklearn import ??

################################################################
################################################################
###                   Level Set Estimators                   ###
################################################################
################################################################
###This file defines functions for estimating level sets of an
###unknown probability distribution.
################################################################

################################################################
####Expectations: Data comes in a pd.DataFrame with three colums
####              x, y, and impact
####
####  x      - the x coordinate of the crime
####  y      - the y coordinate of the crime
####  t      - the time of the crime
####  impact - the severity of the crime as a number between 0
####           and 1 (0 being least severe and 1 being most)
####
####  x and y are required, but t and impact are optional
###############################################################

###############################################################
####Testing:
####        Code for validating input
###############################################################
#TODO: Write this


###############################################################
def getTestData(number_rows=10,include_t=False,include_impact=False):
	number_columns = 2+include_t+include_impact;
	columns = ['x','y'];
	if(include_t):
		columns.append('t');
	if(include_impact):
		columns.append('impact');
	return pd.DataFrame(data=np.random.rand(number_rows,number_columns),columns=columns);

def plotData(data):
	plt.plot(data['x'],data['y'],'+');
	plt.show();

def plotRasterData(data):
	plt.imshow(data,interpolation=None);
	plt.show();

def rasterizeData(data,binSize):
	xmin = np.min(data['x']);
	xmax = np.max(data['x']);
	ymin = np.min(data['y']);
	ymax = np.max(data['y']);
	xbins = int(np.ceil((xmax-xmin)/binSize));
	ybins = int(np.ceil((ymax-ymin)/binSize));
	raster = np.zeros([ybins,xbins],np.float32);
	print np.shape(data)[0]
	#Vectorize this
	for i in range((np.shape(data))[0]):
		row = data.iloc[i,:];
		xbin = np.floor((xmax - row['x'])/(xmax-xmin)*xbins);
		if(xbin == xbins):
			xbin -=1;
		ybin = np.floor((ymax - row['y'])/(ymax-ymin)*ybins);
		if(ybin == ybins):
			ybin -=1;
		raster[ybin,-xbin] += 1;
	return raster

def estimatePxy(data,x,y):
	for i in range((np.shape(data))[0]):
		distance = sqrt((x - data[i,'x'])**2 + (x - data[i,'x'])**2)


def estimateBoundary(rasterizedData,threshold,number):
	mask = np.zeros(np.shape(rasterizedData));
	mask = rasterizedData*1./number > (threshold*1./np.prod(np.shape(rasterizedData)));
	return mask;

