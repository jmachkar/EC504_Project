import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

import heapq as heapq

def dijkstra_get_distance(G,source,target):
    G_succ = G.succ

    push = heapq.heappush
    pop = heapq.heappop
    heap = []
    marked = {}            #nodes that have been popped
    distance = {source:0} #current distance to each node
    push(heap,(0,source))

    while heap:
        (d,v) = pop(heap)
        if v in marked:
            continue        #v may have been popped bc skipping decrease key and just adding an extra
        marked[v] = 1      
        if v == target:
            break           #found the target node
        for u, e in G_succ[v].items():  #u is next vertex number, e is information about the edge
            cost = e[0]['length']
            if(cost == None):
                continue        #means data for the edge is missing    
            dist = d + cost
            if u in marked:
                continue
            if u in distance:
                if dist < distance[u]:
                    distance[u] = dist
                    push(heap,(dist,u)) #dont NEED to update distance
            else:
               distance[u] = dist
               push(heap,(dist,u))
    return distance


#takes in the graph, source, target and distances and works backwards from the target following the
#lowest weight path to the source
def dijkstra_get_path(G,source,target,distances):
    G_pred = G.pred
    path = []
    v = target

    while v != source:
        path.insert(0,v)
        min = None
        for u, e in G_pred[v].items():
            if u in distances:
                if min == None:
                    min = distances.get(u)
                    v = u
                elif min > distances.get(u):
                    min = distances.get(u)
                    v = u            
    path.insert(0,v)
    return path