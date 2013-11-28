#!/usr/bin/python
def pulverizer(a, b): # a > b
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b != 0:
    	q, r = a//b, a%b
    	x, y = x2 - q*x1, y2 - q*y1
    	a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y
    return a, x2, y2

def modularInverse(e, phi):
    g, x, y = pulverizer(e, phi)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % phi