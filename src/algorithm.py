# return a list of co-ordinates, given a list of all points
from point import *
from path import *
from collections import deque
import math
import heapq


# return a list of paths, every path is a pair of points every point is a pair (x,y)
def shortest(start, paths, end):

    paths_aug = [Path(start,start)]+paths+[Path(end,end)]

    n = len(paths_aug)
    distances = []
    lines = []
    for i in range(n):
        distances.append([])
        lines.append([])
        for j in range(n):
            distances[i].append(math.inf)
            lines[i].append(None)

    for i in range(n):
        for j in range(n):
            distances[i][j], lines[i][j] = dist_lines(paths_aug[i],paths_aug[j])
        print(distances[i])

    mp = min_path(distances)

    solution = []

    for i in range(len(mp)-1):
        solution.append(lines[mp[i]][mp[i+1]])

    
    return solution

def image(p, l): # projection of p on l
    I = Point()
    x1, y1 = l.start.x, l.start.y
    x2, y2 = l.end.x, l.end.y
    B = x2-x1
    A = y2-y1
    if A == 0 and B == 0:
        I.x, I.y = x1, y1
        return I
    x0, y0 = p.x, p.y
    t = (A*(y0-y1)+B*(x0-x1))/(A**2 + B**2)
    
    I.x, I.y = B*t+x1, A*t+y1
    return I

def dist(p,q): # Euclidean distance
    return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)

def dist_line(p, l): # distance from point to line segment (returns distance and path)
    img = image(p,l)
    if l.contains(img):
        return dist(p,img), Path(p, img)
    d_1 = dist(p, l.start)
    d_2 = dist(p, l.end)
    if d_1 > d_2:
        return d_1, Path(p, l.start)
    return d_2, Path(p, l.end)
    pass

def dist_lines(line_A,line_B): # distance between two line segments
    # find intersection point and check
    x1, y1, x2, y2 = line_B.start.x, line_B.start.y, line_B.end.x, line_B.end.y
    x3, y3, x4, y4 = line_A.start.x, line_A.start.y, line_A.end.x, line_A.end.y
    A = y2-y1
    B = x2-x1
    C = y4-y3
    D = x4-x3
    disc = B*C - A*D
    if disc != 0:
        t = (D*(y1-y3)-C*(x1-x3))/disc
        intersection = Point()
        intersection.x, intersection.y = x1+B*t, y1+A*t
        if line_A.contains(intersection) and line_B.contains(intersection):
            return 0.0, Path(intersection, intersection)
    
    d = [None]*8
    lin = [None]*8
    d[1], lin[1] = dist_line(line_A.start,line_B)
    d[2], lin[2] = dist_line(line_A.end, line_B)
    d[3], lin[3] = dist_line(line_B.start, line_A)
    d[4], lin[4] = dist_line(line_B.end, line_A)
    d[5], lin[5] = dist(line_A.start, line_B.start), Path(line_A.start, line_B.start)
    d[6], lin[6] = dist(line_A.start, line_B.end), Path(line_A.start, line_B.end)
    d[7], lin[7] = dist(line_A.end, line_B.start), Path(line_A.end, line_B.start)
    d[0], lin[0] = dist(line_A.end, line_B.end), Path(line_A.end, line_B.end)

    min_i = 0
    for i in range(8):
        if d[i] < d[min_i]:
            min_i = i
    return d[min_i], lin[min_i]


"""
function Dijkstra(Graph, source):
 2      
 3      for each vertex v in Graph.Vertices:
 4          dist[v] ← INFINITY
 5          prev[v] ← UNDEFINED
 6          add v to Q
 7      dist[source] ← 0
 8      
 9      while Q is not empty:
10          u ← vertex in Q with min dist[u]
11          remove u from Q
12          
13          for each neighbor v of u still in Q:
14              alt ← dist[u] + Graph.Edges(u, v)
15              if alt < dist[v]:
16                  dist[v] ← alt
17                  prev[v] ← u
18
19      return dist[], prev[]
"""

# Dijkstra
def min_path(graph): # takes in a graph (adjacency matrix) and finds the shortest path from node 0 to node n
    n = len(graph)

    for i in range(n):
        for j in range(n):
            if graph[i][j] == 0:
                graph[i][j] = 0.001 # This implementation cannot handle when an edge-weight is zero

    if n == 0:
        return []

    distances = [float('inf')] * n
    prev_node = [None]*n
    distances[0] = 0
    pq = [(0, 0)]  # Priority queue to store nodes with their distances

    while pq:
        dist, node = heapq.heappop(pq)

        if node == n - 1:  # Reached the destination node
            path = []
            while node is not None:
                path.append(node)
                node = prev_node[node]
                print(path)
            return list(reversed(path))  # Return the path in the correct order

        for neighbor, weight in enumerate(graph[node]):
            if weight > 0:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
                    prev_node[neighbor] = node

    return []  # Return empty list if no path exists