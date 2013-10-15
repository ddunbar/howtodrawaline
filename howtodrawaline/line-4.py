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

    i_dx = int(x1 - x0)
    i_dy = int(y1 - y0)
    abs_i_dx = abs(i_dx)
    abs_i_dy = abs(i_dy)
    inc = 1 if i_dx >= 0 else -1

    m = i_dy

    # Determine if we are moving up or down in Y.
    y_up = y1 >= y0
    y_inc = 1 if y_up else -1

    error = 0 * i_dx
    delta_error = abs_i_dy

    i_x = int(x0)
    i_y = int(y0)
    i_x1 = int(x1)
    for i in range(abs_i_dx):
        yield (i_x, i_y)

        error = error + delta_error
        if error / abs_i_dx >= .5:
            i_y += y_inc
            error = error - abs_i_dx

        i_x += inc
