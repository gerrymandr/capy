import json
import os.path
import warnings
from collections import Counter

import geopandas as gp
import networkx
import pandas as pd
import pysal
from networkx.readwrite import json_graph
from shapely.ops import cascaded_union

import utm

from shapely import geometry



# dummy file

# only in some range....

x = utm.from_latlon(-80, 80)[2]

from pyproj import Proj, transform

#inProj = Proj(init='epsg:3857')

inProj = Proj(init='epsg:3857')

outProj = Proj(init='epsg:4326')
x1,y1 = 1780865.9237387704, 803492.2251091545
x2,y2 = transform(inProj,outProj,x1,y1)
print x2,y2








print "success"
