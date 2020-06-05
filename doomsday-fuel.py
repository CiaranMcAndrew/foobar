'''
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of 
the exotic matter involved. It starts as raw ore, then during processing, 
begins randomly changing between forms, eventually reaching a stable form. 
There may be multiple stable forms that a sample could ultimately reach, not 
all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation 
efficiency by predicting the end state of a given ore sample. You have 
carefully studied the different structures that the ore can take and which 
transitions it undergoes. It appears that, while random, the probability of 
each structure transforming is fixed. That is, each time the ore is in 1 state, 
it has the same probabilities of entering the next state (which might be the 
same state).  You have recorded the observed transitions in a matrix. The 
others in the lab have hypothesized more exotic forms that the ore can become, 
but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints 
representing how many times that state has gone to the next state and return an 
array of ints for each terminal state giving the exact probabilities of each 
terminal state, represented as the numerator for each state, then the 
denominator for all of them at the end and in simplest form. The matrix is at 
most 10 by 10. It is guaranteed that no matter which state the ore is in, there 
is a path from that state to a terminal state. That is, the processing will 
always eventually end in a stable state. The ore starts in state 0. The 
denominator will fit within a signed 32-bit integer during the calculation, as 
long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

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
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
'''
import numpy as np

def solution(m):
    print("Calculating doomsday fuel decomposition")
    print(m)
    # Using https://brilliant.org/wiki/markov-chains/    

    # Get size
    N = len(m)

    if N == 1:
        ans = [1,1]
        print("Complete")
        print(ans)
        return ans

    # Find terminal states
    # and resolve probability matrix to common denominator
    terminal_states = np.zeros(N,dtype=int) == 1
    P = np.array(m,dtype='float64')
    d = np.zeros(N)
    
    for y in range(0,N):
        X = sum(m[y])
        d[y] = X
        if X == 0:
            terminal_states[y] = True
            X = 1
            P[y,y] = 1
        else:
            a = P[y] / X
            P[y] = a
    
    # Case when first state is terminal
    if P[0,0] == 1:
        T = np.zeros(N,dtype=int)[terminal_states]
        T[0] = 1
        ans = list(T)
        ans.append(1)
        print("Complete")
        print(ans)
        return ans

    # Reorder so absorbing states are at the end
    ix = np.argsort(terminal_states)
    P = P[ix]
    for y in range(0,N):
        P[y] = P[y][ix]
    terminal_states = terminal_states[ix]
    

    Is = P[terminal_states][:,terminal_states]
    R = P[terminal_states==False][:,terminal_states]
    Q = P[terminal_states==False][:,terminal_states==False]
    It = np.eye(Q.shape[0],dtype=int)
    N = np.linalg.inv(It-Q)
    B = np.dot(N,R)
    
    # Find common denominator - brute force approach
    d = 1
    T = np.array(B[0],dtype='float64')
    while not all(np.isclose(abs(T-np.round(T)),0,rtol=1e-30)):
        d = d + 1
        T = d * B[0]

    ans = list(np.array(np.hstack((np.round(T),d)),dtype=int))
    
    print("Complete")
    print(ans)
    return ans

'''
# Input:
solution(
    [
        [0, 1, 2, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 3, 4],         
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0]
    ])
# Output:
#     [7, 6, 8, 21]

# Input:
solution(
    [
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 3, 4], 
        [0, 2, 1, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0]
    ])
# Output:
#     [7, 6, 8, 21]
'''


# Input:
solution(
    [
        [0, 2, 1, 0, 0], 
        [0, 0, 0, 3, 4], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0]
    ])
# Output:
#     [7, 6, 8, 21]

solution(
    [
        [1]
    ])

# Input:
solution(
    [
        [0, 1, 0, 0, 0, 1], 
        [4, 0, 0, 3, 2, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0]
    ])
# Output:
#     [0, 3, 2, 9, 14]

solution( 
    [
        [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
        [0,0,0,0,0,0],  # s3 is terminal
        [0,0,0,0,0,0],  # s4 is terminal
        [0,0,0,0,0,0],  # s5 is terminal
    ])


m = [
        [0, 1,0, 1, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
solution( m )
