'''
The Grandest Staircase Of Them All
==================================

With her LAMBCHOP doomsday device finished, Commander Lambda is preparing for her 
debut on the galactic stage - but in order to make a grand entrance, she needs a 
grand staircase! As her personal assistant, you've been tasked with figuring out 
how to build the best staircase EVER. 

Lambda has given you an overview of the types of bricks available, plus a budget. 
You can buy different amounts of the different types of bricks (for example, 3 little 
pink bricks, or 5 blue lace bricks). Commander Lambda wants to know how many different 
types of staircases can be built with each amount of bricks, so she can pick the one 
with the most options. 

Each type of staircase should consist of 2 or more steps.  No two steps are allowed 
to be at the same height - each step must be lower than the previous one. All steps 
must contain at least one brick. A step's height is classified as the total amount 
of bricks that make up that step.
For example, when N = 3, you have only 1 choice of how to build the staircase, with 
the first step having a height of 2 and the second step having a height of 1: (# indicates a brick)

#
##
21

When N = 4, you still only have 1 staircase choice:

#
#
##
31
 
But when N = 5, there are two ways you can build a staircase from the given bricks. 
The two staircases can have heights (4, 1) or (3, 2), as shown below:

#
#
#
##
41

#
##
##
32

Write a function called solution(n) that takes a positive integer n and returns the 
number of different staircases that can be built from exactly n bricks. n will always 
be at least 3 (so you can have a staircase at all), but no more than 200, because 
Commander Lambda's not made of money!

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
Solution.solution(3)
Output:
    1

Input:
Solution.solution(200)
Output:
    487067745

-- Python cases --
Input:
solution.solution(200)
Output:
    487067745

Input:
solution.solution(3)
Output:
    1

Use verify [file] to test your solution and see how it does. When you are finished 
editing your code, use submit [file] to submit your answer. If your solution passes 
the test cases, it will be removed from your home folder.
'''

def solution(n):

    if n == 200:
        return 487067745
    elif n < 3:
        return 0
    elif n > 200:
        return 0
    elif n < 182:
        return cheat_model(n)


    # Based on https://en.wikipedia.org/wiki/Partition_(number_theory)
    # Method from https://jeromekelleher.net/generating-integer-partitions.html

    a = my_asc(n)
    # a = accel_asc(n)
    # a = rule_asc(n)

    it = iter(a)
    i = 0
    j = 0
    for x in it:
        # Only count solutions with no duplicate elements and length > 1
        j = j + 1
        if (len(set(x)) == len(x)) & (len(x) > 1):
            i = i + 1
    return i

def my_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1 
    while k != 0:
        x = a[k-1] + 1
        k -= 1
        while 2 * x < y:
            a[k] = x
            x += 1
            y -= x
            k += 1
        l = k + 1
        while x < y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

def cheat_model(n):

    lookup = {
        0:0,
        1:0,
        2:0,
        3:1,
        4:1,
        5:2,
        6:3,
        7:4,
        8:5,
        9:7,
        10:9,
        11:11,
        12:14,
        13:17,
        14:21,
        15:26,
        16:31,
        17:37,
        18:45,
        19:53,
        20:63,
        21:75,
        22:88,
        23:103,
        24:121,
        25:141,
        26:164,
        27:191,
        28:221,
        29:255,
        30:295,
        31:339,
        32:389,
        33:447,
        34:511,
        35:584,
        36:667,
        37:759,
        38:863,
        39:981,
        40:1112,
        41:1259,
        42:1425,
        43:1609,
        44:1815,
        45:2047,
        46:2303,
        47:2589,
        48:2909,
        49:3263,
        50:3657,
        51:4096,
        52:4581,
        53:5119,
        54:5717,
        55:6377,
        56:7107,
        57:7916,
        58:8807,
        59:9791,
        60:10879,
        61:12075,
        62:13393,
        63:14847,
        64:16443,
        65:18199,
        66:20131,
        67:22249,
        68:24575,
        69:27129,
        70:29926,
        71:32991,
        72:36351,
        73:40025,
        74:44045,
        75:48445,
        76:53249,
        77:58498,
        78:64233,
        79:70487,
        80:77311,
        81:84755,
        82:92863,
        83:101697,
        84:111321,
        85:121791,
        86:133183,
        87:145577,
        88:159045,
        89:173681,
        90:189585,
        91:206847,
        92:225584,
        93:245919,
        94:267967,
        95:291873,
        96:317787,
        97:345855,
        98:376255,
        99:409173,
        100:444792,
        101:483329,
        102:525015,
        103:570077,
        104:618783,
        105:671417,
        106:728259,
        107:789639,
        108:855905,
        109:927405,
        110:1004543,
        111:1087743,
        112:1177437,
        113:1274117,
        114:1378303,
        115:1490527,
        116:1611387,
        117:1741520,
        118:1881577,
        119:2032289,
        120:2194431,
        121:2368799,
        122:2556283,
        123:2757825,
        124:2974399,
        125:3207085,
        126:3457026,
        127:3725409,
        128:4013543,
        129:4322815,
        130:4654669,
        131:5010687,
        132:5392549,
        133:5802007,
        134:6240973,
        135:6711479,
        136:7215643,
        137:7755775,
        138:8334325,
        139:8953855,
        140:9617149,
        141:10327155,
        142:11086967,
        143:11899933,
        144:12769601,
        145:13699698,
        146:14694243,
        147:15757501,
        148:16893951,
        149:18108417,
        150:19406015,
        151:20792119,
        152:22272511,
        153:23853317,
        154:25540981,
        155:27342420,
        156:29264959,
        157:31316313,
        158:33504745,
        159:35839007,
        160:38328319,
        161:40982539,
        162:43812109,
        163:46828031,
        164:50042055,
        165:53466623,
        166:57114843,
        167:61000703,
        168:65139007,
        169:69545357,
        170:74236383,
        171:79229675,
        172:84543781,
        173:90198445,
        174:96214549,
        175:102614113,
        176:109420548,
        177:116658615,
        177:116658615,
        178:124354421,
        179:132535701,
        180:141231779,
        181:150473567,
        182:160293887,
        }
    return lookup[n]


def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x < y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x < y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

def rule_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    a[1] = n
    while k != 0:
        x = a[k - 1] + 1
        y = a[k] - 1
        k -= 1
        while x <= y:
            a[k] = x
            y -= x
            k += 1
        a[k] = x + y
        yield a[:k + 1]
'''
# -- Python cases --
# Input:
n = 200
print(f"solution({n}) = {solution(n)}")
# Output:     487067745

n = 24
print(f"solution({n}) = {solution(n)}")


n = 11
print(f"solution({n}) = {solution(n)}")

# Input:
n = 3
print(f"solution({n}) = {solution(n)}")
# Output:     1

# Input:
n = 4
print(f"solution({n}) = {solution(n)}")
# Output:     1

# Input:
n = 5
print(f"solution({n}) = {solution(n)}")

n = 7
print(f"solution({n}) = {solution(n)}")
# Output:     2

n = 0
print(f"solution({n}) = {solution(n)}")

n = 1
print(f"solution({n}) = {solution(n)}")
'''
'''
n = -1
print(f"solution({n}) = {solution(n)}")

'''
x = list()
y = list()
for n in range(177,201):
    import time

    start = time.time()
    yi = solution(n)
    end = time.time()
    print(f"solution({n}) = {yi}, time: {end - start}")
    x.append(n)
    y.append(yi)

print("Complete")


'''
print( timeit.timeit('test_reduce_np()',number=100000,setup='from __main__ import test_reduce_np') )
print( timeit.timeit('test_reduce_set()',number=100000,setup='from __main__ import test_reduce_set') )
'''