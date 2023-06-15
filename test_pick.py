import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import degrees
import vector
from arcball import ArcBall

# Selected object
selected = None

# Set of removed objects
removed = set()

# size of cube array
n = 3

# rotation angle
angle = 0

# ArcBall object
arcball = None
startx, starty = 0, 0

def draw_scene(flatColors=False):
    "Draws the scene emitting a 'name' for each cube"
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -3)
    glRotatef(-80, 1, 0, 0)
    glRotatef(angle, 0, 1, 1)
    size = 1 / n
    for i in range(n):
        x = i - (n - 1) / 2
        for j in range(n):
            y = j - (n - 1) / 2
            for k in range(n):
                z = k - (n - 1) / 2
                name = (i * n + j) * n + k
                if flatColors:
                    glColor3f((i + 1) / n, (j + 1) / n, (k + 1) / n)
                # Ignore removed objects
                if name in removed:
                    continue
                glLoadName(name)
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


def reshape(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    global projectionArgs, windowSize
    windowSize = width, height
    projectionArgs = 50, width / height, 0.1, 20
    gluPerspective(*projectionArgs)
    glViewport(0, 0, width, height)


def pick(x, y):
    glDisable(GL_LIGHTING)
    draw_scene(True)
    glFlush()
    glEnable(GL_LIGHTING)
    buf = glReadPixels(x, windowSize[1] - y, 1, 1, GL_RGB, GL_FLOAT)
    pixel = buf[0][0]
    r, g, b = pixel
    i, j, k = int(r * n - 1), int(g * n - 1), int(b * n - 1)
    if i >= 0:
        return (i * n + j) * n + k
    return -1


def mousePressed(button, state, x, y):
    global selected, prevx, prevy, arcball, startx, starty
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            selected = pick(x, y)
            if selected != -1:
                arcball = ArcBall((windowSize[0] / 2, windowSize[1] / 2, 0), windowSize[0] / 2)
                startx, starty = x, y
        else:
            selected = None


def mouseMotion(x, y):
    global angle, prevx, prevy, arcball, startx, starty
    if selected is not None:
        dx = x - prevx
        dy = y - prevy
        prevx = x
        prevy = y
        angle += (dx + dy) * 0.2  # Update angle based on both dx and dy
    else:
        if arcball:
            angle, axis = arcball.rot(startx, windowSize[1] - starty, x, windowSize[1] - y)
            glLoadIdentity()
            glRotatef(degrees(angle), *axis)
            glMultMatrixd(matrix)
            matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
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
