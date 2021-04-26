import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import time

from dijkstras import *
from Astar import *

start = (42.25,-71.05)
end =   (42.40,-71.2)
#start = (42.3,-71.1)
#end =   (42.35,-71.15)
test = int(input("use default (1 or 0): "))
if(test == 0):
    s_lat = float(input("enter starting latitude: "))
    s_long = float(input("enter starting longitude: "))

    d_lat = float(input("enter destination latitude: "))
    d_long = float(input("enter destination longitude: "))

    start = (s_lat,s_long)
    end = (d_lat,d_long)


#the +- .02 is to give a little buffer room in case the path needs to take a short detour,
#without it the path may not be found in the graph (or the wrong path is found)
#increasing it much more than this significantly slows down loading the graph though
north = max(start[0],end[0]) + .02
south = min(start[0],end[0]) - .02
east = max(start[1],end[1])  + .02
west = min(start[1],end[1])  - .02

print("Generating graph:")
t0 = time.time()
G = ox.graph_from_bbox(north,south,east,west, network_type='drive')

Gp = ox.project_graph(G)
Gc = ox.consolidate_intersections(Gp, rebuild_graph=True, tolerance=20, dead_ends=False)

t1 = time.time()
print("time to generate graph: ", t1-t0)

nodes, edges = ox.graph_to_gdfs(Gc, nodes=True, edges=True)

lats = [start[0], end[0]]
lngs = [start[1], end[1]]

points_list = [Point((lng, lat)) for lat, lng in zip(lats, lngs)]
points = gpd.GeoSeries(points_list, crs='epsg:4326')
points_proj = points.to_crs(Gp.graph['crs'])

source_node = ox.get_nearest_node(Gc, (points_proj[0].y, points_proj[0].x), method = 'euclidean')
target_node = ox.get_nearest_node(Gc, (points_proj[1].y, points_proj[1].x), method = 'euclidean')

s_closest = nodes.loc[source_node]
t_closest = nodes.loc[target_node]

t0 = time.time()
for i in range (0, 100):
    distances = dijkstra_get_distance(Gc,source_node,target_node)
    d_path = dijkstra_get_path(Gc,source_node, target_node,distances)
t1 = time.time()
print("average time to generate dijkstra path: ", (t1-t0)/100)

t0 = time.time()
for i in range (0, 100):
    distances = a_star_get_distance_euclidean(Gc,source_node,target_node)
    ae_path = a_star_get_path(Gc,source_node, target_node,distances)
t1 = time.time()
print("average time to generate euclidean astar path: ", (t1-t0)/100)

t0 = time.time()
for i in range (0, 100):
    distances = a_star_get_distance_manhattan(Gc,source_node,target_node)
    am_path = a_star_get_path(Gc,source_node, target_node,distances)
t1 = time.time()
print("average time to generate manhattan astar path: ", (t1-t0)/100)

t0 = time.time()
for i in range (0,100):
    route = nx.shortest_path(G=Gc, source=source_node, target=target_node, weight='length')
t1 = time.time()
print("average time for library to find shortest path: ", (t1-t0)/100)

fig, ax = ox.plot_graph_routes(Gc, [d_path,ae_path,am_path,route],route_colors = ["red","blue","green","yellow"])