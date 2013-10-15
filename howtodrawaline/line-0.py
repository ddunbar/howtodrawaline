def line2d(x0, y0, x1, y1):
    N = 50
    for i in range(N):
        t = float(i) / N
        p_x = x0 + (x1 - x0) * t
        p_y = y0 + (y1 - y0) * t
        yield (p_x, p_y)
