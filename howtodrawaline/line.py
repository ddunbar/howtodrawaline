from __future__ import division
import vec2

def safediv(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return 0.

def line2d(x0, y0, x1, y1):
    N = 50
    for i in range(N):
        t = float(i) / N
        p_x = x0 + (x1 - x0) * t
        p_y = y0 + (y1 - y0) * t
        yield (p_x, p_y)

line2d_norm = line2d

def line2d(x0, y0, x1, y1):
    if abs(x0 - x1) < abs(y0 - y1):
        for x,y in line2d_norm(y0, x0, y1, x1):
            yield y,x
    else:
        for x,y in line2d_norm(x0, y0, x1, y1):
            yield x,y

def line2d_norm(x0, y0, x1, y1):
    assert abs(x0 - x1) >= abs(y0 - y1)

    inc = 1 if x1 > x0 else -1

    m = safediv(y1 - y0, x1 - x0)
    b = y0 - m*x0

    i_x = int(x0)
    i_x1 = int(x1)
    while i_x != i_x1:
        y = m*i_x + b
        yield (i_x, int(y))
        i_x += inc

def line2d_norm(x0, y0, x1, y1):
    assert abs(x0 - x1) >= abs(y0 - y1)

    inc = 1 if x1 > x0 else -1

    m = safediv(y1 - y0, x1 - x0)
    b = y0 - m*x0

    i_x = int(x0)
    i_x1 = int(x1)
    while True:
        y = m*i_x + b
        yield (i_x, int(y))
        if i_x == i_x1:
            break
        i_x += inc

def pt_in_pixeldiamond(pt):
	diamondco = vec2.modN(pt,1.0)
	return abs(diamondco[0]-0.5)+abs(diamondco[1]-0.5)<0.5

def ogl_line2d_2(pt0, pt1, set_last_line= True):
	dx,dy= vec2.sub(pt1,pt0)
	adx,ady= abs(dx),abs(dy)

	if adx<ady:
		return [(y,x) for (x,y) in ogl_line2d_2((pt0[1],pt0[0]),(pt1[1],pt1[0]))]
	
	def raster(pt0,pt1):
		dx,dy= vec2.sub(pt1,pt0)
		adx,ady= abs(dx),abs(dy)

		try:
			m= dy/dx
		except ZeroDivisionError:
			return []

		b= pt0[1]-m*pt0[0]

		pts= []
		x= int(pt0[0])
		y= int(pt0[1])
		if (pt0[0]%1.0)>0.5:
			if pt_in_pixeldiamond(pt0):
				pts.append( (x,y) )
		else:
			i_y= m*(x+0.5)+b
			if dy*(x+0.5) - dx*(y+1) + b*dx>=0.0:
				y+= 1
			pts.append( (x,y) )

		while x<int(pt1[0])-1:
			if dy*(x+1.5) - adx*(y+1) + b*adx>=0.0:
				x+= 1
				y+= 1
			else:
				x+= 1
			pts.append( (x,y) )

		if (pt1[0]%1.0)>0.5:
			if not pt_in_pixeldiamond(pt1):
					pts.append( vec2.toint(pt1) )

		return pts

	def mirror_about(axis, val):
		return axis + (axis-val)
	
	xaxis= int(pt0[0])
	yaxis= int(pt1[1])
	flipx= pt1[0]<pt0[0]
	flipy= pt1[1]<pt0[1]
	if flipx:
		pt0,pt1= (	(mirror_about(xaxis+0.5,pt0[0]),pt0[1]),
					(mirror_about(xaxis+0.5,pt1[0]),pt1[1]))
	if flipy:
		pt0,pt1= (	(pt0[0],mirror_about(yaxis+0.5,pt0[1])),
					(pt1[0],mirror_about(yaxis+0.5,pt1[1])))
	pts= raster(pt0,pt1)

	if flipx:
		pts= [(mirror_about(xaxis,x),y) for x,y in pts]
	if flipy:
		pts= [(x,mirror_about(yaxis,y)) for x,y in pts]
	
	return pts

def line2d_x(x0, y0, x1, y1):
    for pt in ogl_line2d_2((x0, y0), (x1, y1)):
        yield pt
