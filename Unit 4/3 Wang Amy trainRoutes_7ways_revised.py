import tkinter as tk
import time
from time import perf_counter
from collections import  defaultdict
from collections import deque
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
distances_target = defaultdict(list)
lines = defaultdict(list)
redlines = []
minlat = 0
maxlat = 0
minlong = 0
maxlong = 0
height = 800
width = 1500
route_counter = 0


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
        distances_target[s[0]] = math.inf
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

def biDijkstra(start, target, r, c):
    distances[start] = 0
    distances_target[target] = 0

    q1 = []
    q2 = []
    path1 = []
    path1.append(start)
    path2 = []
    path2.append(target)
    heapq.heapify(q1)
    heapq.heappush(q1, (distances[start], start, path1))
    heapq.heapify(q2)
    heapq.heappush(q2, (distances_target[target], target, path2))
   
    map1 = defaultdict(list)
    map2 = defaultdict(list)
    map1[start] = path1
    map2[target] = path2
    visited1 = set()
    visited2 = set()
    visited1.add(start)
    visited2.add(target)

    while (len(q1) > 0 and len(q2) > 0):
        v1 = heapq.heappop(q1)
        city1 = v1[1]
        if (city1 == target):
            print("biDijkstra reached target front distance=", v1[0])
            draw_final_route(v1[2], r, c)
            return

        v2 = heapq.heappop(q2)
        city2 = v2[1]
        if (city2 == start):
            print("biDijkstra reached target back distance=", v2[0])
            draw_final_route(v2[2], r, c)
            return
            
        for nb in edges[city1]:
            neighbor = nb[0]
            new_distance = distances[city1] + nb[1]
            if (new_distance < distances[neighbor] ):
                distances[neighbor] = new_distance
                newpath = list(v1[2])
                newpath.append(neighbor)
                heapq.heappush(q1, (distances[neighbor], neighbor, newpath))
                visited1.add(neighbor)
                map1[neighbor] = newpath

                if neighbor in visited2:  #found when searching from target
                    list2 = map2[neighbor]
                    if len(list2) > 0:
                        list2.pop()
                        list2.reverse()
                    print("biDijkstra meet from front distance=", distances[neighbor]+distances_target[neighbor])
                    draw_final_route(map1[neighbor] + list2, r, c)
                    return
            draw_search_route(city1, neighbor, r, c)

        for nb in edges[city2]:
            neighbor = nb[0]
            new_distance = distances_target[city2] + nb[1]
            node1 = nodes[neighbor]
            node2 = nodes[start]
            estimate = calcd(node1, node2)
            if (new_distance < distances_target[neighbor] ):
                distances_target[neighbor] = new_distance
                newpath = list(v2[2])
                newpath.append(neighbor)
                heapq.heappush(q2, (distances_target[neighbor]+estimate, neighbor, newpath))
                visited2.add(neighbor)
                map2[neighbor] = newpath
                if neighbor in visited1:
                    list2 = map2[neighbor]
                    if len(list2) > 0:
                        list2.pop()
                        list2.reverse()
                    print("biA* meet from back distance=", distances[neighbor]+distances_target[neighbor])
                    #print("path", map1[neighbor], "-----", list2)
                    draw_final_route(map1[neighbor] + list2, r, c)
                    return
            draw_search_route(city2, neighbor, r, c)
    return None

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
            print("Dijkstra reached target distance=", v[0])
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
            print("Astar reached target distance=", v[0])
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

def reverseAstar(node, target, r, c):
   
    distances[node] = 0
    fringe = []
    path = []
    path.append(node)
    heapq.heapify(fringe)
    heapq.heappush(fringe, (0-distances[node], node, path))

    count = 0
    while len(fringe) > 0 :
        v = heapq.heappop(fringe)
        city = v[1]
        if (city == target):
            print("reverseAstar reached target distance=", 0-v[0])
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
                heapq.heappush(fringe, (0-(distances[nb[0]]+estimate), nb[0], newpath))
            draw_search_route(city, nb[0], r, c) 
    return None

def biAstar(start, target, r, c):
    distances[start] = 0
    distances_target[target] = 0

    q1 = []
    q2 = []
    path1 = []
    path1.append(start)
    path2 = []
    path2.append(target)
    heapq.heapify(q1)
    heapq.heappush(q1, (distances[start], start, path1))
    heapq.heapify(q2)
    heapq.heappush(q2, (distances_target[target], target, path2))
   
    map1 = defaultdict(list)
    map2 = defaultdict(list)
    map1[start] = path1
    map2[target] = path2
    visited1 = set()
    visited2 = set()
    visited1.add(start)
    visited2.add(target)

    while (len(q1) > 0 and len(q2) > 0):
        v1 = heapq.heappop(q1)
        city1 = v1[1]
        if (city1 == target):
            print("biA* reached target front distance=", v1[0])
            draw_final_route(v1[2], r, c)
            return

        v2 = heapq.heappop(q2)
        city2 = v2[1]
        if (city2 == start):
            print("biA* reached target back distance=", v2[0])
            draw_final_route(v2[2], r, c)
            return
            
        for nb in edges[city1]:
            neighbor = nb[0]
            new_distance = distances[city1] + nb[1]
            node1 = nodes[neighbor]
            node2 = nodes[target]
            estimate = calcd(node1, node2)
            if (new_distance < distances[neighbor] ):
                distances[neighbor] = new_distance
                newpath = list(v1[2])
                newpath.append(neighbor)
                heapq.heappush(q1, (distances[neighbor]+estimate, neighbor, newpath))
                visited1.add(neighbor)
                map1[neighbor] = newpath

                if neighbor in visited2:
                    list2 = map2[neighbor]
                    if len(list2) > 0:
                        list2.pop()
                        list2.reverse()
                    print("biA* meet from front distance=", distances[neighbor]+distances_target[neighbor])
                    draw_final_route(map1[neighbor] + list2, r, c)
                    return
            draw_search_route(city1, neighbor, r, c)


        for nb in edges[city2]:
            neighbor = nb[0]
            new_distance = distances_target[city2] + nb[1]
            node1 = nodes[neighbor]
            node2 = nodes[start]
            estimate = calcd(node1, node2)
            if (new_distance < distances_target[neighbor] ):
                distances_target[neighbor] = new_distance
                newpath = list(v2[2])
                newpath.append(neighbor)
                heapq.heappush(q2, (distances_target[neighbor]+estimate, neighbor, newpath))
                visited2.add(neighbor)
                map2[neighbor] = newpath

                if neighbor in visited1:
                    list2 = map2[neighbor]
                    if len(list2) > 0:
                        list2.pop()
                        list2.reverse()
                    print("biA* meet from back distance=", distances[neighbor]+distances_target[neighbor])
                    #print("path", map1[neighbor], "-----", list2)
                    draw_final_route(map1[neighbor] + list2, r, c)
                    return
            draw_search_route(city2, neighbor, r, c)
    return None


def DFS(node, target, r, c):

    distances[node] = 0
    fringe = deque()
    path = []
    path.append(node)
    fringe.append((distances[node], node, path))

    while len(fringe) > 0 :
        v = fringe.pop()
        city = v[1]
        if (city == target):
            print("DFS reached target distance=", v[0])
            draw_final_route(v[2], r, c)
            return
        nei = edges[city]
        for nb in nei:
            new_distance = distances[city] + nb[1]
            if (new_distance < distances[nb[0]] ):
                distances[nb[0]] = new_distance
                newpath = list(v[2])
                newpath.append(nb[0])
                fringe.append((distances[nb[0]], nb[0], newpath))
            draw_search_route(city, nb[0], r, c)
                
    return None

def k_DFS(start, target, r, c, k):
    distances[start] = 0
    fringe = deque()
    path = []
    path.append(start)
    fringe.append((distances[start], start, path))    

    while len(fringe)>0:
        v = fringe.pop()

        city = v[1]
        if (city == target):
            print("ID_DFS reached target distance=", v[0])
            draw_final_route(v[2], r, c)
            return v[2]
       
        if v[0] < k:
            # print("v0", v[0], "k ", k, "queue len", len(fringe))
            nei = edges[city]
            for nb in nei:
                # if nb[0] in v[2]:
                #     print("skip found in previous path", nb[0])
                #     continue
                new_distance = distances[city] + nb[1]
                if (new_distance < distances[nb[0]] ):
                    distances[nb[0]] = new_distance
                    newpath = list(v[2])
                    newpath.append(nb[0])
                    fringe.append((distances[nb[0]], nb[0], newpath))
                draw_search_route(city, nb[0], r, c)
                    # print("draw ", city, nb[0])
               
    return None


def ID_DFS(start, target, r, c):
    node1 = nodes[start]
    node2 = nodes[target]
    estimate = calcd(node1, node2)
    max_depth = int(estimate)+100
    result = None
    print("starting depth:", max_depth)
    while result is None:
        result = k_DFS(start, target, r, c, max_depth)
        if result is not None:
            break
        max_depth = max_depth + 100
        print("max depth:", max_depth, "reset routes")
        reset_red_route(r, c)
        for line in node_list:
            s = line.split()
            distances[s[0]] = math.inf
    return result

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
    global route_counter
    global redlines
    if (c1 < c2):
        l = (c1, c2)
    else:
        l = (c2, c1)
    
    values = lines[l]
    c.itemconfig(values[2], fill="red") #changes color of one line to red
    if route_counter >= 1000:
        r.update()
        route_counter = 0

    route_counter += 1
    redlines.append(values[2])
    return

def reset_red_route(r, c):
    global redlines
    for line in redlines:
        c.itemconfig(line, fill="black") #changes color of one line to black
    r.update()
    redlines = []
    return

city1 = sys.argv[1]
city2 = sys.argv[2]

buildStructure()

root = tk.Tk() #creates the frame

canvas = tk.Canvas(root, height=800, width=1500, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
create_routes(canvas)
canvas.pack(expand=True) #packing widgets places them on the board

print("Select an algorithm:")
print("1 - Dijkstra")
print("2 - A*")
print("3 - DFS")
print("4 - ID-DFS")
print("5 - Bidirectional Dijkstra")
print("6 - Reverse A*")
print("7 - Bidirectional A*")
option = input("Enter 1 to 7:  ")
print("selected option ", option)
start = perf_counter()
if option == '1':
    Dijkstra(cities[city1][0], cities[city2][0], root, canvas)
if option == '2':
    astar(cities[city1][0], cities[city2][0], root, canvas)
if option == '3':
    DFS(cities[city1][0], cities[city2][0], root, canvas)
if option == '4':
    ID_DFS(cities[city1][0], cities[city2][0], root, canvas)
if option == '5':
    biDijkstra(cities[city1][0], cities[city2][0], root, canvas)
if option == '6':
    reverseAstar(cities[city1][0], cities[city2][0], root, canvas)
if option == '7':
    biAstar(cities[city1][0], cities[city2][0], root, canvas)
end = perf_counter()
print("total time", end-start)
root.mainloop()
