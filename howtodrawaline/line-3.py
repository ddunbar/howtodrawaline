from __future__ import division

def safediv(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return 0.

def line2d(x0, y0, x1, y1):
    if abs(x0 - x1) < abs(y0 - y1):
        for x,y in line2d_norm(y0, x0, y1, x1):
            yield y,x
    else:
        for x,y in line2d_norm(x0, y0, x1, y1):
            yield x,y

def line2d_norm(x0, y0, x1, y1):
    """Bresenham's Algorithm"""
    assert abs(x0 - x1) >= abs(y0 - y1)

    inc = 1 if x1 > x0 else -1

    m = safediv(y1 - y0, x1 - x0)

    # Determine if we are moving up or down in Y.
    y_up = y1 >= y0
    y_inc = 1 if y_up else -1

    error = 0.
    delta_error = abs(m)

    i_x = int(x0)
    i_y = int(y0)
    i_x1 = int(x1)
    while i_x != i_x1:
        yield (i_x, i_y)

        error = error + delta_error
        if error >= .5:
            i_y += y_inc
            error = error - 1

        i_x += inc
