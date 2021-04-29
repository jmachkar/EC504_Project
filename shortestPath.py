import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import time

from dijkstras import *
from Astar import *

start = (42.0,-71.0)
end =   (42.4,-71.4)

#start = (42.3,-71.1)
#end =   (42.35,-71.15)
test = int(input("use default (1 or 0): "))
if(test == 0):
    print("If loading bigBoston.graphml as graph, 42.0 < latitude < 42.4; -71.4 < longitude < -71.0")
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
load = int(input("load from bigBoston.graphml (1 or 0): "))
if load == 0:
    print("Generating graph:")
    t0 = time.time()
    G = ox.graph_from_bbox(north,south,east,west, network_type='drive')

    Gp = ox.project_graph(G)
    Gc = ox.consolidate_intersections(Gp, rebuild_graph=True, tolerance=20, dead_ends=False)

    t1 = time.time()
    print("time to generate graph: ", t1-t0)
elif load == 1:
    print("loading graph:")
    t0 = time.time()
    #G = ox.io.load_graphml("bigBoston.graphml") cant use this bc it calls read_graphml wrong
    # all this code is essentially just copying load_graphml and fixing what was wrong with load_graphml
    default_node_dtypes = {
        "elevation": float,
        "elevation_res": float,
        "lat": float,
        "lon": float,
        "osmid": int,
        "street_count": int,
        "x": float,
        "y": float,
    }
    default_edge_dtypes = {
        "bearing": float,
        "grade": float,
        "grade_abs": float,
        "length": float,
        "osmid": int,
        "speed_kph": float,
        "travel_time": float,
    }
    G = nx.read_graphml("bigBoston.graphml", node_type=default_node_dtypes["osmid"])

    G = ox.io._convert_node_attr_types(G, default_node_dtypes)
    G = ox.io._convert_edge_attr_types(G, default_edge_dtypes)

    # remove node_default and edge_default metadata keys if they exist
    if "node_default" in G.graph:
        del G.graph["node_default"]
    if "edge_default" in G.graph:
        del G.graph["edge_default"]

    Gp = ox.project_graph(G)
    Gc = ox.consolidate_intersections(Gp, rebuild_graph=True, tolerance=20, dead_ends=False)
    t1 = time.time()
    print("time to load graph: ",t1-t0)
else:
    print("invalid input")
    exit(-1)


#print("starting to save graph...")
#t0 = time.time()
#ox.io.save_graphml(G,filepath="bigBoston.graphml")
#t1 = time.time()
#print("time to save graph: ", t1-t0)

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