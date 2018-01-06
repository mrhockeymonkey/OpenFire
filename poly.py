import pylygon
import numpy
p1 = pylygon.Polygon([(20,20),(40,20),(60,60),(100,40),(25,25)])
p2 = pylygon.Polygon([(20,20),(40,20),(60,60),(100,40),(25,25)])
r = p1.collidepoly(p2)
print(r)
#print(r)

