from __future__ import division
from math import fabs, fmod, floor

def safediv(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return 0.

def ipart(x):
    return int(floor(x))

def round(x):
    return int(ipart(x + .5))

def fpart(x):
    return fmod(x, 1.0)

def rfpart(x):
    return 1.0 - fpart(x)
 
def aline2d(x0, y0, x1, y1): 
    """Wu antialiased line algorithm"""

    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0,y0 = y0,x0
        x1,y1 = y1,x1

    if x0 > x1:
        x0,x1 = x1,x0
        y0,y1 = y1,y0
 
    dx = x1 - x0
    dy = y1 - y0
    gradient = safediv(dy, dx)
 
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend
    ypxl1 = ipart(yend)
    if steep:
        yield (ypxl1,   xpxl1, rfpart(yend) * xgap)
        yield (ypxl1+1, xpxl1,  fpart(yend) * xgap)
    else:
        yield (xpxl1, ypxl1  , rfpart(yend) * xgap)
        yield (xpxl1, ypxl1+1,  fpart(yend) * xgap)
    intery = yend + gradient
 
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend
    ypxl2 = ipart(yend)
    if steep:
        yield (ypxl2  , xpxl2, rfpart(yend) * xgap)
        yield (ypxl2+1, xpxl2,  fpart(yend) * xgap)
    else:
        yield (xpxl2, ypxl2,  rfpart(yend) * xgap)
        yield (xpxl2, ypxl2+1, fpart(yend) * xgap)
 
    for x in range(xpxl1 + 1, xpxl2 - 1):
        if steep:
            yield (ipart(intery)  , x, rfpart(intery))
            yield (ipart(intery)+1, x,  fpart(intery))
        else:
            yield (x, ipart (intery),  rfpart(intery))
            yield (x, ipart (intery)+1, fpart(intery))
        intery = intery + gradient
