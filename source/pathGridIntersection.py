#This comes from google
import numpy as np
import polyline

twopoint = "s_ynFhrnrM_@@"
#s_ynFhrnrM_@@
#s`ynFjrnrMA{A
#u`ynFnonrMuAF
#kcynFvonrMGcECgCC_C
#{cynFjanrMoADoCJqCBoBFsFNaA@{CDsDHE?C?K@eBD

print twopoint

line = polyline.decode(twopoint)

line = np.array(line)

grid = np.array([
	[[0,0],[1,1]],
	[[1,0],[2,1]],
	[[2,0],[3,1]],
	[[3,0],[4,1]],
	[[4,0],[5,1]],
	[[0,1],[1,2]],
	[[1,1],[2,2]],
	[[2,1],[3,2]],
	[[3,1],[4,2]],
	[[4,1],[5,2]],
	[[0,2],[1,3]],
	[[1,2],[2,3]],
	[[2,2],[3,3]],
	[[3,2],[4,3]],
	[[4,2],[5,3]],
	[[0,3],[1,4]],
	[[1,3],[2,4]],
	[[2,3],[3,4]],
	[[3,3],[4,4]],
	[[4,3],[5,4]],
	[[0,4],[1,5]],
	[[1,4],[2,5]],
	[[2,4],[3,5]],
	[[3,4],[4,5]],
	[[4,4],[5,5]]
])

for box in grid:
	point0 = box[0]
	point3 = box[1]
	point1 = np.array([box[0][0],box[1][1]])
	point2 = np.array([box[1][0],box[0][1]])
	line0 = np.array([point0,point1 - point0])
	line1 = np.array([point0,point2 - point0])
	line2 = np.array([point3,point1 - point3])
	line3 = np.array([point3,point2 - point3])
	#print(point0,point1,point2,point3)
	#print(line0,line1,line2,line3)
	print(point0,point1,point2,point3)
	print(line0)
	print(line1)
	print(line2)
	print(line3)
	input_line = line
	output_line = np.array(line)
	#line1 = point1-point2
