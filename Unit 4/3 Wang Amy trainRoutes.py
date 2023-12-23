from collections import  defaultdict, deque
from time import perf_counter
from distanceDemo import calcd
import sys
import heapq
import math

start = perf_counter()

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

def buildStructure():
    for line in city_list:
        index = line.index(" ")
        cityname = line[index+1:]
        citynumber = line[:index]
        cities[cityname].append(citynumber)

    for line in node_list:
        s = line.split()
        nodes[s[0]].append(float(s[1]))
        nodes[s[0]].append(float(s[2]))
        distances[s[0]] = math.inf

    for line in edge_list:
        s = line.split()
        node1 = nodes[s[0]]
        node2 = nodes[s[1]]
        distance = calcd(node1, node2)
        edges[s[0]].append((s[1], distance))
        edges[s[1]].append((s[0], distance))
    return

def Dijkstra(node):
    distances[node] = 0
    fringe = []
    heapq.heapify(fringe)
    heapq.heappush(fringe, (distances[node], node))
    
    while len(fringe) > 0 :
        v = heapq.heappop(fringe)
        city = v[1]
        nei = edges[city]
        for i in nei:
            new_d = distances[city] + i[1]
            if (new_d < distances[i[0]] ):
                distances[i[0]] = new_d
                heapq.heappush(fringe, (distances[i[0]], i[0]))   
    return None

def astar(node, target):
    distances[node] = 0
    fringe = []
    heapq.heapify(fringe)
    heapq.heappush(fringe, (distances[node], node))
    
    while len(fringe) > 0 :
        v = heapq.heappop(fringe)
        city = v[1]
        nei = edges[city]
        for i in nei:
            new_d = distances[city] + i[1]
            node1 = nodes[i[0]]
            node2 = nodes[target]
            estimate = calcd(node1, node2)
            if (new_d < distances[i[0]] ):
                distances[i[0]] = new_d
                heapq.heappush(fringe, (distances[i[0]]+estimate, i[0]))   
    return None

city1 = sys.argv[1]
city2 = sys.argv[2]

start = perf_counter()
buildStructure()
end = perf_counter()
print("Time to create data structure:", end - start)

start = perf_counter()
Dijkstra(cities[city1][0])
distance = distances[cities[city2][0]]
end = perf_counter()
print(city1, "to", city2, "with Dijkstra:", distance, "in", end-start, "seconds")

start = perf_counter()
astar(cities[city1][0], cities[city2][0])
distance = distances[cities[city2][0]]
end = perf_counter()
print(city1, "to", city2, "with A*:", distance, "in", end-start, "seconds")



