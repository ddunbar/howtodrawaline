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
        self.last_frame_time = None

        # Bind several debug widgets.
        self.animate = self.bind_debug_widget(
            "animate", bool, True, False, True)
        self.transparent = self.bind_debug_widget(
            "transparent", bool, False, False, True)
        self.use_gl = self.bind_debug_widget(
            "use_gl", bool, False, False, True)
        self.circle_num_points = self.bind_debug_widget(
            "circle_num_points", int, 60, 3, 1000)
        self.pinwheel_num_lines = self.bind_debug_widget(
            "pinwheel_num_lines", int, 8, 1, 64)
        self.animation_speed = self.bind_debug_widget(
            "animation_speed", float, 1.0, 0.0, 100.0)

        # Recover state on a reload.
        self.panels = getattr(last_proxy, 'panels', [])
        self.frame = getattr(last_proxy, 'frame', 0)
        self.start_time = getattr(last_proxy, 'start_time', time.time())
        self.animtime = getattr(last_proxy, 'animtime', 0.0)

    def on_idle(self):
        if self.animate.value:
            self.window.update()

    def on_special(self, key, x, y):
        if key == ord('a'):
            self.animate.value = not self.animate.value
            self.last_frame_time = time.time()
            self.window.update()
        elif key == ord('t'):
            self.transparent.value = not self.transparent.value
            self.window.update()
        elif key == ord('g'):
            self.use_gl.value = not self.use_gl.value
            self.window.update()
        elif key >= ord('1') and key <= ord('9'):
            panel = { '1' : 'display_trivial_lines',
                      '2' : 'display_simple_lines',
                      '3' : 'display_circle',
                      '4' : 'display_pinwheel' }.get(chr(key))
            if panel is not None:
                # Remove the panel, if it exists.
                if panel in self.panels:
                    self.panels.remove(panel)
                else:
                    self.panels.append(panel)
                self.window.update()
            
    def on_draw(self):
        # Handle animation.
        if self.animate.value:
            self.frame += 1

        current_time = time.time()
        if self.last_frame_time is not None and self.animate.value:
            dtime = current_time - self.last_frame_time
            self.animtime += self.animation_speed.value * dtime
        self.last_frame_time = current_time

        # Draw a silly progress bar across the bottom.
        glColor3f(.9, .9, .9)
        glRectf(0, 0, (self.frame/10. % self.window.width), 12)
        glColor3f(.5, .5, .5)
        draw_string(1, 1, "Use GL: %s, Animate: %s, Time: %.2fs" % (
            "Yes" if self.use_gl.value else "No",
            "Yes" if self.animate.value else "No",
            self.animtime))

        # Organize our displays into a grid.
        if len(self.panels) <= 1:
            rows = columns = 1
        elif len(self.panels) <= 2:
            columns = 1
            rows = 2
        elif len(self.panels) <= 4:
            columns = 2
            rows = 2
        elif len(self.panels) <= 6:
            columns = 2
            rows = 3

        padding = 10
        bottom_padding = 50
        cell_width = (self.window.width - 2*padding) // columns - padding
        cell_height = (self.window.height - 2*padding -
                       bottom_padding) // rows - padding
        
        glTranslatef(.375, .375, 0)
        for column in range(columns):
            for row in range(rows):
                panel_idx = column * rows + row
                if panel_idx >= len(self.panels):
                    break

                panel = self.panels[panel_idx]
                
                x = padding + column * (cell_width + padding)
                y = bottom_padding + padding + row * (cell_height + padding)
                glColor3f(0, 0, 0)
                glBegin(GL_LINE_LOOP)
                glVertex2f(x - 0.375, y - 0.375)
                glVertex2f(x + cell_width - 0.375, y - 0.375)
                glVertex2f(x + cell_width - 0.375, y + cell_height - 0.375)
                glVertex2f(x - 0.375, y + cell_height - 0.375)
                glEnd()

                display = getattr(self, panel)
                display(x, y, cell_width, cell_height)

    def display_trivial_lines(self, x, y, w, h):
        # Display lines at 9 different orientations.
        rows = 3
        columns = 3
        glColor3f(0, 0, 0)
        glBegin(GL_LINES if self.use_gl.value else GL_POINTS)
        l = min(float(w)/columns, float(h)/rows) * .8
        cx = x + w/2.
        cy = y + h/2.
        l = min(w, h)
        x0 = cx - l*.5*.8
        y0 = cy - l*.5*.2
        x1 = cx + l*.5*.8
        y1 = cy + l*.5*.2
        if self.use_gl.value:
            glVertex2f(x0 - 0.375, y0 - 0.375)
            glVertex2f(x1 - 0.375, y1 - 0.375)
        else:
            for pt in line.line2d(x0, y0, x1, y1):
                glVertex2fv(pt)
        glEnd()

    def display_simple_lines(self, x, y, w, h):
        # Display lines at 9 different orientations.
        rows = 3
        columns = 3
        glColor3f(0, 0, 0)
        glBegin(GL_LINES if self.use_gl.value else GL_POINTS)
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
                if self.use_gl.value:
                    glVertex2f(x0 - 0.375, y0 - 0.375)
                    glVertex2f(x1 - 0.375, y1 - 0.375)
                else:
                    for pt in line.line2d(x0, y0, x1, y1):
                        glVertex2fv(pt)
        glEnd()

    def display_circle(self, x, y, w, h):
        N = self.circle_num_points.value # + int(self.frame/10. % 20)
        angle_offset = math.fmod(self.animtime*.01, 1.)
        cx = x + w/2.
        cy = y + h/2.
        l = min(w,h) * .8

        if self.transparent.value:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)
            glColor4f(0., 0., 0., .5)
        else:
            glColor3f(0, 0, 0)

        glBegin(GL_LINES if self.use_gl.value else GL_POINTS)
        for i in range(N):
            t_0 = float(i) / N
            t_1 = float(i + 1) / N
            a_0 = 2*math.pi * t_0 + angle_offset * 2 * math.pi
            a_1 = 2*math.pi * t_1 + angle_offset * 2 * math.pi
            x0 = cx + math.cos(a_0)*l*.5
            y0 = cy + math.sin(a_0)*l*.5
            x1 = cx + math.cos(a_1)*l*.5
            y1 = cy + math.sin(a_1)*l*.5
            if self.use_gl.value:
                glVertex2f(x0 - 0.375, y0 - 0.375)
                glVertex2f(x1 - 0.375, y1 - 0.375)
            else:
                for pt in line.line2d(x0, y0, x1, y1):
                    glVertex2fv(pt)
        glEnd()

        glDisable(GL_BLEND)

    def display_pinwheel(self, x, y, w, h):
        N = self.circle_num_points.value # + int(self.frame/10. % 20)
        angle_offset = math.fmod(self.animtime*.01, 1.)
        cx = x + w/2.
        cy = y + h/2.
        l = min(w,h) * .8

        glColor3f(0, 0, 0)
        glBegin(GL_LINES if self.use_gl.value else GL_POINTS)
        for i in range(N):
            t_0 = float(i) / N
            t_1 = float(i + 1) / N
            a_0 = 2*math.pi * t_0 + angle_offset * 2 * math.pi
            a_1 = 2*math.pi * t_1 + angle_offset * 2 * math.pi
            x0 = cx + math.cos(a_0)*l*.5
            y0 = cy + math.sin(a_0)*l*.5
            x1 = cx + math.cos(a_1)*l*.5
            y1 = cy + math.sin(a_1)*l*.5
            if self.use_gl.value:
                glVertex2f(x0 - 0.375, y0 - 0.375)
                glVertex2f(x1 - 0.375, y1 - 0.375)
            else:
                for pt in line.line2d(x0, y0, x1, y1):
                    glVertex2fv(pt)

        num_lines = self.pinwheel_num_lines.value
        for i in range(num_lines):
            t = float(i) / num_lines
            angle = self.animtime * .1 + t * math.pi
            x0 = cx - math.cos(angle)*l*.5
            y0 = cy - math.sin(angle)*l*.5
            x1 = cx + math.cos(angle)*l*.5
            y1 = cy + math.sin(angle)*l*.5
            if self.use_gl.value:
                glVertex2f(x0 - 0.375, y0 - 0.375)
                glVertex2f(x1 - 0.375, y1 - 0.375)
            else:
                for pt in line.line2d(x0, y0, x1, y1):
                    glVertex2fv(pt)
        glEnd()

def register_pylive(window, last_proxy=None):
    if last_proxy is not None:
        print >>sys.stderr, "reloading module at %.2fs" % (time.time(),)
    else:
        print >>sys.stderr, "loading module initially %.2fs" % (time.time(),)

    # Create our window proxy.
    return HowToDrawALineProxy(window, last_proxy)
