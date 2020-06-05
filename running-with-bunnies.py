'''
Running with Bunnies
====================

You and your rescued bunny prisoners need to get out of this collapsing 
death trap of a space station - and fast! Unfortunately, some of the 
bunnies have been weakened by their long imprisonment and can't run very 
fast. Their friends are trying to help them, but this escape would go a 
lot faster if you also pitched in. The defensive bulkhead doors have begun 
to close, and if you don't make it through in time, you'll be trapped! 
You need to grab as many bunnies as you can and get through the bulkheads 
before they close. 

The time it takes to move from your starting point to all of the bunnies 
and to the bulkhead will be given to you in a square matrix of integers. 
Each row will tell you the time it takes to get to the start, first bunny, 
second bunny, ..., last bunny, and the bulkhead in that order. The order 
of the rows follows the same pattern (start, each bunny, bulkhead). The 
bunnies can jump into your arms, so picking them up is instantaneous, and 
arriving at the bulkhead at the same time as it seals still allows for a 
successful, if dramatic, escape. (Don't worry, any bunnies you don't pick 
up will be able to escape with you since they no longer have to carry the 
ones you did pick up.) You can revisit different spots if you wish, and 
moving to the bulkhead doesn't mean you have to immediately leave - you 
can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact 
with the space station's security checkpoints and add time back to the 
clock. Adding time to the clock will delay the closing of the bulkhead doors, 
and if the time goes back up to 0 or a positive number after the doors have 
already closed, it triggers the bulkhead to reopen. Therefore, it might be 
possible to walk in a circle and keep gaining time: that is, each time a 
path is traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the 
most bunnies you can pick up and which bunnies they are, while still escaping 
through the bulkhead before the doors close for good. If there are multiple 
sets of bunnies of the same size, return the set of bunnies with the lowest 
prisoner IDs (as indexes) in sorted order. The bunnies are represented as a 
sorted list by prisoner ID, with the first bunny being 0. There are at most 
5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, 
bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. 

You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best 
combination for this space station hallway, so the answer is [1, 2].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 1, 1, 1, 1}, {1, 0, 1, 1, 1}, {1, 1, 0, 1, 1}, {1, 1, 1, 0, 1}, {1, 1, 1, 1, 0}}, 3)
Output:
    [0, 1]

Input:
Solution.solution({{0, 2, 2, 2, -1}, {9, 0, 2, 2, -1}, {9, 3, 0, 2, -1}, {9, 3, 2, 0, -1}, {9, 3, 2, 2, 0}}, 1)
Output:
    [1, 2]

-- Python cases --
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]
'''
import numpy as np
from collections import deque, namedtuple

def solution(times, times_limit):
    # Using: 
    #  - https://brilliant.org/wiki/dijkstras-short-path-finder/
    #  - https://www.geeksforgeeks.org/shortest-path-for-directed-acyclic-graphs/

    N = len(times)
    T = np.array(times)

    if N <= 2:
        return []

    # Reapply leading diagonal
    ix = np.eye(N) == True
    # T[ix] = 0

    # Look for any recursive grids
    # Where Tij = [[0, a], [b, 0]]
    # And a+b < 0
    # If so, you can gain infinite time and rescue everything
    recursive = False
    for i in range(0,N):
        for j in range(0,N):
            if i!=j:
                a = T[i,j]
                b = T[j,i]
                if a+b < 0:
                    return list(range(0,N-2))

    # Construct directed graph
    graph = Graph([])
    for i in range(0,N):
        for j in range(0,N):
            if i != j:
                c = T[i,j] 
                graph.add_edge(i,j,c,both_ends=False)
    
        
    # "There are at most 5 bunnies"
    # Cheap approach instead of recursion
    I = N-1
    essential_nodes = range(1,I)
    routes = list()
    # Always include a route home
    r = create_joint_route(graph,[0,I])
    routes.append( r )  

    for i in essential_nodes:        
        nodes = [0,i,I]
        remaining_nodes = list(essential_nodes)        
        r = create_joint_route(graph,nodes)
        routes.append( r )        
        remaining_nodes = list(np.setdiff1d(list(essential_nodes),r.nodes))

        for ii in remaining_nodes:
            nodes = [0,i,I]
            nodes.insert(-1,ii)
            r = create_joint_route(graph,nodes)
            routes.append( r )
            remaining_nodes = list(np.setdiff1d(list(essential_nodes),r.nodes))

            for iii in remaining_nodes:
                nodes = [0,i,I]
                nodes.insert(-1,ii)
                nodes.insert(-1,iii)
                r = create_joint_route(graph,nodes)
                routes.append( r )
                remaining_nodes = list(np.setdiff1d(list(essential_nodes),r.nodes))

                for iiii in remaining_nodes:
                    nodes = [0,i,I]
                    nodes.insert(-1,ii)
                    nodes.insert(-1,iii)
                    nodes.insert(-1,iiii)
                    r = create_joint_route(graph,nodes)
                    routes.append( r )
                    remaining_nodes = list(np.setdiff1d(list(essential_nodes),r.nodes))

                    for iiiii in remaining_nodes:
                        nodes = [0,i,I]
                        nodes.insert(-1,ii)
                        nodes.insert(-1,iii)
                        nodes.insert(-1,iiii)
                        nodes.insert(-1,iiiii)
                        r = create_joint_route(graph,nodes)
                        routes.append( r )
                        remaining_nodes = list(np.setdiff1d(list(essential_nodes),r.nodes))

    # Check for recursive paths, if so assume we can save everything
    if any([r.isrecursive for r in routes]):
        return list(range(0,N-2))

    # Eliminate routes > time limit
    [r.calculate_cost(T) for r in routes]
    routes = [r for r in routes if r.cost <= times_limit]
    if len(routes) == 0:
        # GODDAMIT THE BUNNIES!!
        return []

    # Count number of bunnies saved
    [r.score_essential(list(essential_nodes)) for r in routes]
    routes = sorted(routes, key=lambda x: (-x.count, x.rank, x.lowest))
    route = routes[0]

    bunnies = route.find_essential(essential_nodes)
    bunnies = [n-1 for n in bunnies]
    return bunnies   

def create_joint_route(graph,nodes):
    path = [nodes[0]]
    cost = 0

    for i in range(0,len(nodes)-1):
        A = nodes[i]
        B = nodes[i+1]
        p = graph.dijkstra(A,B)
        if p == -1: # Escape clause due to infinite recursion
            return Route(nodes[0],nodes[-1],[-1])
        path.extend(list(p)[1:])
        
    return Route(nodes[0],nodes[-1],path)

class Route:
    def __init__( self,start,end,path,cost=0 ):
        self.start = start
        self.end = end
        self.path = path
        self.cost = cost

    @property
    def nodes(self):        
        n = set(self.path)
        return list(n)
    
    @property
    def isrecursive(self):  
        return any(np.array(self.path) == -1)
    
    def __repr__(self):
        return str([self.path,self.cost])

    def __str__(self):
        return str([self.path,self.cost])

    def find_essential(self,essential_nodes):
        return list(np.intersect1d(essential_nodes,self.nodes)) 

    def score_essential(self,essential_nodes):
        n = self.find_essential(essential_nodes)
        self.count = len(n)
        self.rank = sum(n)
        if len(n) > 0:
            self.lowest = min(n)
        else: 
            self.lowest = 0
    
    def calculate_cost(self,T):
        cost = 0
        p = self.path
        for i in range(0,len(p)-1):
            A = p[i]
            B = p[i+1]
            cost = cost + T[A][B]
        self.cost = cost
        return cost


# From: https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc
# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        # print(f"Determine Dijkstra's path from {source} to {dest}")
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            # Protect against repeating patterns
            l = len(path)
            if l%2 == 0: # iseven
                p = list(path)
                h = int(l/2)
                if p[0:h] == p[h:l]: # repeats
                    return -1

            if current_vertex == source:
                break
            current_vertex = previous_vertices[current_vertex]            
        if path:
            path.appendleft(current_vertex)

        # cost = self.get_cost(path)
        return path #, cost


def run_solution(x,t):
    print("Input is " + str(x) + ", time is " + str(t))
    y = solution(x,t)
    print("Output is " + str(y))
'''
# Circular route
run_solution([
        [ 0, 1, 5, 9, 1], 
        [ 5, 0, 1, 9, 1], 
        [-3, 5, 0, 9, 1], 
        [ 5, 5, 5, 0, 1],
        [ 5, 5, 5, 5, 0]
    ], 3)

# Circular route
run_solution([
        [ 0, 1, 5, 9, 1], 
        [ 5, 0, 1, 9, 1], 
        [ 5, 5, 0, 1, 1], 
        [ 5,-3, 5, 0, 1],
        [ 5, 5, 5, 5, 0]
    ], 3)

# Input:
run_solution([
        [0, 2, 2, 2, -1], 
        [9, 0, 2, 2, -1], 
        [9, 3, 0, 2, -1], 
        [9, 3, 2, 0, -1], 
        [9, 3, 2, 2, 0]
    ], 1)
# Output:
#     [1, 2]

# Input:
run_solution([
        [0, 1, 1, 1, 1], 
        [1, 0, 1, 1, 1], 
        [1, 1, 0, 1, 1], 
        [1, 1, 1, 0, 1], 
        [1, 1, 1, 1, 0]
    ], 3)

run_solution([
        [0, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 1, 1, 1, 1, 1, 1], 
        [1, 1, 0, 1, 1, 1, 1, 1], 
        [1, 1, 1, 0, 1, 1, 1, 1], 
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0]
    ], 7)
# Output:
#     [0, 1]

run_solution([
        [ 0, 1, 5, 1], 
        [-3, 0, 8, 1], 
        [ 1, 8, 0, 1], 
        [ 5, 5, 5, 0]
    ], 3)

run_solution([
        [ 0, 1], 
        [ 1, 0]
    ], 3)

run_solution([
        [ 0, 1, 1], 
        [ 1, 0, 1],
        [ 1, 1, 0]         
    ], 3)

run_solution([
        [ 0, 9, 1], 
        [ 1, 0, 1],
        [ 1, 9, 0]         
    ], 3)

run_solution([
        [ 0, 9, 1, 1], 
        [ 1, 0, 1, 1],
        [ 1, 9, 0, 1],
        [ 9, 9, 9, 0]            
    ], 3)

run_solution([
        [ 0, 1, 1], 
        [ 9, 0, 9],
        [ 1, 1, 0]         
    ], 3)

run_solution([
        [0]
    ], 3)

run_solution([
        []
    ], 3)

# Input:
run_solution([
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0]
    ], 3)

run_solution([
        [0, -1, -1, -1, -1], 
        [-1, 0, -1, -1, -1], 
        [-1, -1, 0, -1, -1], 
        [-1, -1, -1, 0, -1], 
        [-1, -1, -1, -1, 0]
    ], 3)

run_solution([
        [0, -1, -1, -1, -1], 
        [9, 0, 2, 2, -1], 
        [9, 3, 0, 2, -1], 
        [9, 3, 2, 0, -1], 
        [9, 3, 2, 2, 0]
    ], 1)
'''
run_solution([
        [ 0,  0, 1, 1], 
        [ 1, 0, -1, 1],
        [ 9,  1, 0, 1],
        [ 9,  9, 9, 9]            
    ], 1)

run_solution([
        [ 0, -3,  9,  9], 
        [ 9,  0,  -1,  9],
        [ 1,  -1,  0,  1],         
        [ 9,  9,  9,  9]
    ], -1)