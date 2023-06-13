import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import degrees
from arcball import ArcBall

# size of cube array
n = 3

# rotation angle
angle = 0

# ArcBall object
arcball = None
startx, starty = 0, 0

windowSize = (0, 0)

def draw_scene():
    "Draws the scene"
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -3)
    glRotatef(angle, 0, 1, 1)
    size = 1 / n
    for i in range(n):
        x = i - (n - 1) / 2
        for j in range(n):
            y = j - (n - 1) / 2
            for k in range(n):
                z = k - (n - 1) / 2
                glPushMatrix()
                glTranslatef(x * size, y * size, z * size)
                glutSolidCube(size * 0.8)
                glPopMatrix()


def display():
    draw_scene()
    glutSwapBuffers()


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLight(GL_LIGHT0, GL_POSITION, [.5, .2, 1, 0])
    glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, [0.2, 0.2, 0.2, 1])
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    # Helps with antialiasing
    glEnable(GL_MULTISAMPLE)

    global arcball
    arcball = ArcBall((windowSize[0] / 2, windowSize[1] / 2, 0), min(windowSize[0] / 2, windowSize[1] / 2))



def reshape(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    global projectionArgs
    projectionArgs = 50, width / height, 0.1, 20
    gluPerspective(*projectionArgs)
    glViewport(0, 0, width, height)


def mousePressed(button, state, x, y):
    global arcball, startx, starty
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            arcball = ArcBall((windowSize[0] / 2, windowSize[1] / 2, 0), windowSize[0] / 2)
            startx, starty = x, y


def mouseMotion(x, y):
    global angle, arcball, startx, starty
    if arcball:
        angle, axis = arcball.rot(startx, windowSize[1] - starty, x, windowSize[1] - y)
        glLoadIdentity()
        glRotatef(degrees(angle), *axis)
        startx, starty = x, y
    glutPostRedisplay()


def keyboard(key, x, y):
    if key == b'\x1b':  # ESC
        sys.exit(0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"Rubik")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mousePressed)
    glutMotionFunc(mouseMotion)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == '__main__':
    main()
