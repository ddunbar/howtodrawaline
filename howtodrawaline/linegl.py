from __future__ import division
from math import fabs,fmod

def line2d(x0, y0, x1, y1):
    if abs(x0 - x1) < abs(y0 - y1):
        for x,y in line2d_norm(y0, x0, y1, x1):
            yield y,x
    else:
        for x,y in line2d_norm(x0, y0, x1, y1):
            yield x,y

def line2d_norm(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    adx = fabs(dx)
    ady = fabs(dy)
    sx = int(x0)
    sy = int(y0)
    ex = int(x1)

    pt0_in_diamond = (fabs(fmod(x0,1.0)-0.5) + fabs(fmod(y0,1.0)-0.5)) < 0.5
    pt1_in_diamond = (fabs(fmod(x1,1.0)-0.5) + fabs(fmod(y1,1.0)-0.5)) < 0.5

    if dx >= 0.0:
        pt0_interior = fmod(x0,1.0) > 0.5
        pt1_exterior = fmod(x1,1.0) > 0.5
        xinc = 1
        d_1 = ady * (sx+1.5-x0)
    else:
        pt0_interior= fmod(x0,1.0) < 0.5
        pt1_exterior= fmod(x1,1.0) < 0.5
        xinc = -1
        d_1 = -ady * (sx-0.5-x0)

    if dy >= 0.0:
        yinc = 1
        d_2 = -adx*(sy+1.0-y0)
    else:
        yinc = -1
        d_2 = adx*(sy-y0)

    D = d_1 + d_2
    dNE = (ady - adx)
    dN = (ady)

    skipPxl = 0
    if pt0_interior:
        if not pt0_in_diamond:
            skipPxl = 1
    else:
        if (D-dN) >= 0.0:
            sy += yinc
            D += dNE-dN

    y = sy
    x = sx
    while x != ex:
        if skipPxl:
            skipPxl = 0
        else:
            yield (x, y)
        if D >= 0.0:
            y += yinc
            D += dNE
        else:
            D += dN
        x += xinc

    if pt1_exterior and not pt1_in_diamond:
        yield (ex, y)
