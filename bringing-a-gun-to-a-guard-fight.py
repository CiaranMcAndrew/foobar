'''
Bringing a Gun to a Guard Fight
===============================

Uh-oh - you've been cornered by one of Commander Lambdas elite guards! 
Fortunately, you grabbed a beam weapon from an abandoned guard post while 
you were running through the station, so you have a chance to fight your 
way out. But the beam weapon is potentially dangerous to you as well as 
to the elite guard: its beams reflect off walls, meaning you'll have to 
be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before 
becoming too weak to cause damage. You also know that if a beam hits a 
corner, it will bounce back in exactly the same direction. And of course, 
if the beam hits either you or the guard, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, guard_position, 
distance) that gives an array of 2 integers of the width and height of 
the room, an array of 2 integers of your x and y coordinates in the room, 
an array of 2 integers of the guard's x and y coordinates in the room, 
and returns an integer of the number of distinct directions that you can 
fire to hit the elite guard, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. 
You and the elite guard are both positioned on the integer lattice at 
different distinct positions (x, y) inside the room such that 
        [0 < x < x_dim, 0 < y < y_dim]. 
Finally, the maximum distance that the beam can travel before becoming 
harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite guard were positioned in a room with 
dimensions [3, 2], your_position [1, 1], guard_position [2, 1], and a maximum 
shot distance of 4, you could shoot in seven different directions to hit the
elite guard (given as vector bearings from your location): 
        [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. 
As specific examples, the shot at bearing [1, 0] is the straight line horizontal 
shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and 
then the bottom wall before hitting the elite guard with a total shot distance 
of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before 
hitting the elite guard with a total shot distance of sqrt(5).

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
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9
'''
import numpy as np
import math
import copy

def solution(dimensions, your_position, guard_position, distance):

    xgrid = np.array([0,dimensions[0]])
    ygrid = np.array([0,dimensions[1]])
    
    # calculate how much to grow the grid
    X = np.ptp(xgrid)
    Y = np.ptp(ygrid)

    nx = int(np.ceil( distance / (2*X) ))
    ny = int(np.ceil( distance / (2*Y) ))

    actors = list()
    actors.append(Actor('you',your_position,isprimary=True))
    actors.append(Actor('guard',guard_position,isprimary=True))

    # Offset to primary player
    P = np.array(your_position)
    x = P[0]
    y = P[1]
    xgrid = xgrid - x
    ygrid = ygrid - y
    for a in actors:
        a.set_position(x = a.position[0] - x, y = a.position[1] - y)

    # Create mirror grid     
    while np.max(np.abs(xgrid)) < distance:
        new_actors = actors[:]
        
        # Horizontal        
        dx = xgrid[-1]
        x_new_r = -(xgrid - dx) + dx
        for a in new_actors:
            p = a.position[:]
            p[0] = -(p[0] - dx) + dx
            add_actor( actors, a.role, p, distance )
            # actors.append(Actor(a.role, p))

        dx = xgrid[0]
        x_new_l = -(xgrid - dx) + dx
        for a in new_actors:
            p = a.position[:]
            p[0] = -(p[0] - dx) + dx
            add_actor( actors, a.role, p, distance )
            # actors.append(Actor(a.role, p))

        x_new = np.hstack([x_new_l,xgrid,x_new_r])
        x_new = np.unique(x_new)
        xgrid = x_new

    # Vertical
    while np.max(np.abs(ygrid)) < distance:
        new_actors = actors[:]
   
        dy = ygrid[-1]
        y_new_u = -(ygrid - dy) + dy
        for a in new_actors:
            p = a.position[:]
            p[1] = -(p[1] - dy) + dy
            add_actor( actors, a.role, p, distance )
            #actors.append(Actor(a.role, p))

        dy = ygrid[0]
        y_new_d = -(ygrid - dy) + dy
        for a in new_actors:
            p = a.position[:]
            p[1] = -(p[1] - dy) + dy
            add_actor( actors, a.role, p, distance )
            # actors.append(Actor(a.role, p))

        y_new = np.hstack([y_new_d,ygrid,y_new_u])
        y_new = np.unique(y_new)
        ygrid = y_new
    
    
    # Remove actors who are too far from origin
    actors.sort(key=lambda x: x.distance)
    actors = [a for a in actors if a.distance <= distance] # This made 9 work but 5 fail

    # Find first of each angle
    C,ix = np.unique(np.array([a.angle for a in actors]),return_index=True)
    actors = np.array(actors)[ix]
    actors = [a for a in actors if a.role=="guard"]

    return len(actors)


def add_actor( actors, role, position, max_distance ):
    a = Actor(role, position)
    if a.distance <= max_distance:        
       actors.append(a)
    return actors

class Actor():

    def __init__(self,role,position,isprimary=False):
        self.role = role
        self.set_position(x=position[0],y=position[1])
        self.isprimary = isprimary
        self.blocked = False

    def set_position(self,x=None,y=None):
        if x != None:
            self.x = float(x)
        if y != None:
            self.y = float(y)

        self.distance = math.sqrt(self.x**2 + self.y**2)
        if (self.x == 0) & (self.y == 0):
            self.angle = 1e6
        else:
            self.angle = math.atan2(self.y,self.x)
        
        m = max( [np.abs(self.x), np.abs(self.y)] )
        self.vector = self.position / m

    def move_position(self,dx=0,dy=0):
        self.set_position(x=self.x+dx,y=self.y+dy)

    def set_blocked(self,tf=True):
        self.blocked = tf

    @property
    def position(self):
        return np.array([self.x,self.y])

import matplotlib.pyplot as plt
import timeit
def plot_solution(xgrid,ygrid,actors=[],vectors=[]):
    
    # Visualise
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    ax.grid()

    # Draw grid
    linecolor = [0.5,0.5,0.5,1.0]
    X = [np.min(xgrid), np.max(xgrid)]
    Y = [np.min(ygrid), np.max(ygrid)]

    for xi in xgrid:
        x = [xi,xi]
        y = Y
        line, = ax.plot(x, y, "-", color=linecolor, lw=2)
    
    for yi in ygrid:
        x = X
        y = [yi,yi]
        line, = ax.plot(x, y, "-", color=linecolor, lw=2)

    # Draw actors
    for a in actors:
        x = a.position[0]
        y = a.position[1]
        if a.role == 'guard':
            color='red'
            m = 'x'
        else:
            color='blue'
            if a.isprimary:
                color='gold'
            m = '*'
            
        marker, = ax.plot(x, y, m, color=color, lw=2)
    
    # Draw vectors
    for v in vectors:
        x = [0,v[0]]
        y = [0,v[1]]
        line, = ax.plot(x, y, '-', color='green', lw=1)
    
    plt.show()

import time
def run_solution(dimensions, your_position, guard_position, distance):
    print( "Running solution dimensions={}, your_position={}, guard_position={}, distance={}".format(dimensions, your_position, guard_position, distance) )
    start = time.time()
    bearings = solution(dimensions, your_position, guard_position, distance)
    end = time.time()
    print( "Answer={}, time={})".format(bearings,end - start) )

'''
# -- Python cases --
# Input:
run_solution([3,2], [1,1], [2,1], 4)
# Output:
#     7

# Input:
run_solution([300,275], [150,150], [185,100], 500)
# Output:
#     9

run_solution([300,275], [150,150], [185,100], 1000)

run_solution([100,4], [5,2], [85,2], 100)

run_solution([100,4], [5,2], [85,2], 3)

run_solution([3,2], [1,1], [2,1], 4)
'''
# Try a small repeated grid
# run_solution([3,3], [1,1], [2,2], 1000)

for n in range(1,10):
    run_solution([3,3], [1,1], [2,2], 25 * n)



