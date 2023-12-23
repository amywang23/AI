import tkinter as tk
import time
from time import perf_counter
from collections import  defaultdict
from distanceDemo import calcd
import sys
import heapq
import math

with open("rrEdges.txt") as f:
    edge_list = [line.strip() for line in f]

with open("rrNodeCity.txt") as f:
    city_list = [line.strip() for line in f]

with open("rrNodes.txt") as f:
    node_list = [line.strip() for line in f]

cities = defaultdict(list)
edges = defaultdict(list)
nodes = defaultdict(list)
distances = defaultdict(list)
lines = defaultdict(list)
minlat = 0
maxlat = 0
minlong = 0
maxlong = 0
height = 800
width = 1500


def buildStructure():
    global maxlat, minlat, maxlong, minlong
    for line in city_list:
        index = line.index(" ")
        cityname = line[index+1:]
        citynumber = line[:index]
        cities[cityname].append(citynumber)

    maxlat = 0
    minlat = 10000
    maxlong = -10000
    minlong = 0

    for line in node_list:
        s = line.split()
        nodes[s[0]].append(float(s[1]))
        nodes[s[0]].append(float(s[2]))
        #print("node: " , s[0], nodes[s[0]])
        distances[s[0]] = math.inf
        if (float(s[1])<minlat):
            minlat = float(s[1])
        if (float(s[1])>maxlat):
            maxlat = float(s[1])
        if (float(s[2])<minlong):
            minlong = float(s[2])
        if (float(s[2])>maxlong):
            maxlong = float(s[2])
    # print("minlat", minlat, "maxlat", maxlat, "minlong", minlong, "maxlong", maxlong)
        

  
    for line in edge_list:
        s = line.split()
        if (s[0]<s[1]):
            sm = 1
        else:
            sm = 2

        node1 = nodes[s[0]]
        node2 = nodes[s[1]]
        # print("node1", node1, "node2", node2)
        distance = calcd(node1, node2)
        edges[s[0]].append((s[1], distance))
        edges[s[1]].append((s[0], distance))

        cor1 = calc_cor(node1)
        cor2 = calc_cor(node2)
        #print("node1", node1, "node2", node2,"cor1", cor1, "cor2", cor2)

        if (sm ==1):
            if ( len(lines[(s[0],s[1])]) == 0):
                lines[(s[0],s[1])].append(cor1)
                lines[(s[0],s[1])].append(cor2)
        else:
            if (len(lines[(s[1],s[0])]) == 0):
                lines[(s[1],s[0])].append(cor2)
                lines[(s[1],s[0])].append(cor1)
    return


def calc_cor(node):
    y1, x1 = node

    x = (x1 - minlong) * width / (maxlong - minlong)
    y = height - (y1 - minlat) * height / (maxlat - minlat)
    return (int(round(x)), int(round(y)))



def Dijkstra(node, target, r, c):

    distances[node] = 0
    fringe = []
    path = []
    path.append(node)
    heapq.heapify(fringe)
    heapq.heappush(fringe, (distances[node], node, path))

    count = 0
    while len(fringe) > 0 :
        v = heapq.heappop(fringe)
        city = v[1]
        if (city == target):
            print("Dijkstra reached target")
            draw_final_route(v[2], r, c)
            return
        nei = edges[city]
        for nb in nei:
            new_distance = distances[city] + nb[1]
            if (new_distance < distances[nb[0]] ):
                distances[nb[0]] = new_distance
                newpath = list(v[2])
                newpath.append(nb[0])
                heapq.heappush(fringe, (distances[nb[0]], nb[0], newpath))
                draw_search_route(city, nb[0], r, c)
                
    return None



def astar(node, target, r, c):
   
    distances[node] = 0
    fringe = []
    path = []
    path.append(node)
    heapq.heapify(fringe)
    heapq.heappush(fringe, (distances[node], node, path))

    count = 0
    while len(fringe) > 0 :
        v = heapq.heappop(fringe)
        city = v[1]
        if (city == target):
            print("Astar reached target")
            draw_final_route(v[2], r, c)
            return
        nei = edges[city]
        for nb in nei:
            new_distance = distances[city] + nb[1]
            node1 = nodes[nb[0]]
            node2 = nodes[target]
            estimate = calcd(node1, node2)
            if (new_distance < distances[nb[0]] ):
                distances[nb[0]] = new_distance
                newpath = list(v[2])
                newpath.append(nb[0])
                heapq.heappush(fringe, (distances[nb[0]]+estimate, nb[0], newpath))
                draw_search_route(city, nb[0], r, c) 
    return None

def create_routes(c):

    for l in lines:
        values = lines[l]
        line = c.create_line([(values[0][0], values[0][1]), (values[1][0], values[1][1])], tag='grid_line')
        lines[l].append(line)
	

def draw_final_route(path, r, c):
    for i in range(len(path)-1):
        c1 = path[i]
        c2 = path[i+1]
        if (c1 < c2):
            l = (c1, c2)
        else:
            l = (c2, c1)
            values = lines[l]
            c.itemconfig(values[2], fill="blue") #changes color of one line to blue
            r.update()
    return

def draw_search_route(c1, c2, r, c):

    if (c1 < c2):
        l = (c1, c2)
    else:
        l = (c2, c1)
    
    values = lines[l]
    c.itemconfig(values[2], fill="red") #changes color of one line to red
    r.update()

    return

city1 = sys.argv[1]
city2 = sys.argv[2]

buildStructure()

root = tk.Tk() #creates the frame

canvas = tk.Canvas(root, height=800, width=1500, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
create_routes(canvas)
canvas.pack(expand=True) #packing widgets places them on the board

#Dijkstra(cities[city1][0], cities[city2][0], root, canvas)
astar(cities[city1][0], cities[city2][0], root, canvas)
root.mainloop()
