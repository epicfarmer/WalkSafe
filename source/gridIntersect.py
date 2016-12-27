import shapely.geometry as sg
#import matplotlib.pyplot as plt
import polyline
twopoint = "s_ynFhrnrM_@@"
#s_ynFhrnrM_@@
#s`ynFjrnrMA{A
#u`ynFnonrMuAF
#kcynFvonrMGcECgCC_C
twopoint = "{cynFjanrMoADoCJqCBoBFsFNaA@{CDsDHE?C?K@eBD"

line = polyline.decode(twopoint)
path1 = sg.LineString(line)
print(path1)
path1 = sg.LineString([(-1,1),(1,0),(0.5,1),(2,-1)])
path2 = sg.LineString([(1,1),(0,0)])
#square = sg.Polygon([(39,-77),(40,-77),(40,-76),(39,-76)])
square = sg.Polygon([(0,0),(0,1),(1,1),(1,0)])

if(path1.intersects(path2)):
	intersection = path1.intersection(path2)
square.x,square.y=square.exterior.xy
path1.x,path1.y = path1.xy
path3 = path1.intersection(square)
path3.x,path3.y = path3[0].xy
print(path3.length)
plt.plot(square.x,square.y,'g',path1.x,path1.y,'b',path3.x,path3.y,'r--')
#{plt.plot(square.x,square.y,'r',path1.x,path1.y,'b')
plt.show()
