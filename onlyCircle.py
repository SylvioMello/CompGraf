import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr.matrix44 import *

def circle():
    triangleAmount = 1000
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.4,0.4,0.4)
    x, y, radius = 0, 0, 20
    twicePi = 2.0 * np.pi
    glVertex2f(x, y)  # center of circle
    for i in range(triangleAmount + 1):
        glVertex2f(
            x + (radius * np.cos(i * twicePi / triangleAmount)),
            y + (radius * np.sin(i * twicePi / triangleAmount))
        )
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.4,0.4,0.4)
    x, y, radius = 50, 50, 20
    glVertex2f(x, y)  # center of circle
    for i in range(triangleAmount + 1):
        glVertex2f(
            x + (radius * np.cos(i * twicePi / triangleAmount)),
            y + (radius * np.sin(i * twicePi / triangleAmount))
        )
    glEnd()
    glutSwapBuffers()

def init():
    glClearColor(1.0,1.0,1.0,0.0)
    glLoadIdentity()
    glOrtho(-100.0,100.0,-100.0,100.0,-1.0,1.0)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE)
glutInitWindowSize(800, 600)
glutCreateWindow("Circle")
glutDisplayFunc(circle)
init()
glutMainLoop()