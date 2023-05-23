import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr.matrix44 import *

shapes = []

class Rect(object):
    def __init__ (self, points, m = create_identity()):
        self.points = points
        self.set_matrix(m)
        self.start_scale = None
    def set_point (self, i, p):
        self.points[i] = p
        self.set_center()
    def set_matrix(self,t):
        self.m = t
        self.invm = inverse(t)
    def set_center(self):
        self.center = [(self.points[0][0] + self.points[1][0])/2,(self.points[0][1] + self.points[1][1])/2]
    def get_center(self):
        # Calculate the center of the rectangle
        points = []
        for point in self.points:
            point = apply_to_vector(self.m, [point[0], point[1], 0, 1])
            points.append(point)
        return [(points[0][0]+points[1][0])/2, (points[0][1]+points[1][1])/2]
    def contains(self,p):
        p = apply_to_vector(self.invm, [p[0],p[1],0,1])
        xmin = min(self.points[0][0],self.points[1][0])
        xmax = max(self.points[0][0],self.points[1][0])
        ymin = min(self.points[0][1],self.points[1][1])
        ymax = max(self.points[0][1],self.points[1][1])
        return xmin <= p[0] <= xmax and ymin <=p[1] <= ymax
    def draw (self):
        glPushMatrix()
        glMultMatrixf(self.m)
        glRectf(*self.points[0],*self.points[1])
        glPopMatrix()

class Circle(object):
    def __init__(self, points, radius, m = create_identity()):
        self.points = points
        self.radius = radius
        self.set_matrix(m)
        self.start_scale = None
    def set_radius(self, next_radius):
        next_x = next_radius[0] - self.points[0]
        next_y = next_radius[1] - self.points[1]
        self.radius = np.sqrt((next_x ** 2) + (next_y **2))
        self.set_center()
    def set_center(self):
        self.center = self.points
    def get_center(self):
        return apply_to_vector(self.m, [self.points[0], self.points[1], 0, 1])
    def set_matrix(self, t):
        self.m = t
        self.invm = inverse(t)
    def contains(self, p):
        p = apply_to_vector(self.invm, [p[0], p[1], 0, 1])
        dx = p[0] - self.points[0]
        dy = p[1] - self.points[1]
        return dx ** 2 + dy ** 2 <= self.radius ** 2
    def draw(self):
        triangleAmount = 13
        twicePi = 2.0 * np.pi
        glPushMatrix()  # Push the current matrix stack
        glMultMatrixf(self.m)
        glTranslatef(self.points[0], self.points[1], 0.0)  # Translate to the center of the circle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)  # center of circle
        for i in range(triangleAmount + 1):
            glVertex2f(
                self.radius * np.cos(i * twicePi / triangleAmount),
                self.radius * np.sin(i * twicePi / triangleAmount)
            )
        glEnd()
        glPopMatrix()  # Restore the previous matrix from the stack

picked = None
modeConstants = ["RECTANGLE", "CIRCLE", "TRANSLATE", "ROTATE", "SCALE"]
mode = modeConstants[0]

def reshape(width, height):
    glViewport(0,0,width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,width,height,0)
    glMatrixMode (GL_MODELVIEW)

def mouse(button, state, x, y):
    global lastx,lasty,picked
    if state!=GLUT_DOWN: return
    if mode == "RECTANGLE":
        shapes.append(Rect([[x,y],[x,y]]))
    elif mode == "CIRCLE":
        shapes.append(Circle([x, y], 0))
    elif mode == "TRANSLATE" or mode == "ROTATE" or mode == "SCALE":
        picked = None
        for s in shapes:
            if s.contains([x,y]):
                picked = s
        lastx,lasty = x,y

def mouse_drag(x, y):
    global lastx, lasty
    if mode == "RECTANGLE":
        shapes[-1].set_point(1,[x,y])
    elif mode == "CIRCLE":
        shapes[-1].set_radius([x, y])
    elif mode == "TRANSLATE":
        if picked:
            t = create_from_translation([x-lastx,y-lasty,0])
            picked.set_matrix(multiply(picked.m, t))
            lastx,lasty = x,y
    elif mode == "ROTATE":
        if picked:
            center = picked.get_center()
            dx, dy = (x - center[0]), (y - center[1])
            current_angle = np.arctan2(dy, dx)
            last_angle = np.degrees(np.arctan2(lasty - center[1], lastx - center[0]) - current_angle)
            alpha = 0.02 * last_angle
            t1 = create_from_translation([-center[0], -center[1], 0])  # Translate to origin
            t2 = create_from_z_rotation(alpha)  # Rotate around Z-axis
            t3 = create_from_translation([center[0], center[1], 0])  # Translate back to original position
            t = multiply(multiply(t1, t2), t3)  # Combine the transformations
            picked.set_matrix(multiply(picked.m, t))
            lastx, lasty = x, y
    elif mode == "SCALE":
        if picked:
            if picked.start_scale is not None:
                center = np.mean(picked.points, axis=0)
                start_x, start_y = picked.start_scale
                scale_factor = (x - start_x) / (center[0] - start_x + 1e-5)
                t1 = create_from_translation([-center[0], -center[1], 0])  # Translate to origin
                t2 = create_from_scale([scale_factor, 1, 1])  # Scale along X-axis
                t3 = create_from_translation([center[0], center[1], 0])  # Translate back to original position
                t = multiply(multiply(t1, t2), t3)  # Combine the transformations
                picked.set_matrix(multiply(picked.m, t))
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for s in shapes:
        glColor3f(0.4, 0.4, 0.4)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        s.draw()
        glColor3f(1.0, 0.0, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        s.draw()
    glutSwapBuffers()

def createMenu():
    def domenu(item):
        global mode
        mode = modeConstants[item]
        return 0
    glutCreateMenu(domenu)
    for i,name in enumerate(modeConstants):
        glutAddMenuEntry(name, i)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

glutInit(sys.argv)
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize (800, 600)
glutCreateWindow("Shape Editor")
glutMouseFunc(mouse)
glutMotionFunc(mouse_drag)
glutDisplayFunc(display)
glutReshapeFunc(reshape)
createMenu()
glutMainLoop()