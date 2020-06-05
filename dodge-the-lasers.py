'''
Dodge the Lasers!
=================

Oh no! You've managed to escape Commander Lambdas collapsing space station 
in an escape pod with the rescued bunny prisoners - but Commander Lambda 
isnt about to let you get away that easily. She's sent her elite fighter 
pilot squadron after you - and they've opened fire!

Fortunately, you know something important about the ships trying to shoot 
you down. Back when you were still Commander Lambdas assistant, she asked 
you to help program the aiming mechanisms for the starfighters. They undergo 
rigorous testing procedures, but you were still able to slip in a subtle bug. 
The software works as a time step simulation: if it is tracking a target 
that is accelerating away at 45 degrees, the software will consider the 
targets acceleration to be equal to the square root of 2, adding the 
calculated result to the targets end velocity at each timestep. However, 
thanks to your bug, instead of storing the result with proper precision, 
it will be truncated to an integer before adding the new velocity to your 
current position.  This means that instead of having your correct position, 
the targeting software will erringly report your position as 
    sum(i=1..n, floor(i*sqrt(2))) 
- not far enough off to fail Commander Lambdas testing, 
but enough that it might just save your life.

If you can quickly calculate the target of the starfighters' laser beams 
to know how far off they'll be, you can trick them into shooting an asteroid, 
releasing dust, and concealing the rest of your escape.  Write a function 
solution(str_n) which, given the string representation of an integer n, 
returns the sum of 
    (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. 
That is, for every number i in the range 1 to n, it adds up all of the integer portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".

str_n will be a positive integer between 1 and 10^100, inclusive. Since n 
can be very large (up to 101 digits!), using just sqrt(2) and a loop won't 
work. Sometimes, it's easier to take a step back and concentrate not on 
what you have in front of you, but on what you don't.

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
Solution.solution('77')
Output:
    4208

Input:
Solution.solution('5')
Output:
    19

-- Python cases --
Input:
solution.solution('77')
Output:
    4208

Input:
solution.solution('5')
Output:
    19

'''
import math
def solution(str_n):
    str_n
    n = int(str_n)
    v = 0
    for i in range(n, 0, -1):
        dv,j = get_sqrt_2_time_f(100)
        v = v + math.floor(dv)
    return str(int(v))


def get_sqrt_2_time_f( f ):
    number = 2
    a = float(number) 
    previous = a - 1
    n = 1
    number_iters = 500
    while (int(number*10**f) - int(previous*10**f) != 0)  & (n<number_iters):
        previous = number
        number = 0.5 * (number + a / number) # update
        #print("------------------------------------------------")
        #print(int(number*10**f))
        #print(int(previous*10**f))
        n = n + 1
    return number, n

def newton_method(number, number_iters = 500, ndigits = 8):
    a = float(number) # number to get square root of
    previous = a - 1
    n = 1    
    while (round(a,ndigits) != round(previous,ndigits)) & (n<number_iters):
        previous = number
        number = 0.5 * (number + a / number) # update
        n = n + 1
    return number, n



import time
def run_solution(str_n,expected=None):
    print( "Running solution str_n={}".format(str_n) )
    start = time.time()
    ans = solution(str_n)
    end = time.time()
    print( "Answer={}, Expected={}, time={})".format(ans,expected,end - start) )


# ans,n = newton_method(2,ndigits=100)
#ans,n = get_sqrt_2_time_f(100)
#print("Iterations: {}, answer: {}".format(n,ans))
# Output: 1.41421356237

#-- Python cases --
#Input:
#solution.solution('77')
#Output:
#    4208
# run_solution('77',expected=4208)

#Input:
#solution.solution('5')
#Output:
#    19
run_solution('5',expected=19)

#run_solution('0')

# run_solution('741817')

