import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

##  Class to represent a graph
class Graph:
    def __init__(self,vertices, columns):
        self.graph = defaultdict(list) ##  Dictionary containing adjacency List
        self.V = vertices ##  No. of vertices
        self.C = columns
        self.vert_dict = {} ## Dictionary of dictionaries for nodes and weights
        self.top_order = [] ## Stores result of topologicalSort

##  Function to add an edge to graph
    def addEdge(self,u,v,cost):
        if cost > 0:
            self.graph[u].append(v)
        if u not in self.vert_dict:
            self.vert_dict[u] = {}
        self.vert_dict[u][v] = cost

##  The function to do Topological Sort.
    def topologicalSort(self):

##  Create a vector to store indegrees of all
##  vertices. Initialize all indegrees as 0.
        in_degree = [0]*(self.V)

##  Traverse adjacency lists to fill indegrees of
##  vertices.  This step takes O(V+E) time
        for i in self.graph:
            for j in self.graph[i]:
                in_degree[j] += 1

##  Create an queue and enqueue all vertices with
##  indegree 0
        queue = []
        for i in range(self.V):
            if in_degree[i] == 0:
                queue.append(i)

##  Initialize count of visited vertices
        cnt = 0

##  One by one dequeue vertices from queue and enqueue
##  adjacents if indegree of adjacent becomes 0
        while queue:

##  Extract front of queue (or perform dequeue)
##  and add it to topological order
            u = queue.pop(0)
            self.top_order.append(u)

##  Iterate through all neighbouring nodes
##  of dequeued node u and decrease their in-degree
##  by 1
            for i in self.graph[u]:
                in_degree[i] -= 1
##  If in-degree becomes zero, add it to queue
                if in_degree[i] == 0:
                    queue.append(i)

            cnt += 1

##  Check if there was a cycle
        if cnt != self.V:
            print("There exists a cycle in the graph")
        #else :
            #Print topological order
        #    print(self.top_order)

    def displayWeight(self, u):
        if u in self.vert_dict:
            for key in self.vert_dict[u]:
                print('Node', u, 'flows to node', key, 'and the volume is', self.vert_dict[u][key])
        else:
            print('Node', u, 'does not flow to any other node')

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        if start in self.vert_dict:
            for key in self.vert_dict[start]:
                #print(self.vert_dict[key])
                if self.vert_dict[start][key] < 0:
                    if key in visited:
                        continue
                    else:
                        #print(str(start) + ' is downstream from ' + str(key))
                        self.dfs(key, visited)
        return visited

    def fractionThrough(self, start):
##  Calls dfs and returns set of upstream nodes from start
        visited = self.dfs(start)
##  Filter topological order so that only upstream nodes are displayed
        filt_top_order = [x for x in self.top_order if x in visited]
        print(filt_top_order)
##  Dictionary to hold nodes as keys and fractions as values
        percents = {}
##  As long as there are upstream nodes calculate their fraction through
        for i in reversed(filt_top_order):
            down1 = 0
            down2 = 0
            down3 = 0
            down4 = 0
            down1mod = 0
            down2mod = 0
            down3mod = 0
            down4mod = 0
            down_frac = 0
            if i == start:
                percents[filt_top_order.pop()] = 1.0
                continue
            if i in self.vert_dict:
                for key in self.vert_dict[i]:
                    node_flow = 0
                    if self.vert_dict[i][key] > 0:
## This (below) checks if the neighbor's fraction has already
## been calculated, this is why the top sort is useful
                        if key in percents:
                            node_flow = percents[key]
                        if down1 == 0:
                            down1 = self.vert_dict[i][key]
## The mod variables take into account whether or not the downstream
## neighbor leads to the target node, if it does then the % of
## that flow is applied, if it does not then it's multiplied by 0
                            down1mod = down1 * node_flow
                            #print(down1, ' ', down1mod)
                        elif down2 == 0:
                            down2 = self.vert_dict[i][key]
                            down2mod = down2 * node_flow
                            #print(down2, ' ', down2mod)
                        elif down3 == 0:
                            down3 = self.vert_dict[i][key]
                            down3mod = down3 * node_flow
                            #print(down3, ' ', down3mod)
                        else:
                            down4 = self.vert_dict[i][key]
                            down4mod = down4 * node_flow
                            #print(down4, ' ', down4mod)
                down_frac = (down1mod + down2mod + down3mod + down4mod)/(down1 + down2 + down3 + down4)
                #print(i, ' ', down_frac)

            percents[filt_top_order.pop()] = down_frac

##  Create list to graph from -- Initialize to 0
        nodes = [0]*int(self.V)
        print('Percentage of water that flows from each cell through cell ' + str(start))
##  Replace relevant values
        for key in percents:
            nodes[key] = percents[key]*100
##  Split into smaller lists
        chunks = [nodes[x:x+(int(self.C))] for x in range(0, len(nodes), int(self.C))]
        x = np.array(chunks)

        return x, nodes
