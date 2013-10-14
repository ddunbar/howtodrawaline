import sys
import time
import math

from OpenGL.GLUT import *
from OpenGL.GL import *

import pylive.window

import line
reload(line)
import line

def draw_string(x, y, string):
    glRasterPos2f(x, y)
    for c in string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))

class HowToDrawALineProxy(pylive.window.WindowProxy):
    def __init__(self, window, last_proxy=None):
        super(HowToDrawALineProxy, self).__init__(window)
        self.frame = 0
        self.animate = False
        self.use_gl = False

        # Recover state on a reload.
        if last_proxy is not None:
            self.frame = last_proxy.frame
            self.animate = last_proxy.animate

    def on_idle(self):
        if self.animate:
            self.window.update()

    def on_special(self, key, x, y):
        if key == ord('a'):
            self.animate = not self.animate
        elif key == ord('g'):
            self.use_gl = not self.use_gl
            self.window.update()

    def on_draw(self):
        # Handle animation.
        if self.animate:
            self.frame += 1

        # Draw a silly progress bar across the bottom.
        glColor3f(.9, .9, .9)
        glRectf(0, 0, (self.frame/10. % self.window.width), 12)
        glColor3f(.8, .8, .8)
        draw_string(1, 1, "time: %.2fs" % (time.time(),))

        # Enable several displays of our line drawing algorithm. Displays are
        # organized in a 3 x 4 grid.
        padding = 10
        bottom_padding = 50
        rows = 4
        columns = 3
        cell_width = (self.window.width - 2*padding) // columns - padding
        cell_height = (self.window.height - 2*padding -
                       bottom_padding) // rows - padding
        
        glTranslatef(.375, .375, 0)
        for column in range(columns):
            for row in range(rows):
                x = padding + column * (cell_width + padding)
                y = bottom_padding + padding + row * (cell_height + padding)
                glColor3f(0, 0, 0)
                glBegin(GL_LINE_LOOP)
                glVertex2f(x, y)
                glVertex2f(x + cell_width, y)
                glVertex2f(x + cell_width, y + cell_height)
                glVertex2f(x, y + cell_height)
                glEnd()

                if (column, row) == (0, 3):
                    display = self.display_simple_lines
                else:
                    display = None
                if display is not None:
                    display(x, y, cell_width, cell_height)

    def display_simple_lines(self, x, y, w, h):
        # Display lines at 9 different orientations.
        rows = 3
        columns = 3
        glColor3f(0, 0, 0)
        glBegin(GL_LINES if self.use_gl else GL_POINTS)
        l = min(float(w)/columns, float(h)/rows) * .8
        for i in range(columns):
            for j in range(rows):
                t = (i*rows + j) / float(rows * columns)
                r = 2*math.pi * t
                cx = (i + .5)*w/columns
                cy = (j + .5)*h/rows
                x0 = x + int(cx - math.cos(r)*l*.5)
                y0 = y + int(cy - math.sin(r)*l*.5)
                x1 = x + int(cx + math.cos(r)*l*.5)
                y1 = y + int(cy + math.sin(r)*l*.5)
                if self.use_gl:
                    glVertex2f(x0, y0)
                    glVertex2f(x1, y1)
                else:
                    for pt in line.line2d(x0, y0, x1, y1):
                        glVertex2f(pt[0], pt[1])
        glEnd()

def register_pylive(window, last_proxy=None):
    if last_proxy is not None:
        print >>sys.stderr, "reloading module at %.2fs" % (time.time(),)
    else:
        print >>sys.stderr, "loading module initially %.2fs" % (time.time(),)

    # Create our window proxy.
    return HowToDrawALineProxy(window, last_proxy)
