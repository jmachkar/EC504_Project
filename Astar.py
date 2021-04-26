import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

import heapq as heapq

def a_star_get_distance_euclidean(G,source,target):
    G_succ = G.succ
    G_nodes = G.nodes

    push = heapq.heappush
    pop = heapq.heappop
    heap = []
    actual_distance = {source:0} #save actual distances of each node
    marked = {}            #nodes that have been popped
    #distance = {source:0} #current distance to each node
    push(heap,(0,source))
    x2 = G_nodes[target]['x']
    y2 = G_nodes[target]['y']
    while heap:
        (h_d,v) = pop(heap)
        d = actual_distance[v]
        if v in marked:
            continue        #v may have been popped bc skipping decrease key and just adding an extra
        marked[v] = 1
        if v == target:
            break           #found the target node
        for u, e in G_succ[v].items():  #u is next vertex number, e is information about the edge
            cost = e[0]['length']
            x1 = G_nodes[u]['x']
            y1 = G_nodes[u]['y']
            heur_d = ox.distance.euclidean_dist_vec(y1, x1, y2, x2) #use euclidian distance from u to target for heap
            if(cost == None):
                continue        #means data for the edge is missing
            dist = d + cost
            if u in marked:
                continue
            if u in actual_distance:
                if dist < actual_distance[u]:
                    actual_distance[u] = dist #save actual distance of u
                    push(heap,(dist + heur_d,u)) #dont NEED to update distance
            else:
               actual_distance[u] = dist
               push(heap,(dist + heur_d,u))
    return actual_distance


#using manhattan distance ends up giving a ~slightly~ wrong shortest path
#but it is 10x faster than dijkstra and 8x faster than euclidean distance
def a_star_get_distance_manhattan(G,source,target):
    G_succ = G.succ
    G_nodes = G.nodes

    push = heapq.heappush
    pop = heapq.heappop
    heap = []
    actual_distance = {source:0} #save actual distances of each node
    marked = {}            #nodes that have been popped
    #distance = {source:0} #current distance to each node
    push(heap,(0,source))
    x2 = G_nodes[target]['x']
    y2 = G_nodes[target]['y']
    while heap:
        (h_d,v) = pop(heap)
        d = actual_distance[v]
        if v in marked:
            continue        #v may have been popped bc skipping decrease key and just adding an extra
        marked[v] = 1
        if v == target:
            break           #found the target node
        for u, e in G_succ[v].items():  #u is next vertex number, e is information about the edge
            cost = e[0]['length']
            x1 = G_nodes[u]['x']
            y1 = G_nodes[u]['y']
            heur_d = abs(y2-y1)+abs(x2-x1)      #for the manhattan
            if(cost == None):
                continue        #means data for the edge is missing
            dist = d + cost
            if u in marked:
                continue
            if u in actual_distance:
                if dist < actual_distance[u]:
                    actual_distance[u] = dist #save actual distance of u
                    push(heap,(dist + heur_d,u)) #dont NEED to update distance
            else:
               actual_distance[u] = dist
               push(heap,(dist + heur_d,u))
    return actual_distance    


#takes in the graph, source, target and distances and works backwards from the target following the
#lowest weight path to the source
def a_star_get_path(G,source,target,distances):
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