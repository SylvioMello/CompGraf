import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Circle:
    def __init__(self, points, radius):
        self.points = points
        self.radius = radius
    def draw(self):
        triangleAmount = 100
        twicePi = 2.0 * np.pi
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.4,0.4,0.4)
        glVertex2f(self.points[0], self.points[1])  # center of circle
        for i in range(triangleAmount + 1):
            glVertex2f(
                self.points[0] + (self.radius * np.cos(i * twicePi / triangleAmount)),
                self.points[1] + (self.radius * np.sin(i * twicePi / triangleAmount))
            )
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    circle1.draw()
    circle2.draw()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Circle Example")

    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-100, 100, -100, 100)

    global circle1, circle2
    circle1 = Circle([0, 0], 80)
    circle2 = Circle([-50, 50], 10)

    glutDisplayFunc(display)
    glutMainLoop()

main()