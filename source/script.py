import LevelSetEstimation as l
import numpy as np

data = l.getTestData(10000);
data[:5000]['x'] += 1
data[:1000]['x'] += 1
data[4000:6000]['x'] += 1
data[5000:7000]['y'] += 1
l.plotData(data);
print(1./np.sqrt(np.sqrt(10000)))
raster = l.rasterizeData(data,.5);
l.plotRasterData(raster);
mask = l.estimateBoundary(raster,.1,10000);
l.plotRasterData(mask);
