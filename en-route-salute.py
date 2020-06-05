'''
En Route Salute
===============

Commander Lambda loves efficiency and hates anything that wastes time. She's a busy lamb, after all! 
She generously rewards henchmen who identify sources of inefficiency and come up with ways to remove them. 
You've spotted one such source, and you think solving it will help you build the reputation you need to get promoted.

Every time the Commander's employees pass each other in the hall, each of them must stop and salute each other - 
one at a time - before resuming their path. A salute is five seconds long, so each exchange of 
salutes takes a full ten seconds (Commander Lambda's salute is a bit, er, involved). 
You think that by removing the salute requirement, you could save several collective hours of 
employee time per day. But first, you need to show her how bad the problem really is.

Write a program that counts how many salutes are exchanged during a typical walk along a hallway. 
The hall is represented by a string. For example:
"--->-><-><-->-"

Each hallway string will contain three different types of characters: '>', an employee walking to 
the right; '<', an employee walking to the left; and '-', an empty space. Every employee walks at 
the same speed either to right or to the left, according to their direction. Whenever two employees 
cross, each of them salutes the other. They then continue walking until they reach the end, finally 
leaving the hallway. In the above example, they salute 10 times.

Write a function solution(s) which takes a string representing employees walking along a hallway and 
returns the number of times the employees will salute. s will contain at least 1 and at most 100 
characters, each one of -, >, or <.

-- Python cases --
Input:
solution.solution(">----<")
Output:
    2

Input:
solution.solution("<<>><")
Output:
    4

'''

def solution(s):
    # Using a simulation technique
    n = 0
    N = len(s)
    S = "-" * N
    
    turns = 0
    while (s != S) & (turns<100):
        turns+=1
        # m = count_meetings(s)        
        print(f"Turn: {turns}, corridor: {s}, meetings: {n}")

        # Handle right movers
        for c,i in zip(s[::-1],range(N-1,0-1,-1)):
            if c==">":
                s,n = move_right(s,n,i)
            if c=="x":
                s,n = move_right(s,n,i)
                s = replace_index(s,i,"<")
        
        # Handle left movers
        for c,i in zip(s,range(0,N)):
            if c=="<":
                s,n = move_left(s,n,i)
            if c=="x":
                s,n = move_left(s,n,i)
                s = replace_index(s,i,">")

    return n * 2
                

def move_right( s, n, i ):
    a = s[i]
    s = replace_index(s,i,"-")
    if i == len(s)-1:
        return s,n
    
    b = s[i+1]
    if b == "<":
        s = replace_index(s,i+1,"x")
        n+=1 
    else:
        s = replace_index(s,i+1,">")
    return s,n

def move_left( s, n, i ):
    a = s[i]
    s = replace_index(s,i,"-")
    if i == 0:
        return s,n
    
    b = s[i-1]
    if b == ">":
        s = replace_index(s,i-1,"x")
        n+=1
    else:
        s = replace_index(s,i-1,"<")
    return s,n

def replace_index(s,i,c):
    s = s[:i] + c + s[i + 1:]
    return s


print(solution("--->-><-><-->-"))
# Expected 10

print(solution(">----<"))
# Expected 2

print(solution("<<>><"))
# Expected 4