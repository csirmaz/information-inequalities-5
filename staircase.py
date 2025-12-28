

"""
This script generates extremal staircases

A staircase is described by an array [0 .. g] which is decreasing,
but never drops more than 1, and ends with a zero.

In the output, staircases are stored as 0-1 sequences of length g-1, denoting
if the next value is the same (0) or one less (1). The last character
is + if the corresponding triplet is also extremal in the next generation,
and is - if it is extremal in this generation, but not in the next one.

We maintain a pool of staircases which generates the
previous generation. To get elements of the next
generation, follow these steps:
    1) if the array is shorter than the generation, pass (it is final)
    2) the array has length equal to the generation.
    2a) add a zero to the end. Check for NPN and PNP. If none, then
           add this staircase.
    2b) increase all elements by one and add a zero. This is a new
           array (no need to check)
    2c) check if this array becomes superseded. If not, add.
"""

import sys

# Generate up to this generation
maxgen = 60

# array of downward set descriptions for each generation
RECTANGLES = {
   0: [[0]] # generation 0 has a single staircase: [0] (bottom left corner)
}


def die(msg):
    sys.stderr.write(f"ERROR: {msg}\n")
    exit(1)
    

def log(msg):
    sys.stderr.write(f"{msg}\n")
   

def isgt(x, y):
    """store fractions as pairs, this compares two fractions (x0/x1 > y0/y1)"""
    return (x[0]*y[1] > y[0]*x[1])


#  Rectangle/staircase is stored as:
#   r[0 .. g]; r[g]=0; r[i+1]=r[i] || r[i+1]=r[i]-1
#
#   N(i): top element of column i can be deleted: i<g
#      (i==0 || r[i-1]==r[i]) && r[i]>r[i+1]
#       ==> j=r[i]
#   P(i): an element can be added to the top of column i: i<g
#      (i==0 || r[i-1]>r[i]) && r[i+1]==r[i]
#
# For the PNP test:
#  (i3,j3) is a P-point: either i3=g; j3=0 (point added)
#     or [ ...,1,0,0]; i3=g-1, j3=1;
#
#  superseded: (i3-i1)/(j1-j3) >= (i3-i2)/(j2-j3)
#     for some N point (i2,j2) and P point (i1,j1), i1<i2<i3
#
#  go backwards from i=i3-1 to zero
#   if N(i), take the minimum of (i3-i)/(j-j3)
#   if P(i), check min <=(i3-i)/(j-j3) if YES, superseded
#            if NOT, continue.
#
# For the NPN test: r[0 .. g]; r[g]=0 (we have added the last column)
#  r[g] is deleted (i3=g, j3=0) (N point)
#    N(i): the top element of column i can be deleted:
#       r[i]>r[i+1] && (i==0 || r[i-1]==r[i]); j=r[i]
#    P(i): an element can be added to the top of column i:
#        (i==0 || r[i-1]>r[i]) && r[i+1]==r[i]; 
#
#  N(i1,j1), P(i2,j2), N(g,0) is superseded iff
#    (i3-i1)/(j1-j3) <= (i3-i2)/(j2-j3)
#
#  go backwards from i=g-2 (g-1 cannot be taken as P) If P(i): compute
#  the maximum of (g-i)/j. If N(i): check if there is a maximum, 
#  and check max >= (g-i)/j. If yes, superseded, if not, continue.


def pnp(r, i3):
    """The PNP test. Return whether r is superseded. i3==g or g-1"""
    g = len(r) - 1
    if r[g] != 0:
        die("PNP: last element is not zero")
    if g <= 3:
        return False
   
    if i3 == g:
        j3 = 0
    elif i3 == g - 1:
        j3 = 1
        if r[g-1] != 0:
            die("PNP: internal error")
    else:
        die("PNP: unexpected i3")

    minv = [0, 0]
    was_n = False
   
    for idx in range(i3-1, -1, -1):
        if (idx == 0 or r[idx-1] == r[idx]) and r[idx] > r[idx+1]:
            if not was_n:
                was_n = True
                minv = [i3 - idx, r[idx] - j3]
            else:
                p = [i3 - idx, r[idx] - j3]
                if isgt(minv, p):
                    minv = p
               
        if was_n and (idx == 0 or r[idx-1] > r[idx]) and r[idx+1] == r[idx]:
            p = [i3 - idx, r[idx] + 1 - j3]
            if isgt(minv, p):
                pass  # OK
            else:
                return True
    return False


def npn(r):
    """The NPN test. Return whether r is superseded"""
    g = len(r) - 1
    if r[g] != 0:
        die("NPN: last element is not zero")
    if g <= 3:
        return False

    maxv = [0, 0]
    was_p = False
    for idx in range(g-2, -1, -1):
        if (idx == 0 or r[idx-1] > r[idx]) and r[idx+1] == r[idx]:
            if not was_p:
                was_p = True
                maxv = [g - idx, 1 + r[idx]]
            else:
                p = [g - idx, 1 + r[idx]]
                if isgt(p, maxv):
                    maxv = p
        if was_p and (idx == 0 or r[idx-1] == r[idx]) and r[idx] > r[idx+1]:
            p = [g - idx, r[idx]]
            if isgt(p, maxv):
                pass  # OK
            else:
                return True
    return False


splus = [0] * 100
sminus = [0] * 100


def handle(rect, typ):
    """Called on generated staircases (rect) and whether they survive (typ)"""
    m = len(rect)
    txt = ""
    idx = 1
    while idx < m:
        txt += "0" if rect[idx] == rect[idx-1] else "1"
        idx += 1
    if typ == "+":
        splus[m-1] += 1
        print(f"{txt}{typ}")
    else:
        sminus[m-1] += 1


def generatenext(genno):
    RECTANGLES[genno] = []
    for rect in RECTANGLES[genno-1]:
        if len(rect) != genno:
            die("rectangle/staircase has wrong dimensions")
            
        gen2 = [v+1 for v in rect] + [0]
        RECTANGLES[genno].append(gen2)
        
        gen1 = rect + [0]
        if npn(gen1):
            pass  # superseded
        elif pnp(gen1, genno-1):
            pass  # superseded
        else:
            RECTANGLES[genno].append(gen1)  # remains
            
        if pnp(gen1, genno):
            handle(rect, "-")  # not final, will be superseded
        else:
            handle(rect, "+")


for i in range(90):
    generatenext(i+1)
    log(f"Gen: {i+1} size={len(RECTANGLES[i])} plus={splus[i]} minus={sminus[i]} total={splus[i]+sminus[i]}")
log(f"Done, size={len(RECTANGLES[maxgen])}")
