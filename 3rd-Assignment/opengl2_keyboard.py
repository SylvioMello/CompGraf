import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Control points
control_points = []

nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# Initialize window dimensions
width = 800
height = 600

# Mouse state variables
selected_index = -1
prev_mouse_x = 0
prev_mouse_y = 0

# Curve degree
degree = 1

def draw_control_points():
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for point in control_points:
        glVertex2f(point[0], point[1])
    glEnd()

def draw_sample_curve():
    glColor4f(1.0, 0.0, 0.0, 0.2)
    glPointSize(3.0)
    glBegin(GL_POINTS)
    sample = sample_curve(control_points, degree)
    for point in sample:
        glVertex2f(point[0], point[1])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    draw_control_points()
    draw_sample_curve()
    glFlush()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)

def mouse(button, state, x, y):
    global selected_index, prev_mouse_x, prev_mouse_y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # Check if a control point was clicked
            for i, point in enumerate(control_points):
                if abs(point[0] - x) <= 5 and abs(point[1] - (height - y)) <= 5:
                    selected_index = i
                    prev_mouse_x = x
                    prev_mouse_y = height - y
                    break
        elif state == GLUT_UP:
            selected_index = -1

def motion(x, y):
    global selected_index, prev_mouse_x, prev_mouse_y
    if selected_index >= 0:
        dx = x - prev_mouse_x
        dy = height - y - prev_mouse_y
        control_points[selected_index] = (
            control_points[selected_index][0] + dx,
            control_points[selected_index][1] + dy
        )
        prev_mouse_x = x
        prev_mouse_y = height - y
    glutPostRedisplay()

def sample_curve(pts, deg, step=0.01):
    n = len(pts)
    b = [B(k, deg, nodes) for k in range(n)]
    sample = []
    for u in frange(deg, n, step):
        sum_x, sum_y = 0, 0
        for k, p in enumerate(pts):
            w = b[k](u)
            sum_x += w * p[0]
            sum_y += w * p[1]
        sample.append((sum_x, sum_y))
    return sample

def B(k, d, nodes):
    if d == 0:
        return lambda u: 1 if nodes[k] <= u < nodes[k + 1] else 0
    Bk0 = B(k, d - 1, nodes)
    Bk1 = B(k + 1, d - 1, nodes)
    return lambda u: ((u - nodes[k]) / (nodes[k + d] - nodes[k])) * Bk0(u) + ((nodes[k + d + 1] - u) / (nodes[k + d + 1] - nodes[k + 1])) * Bk1(u)

def frange(start, stop, step):
    current = start
    while current <= stop:
        yield current
        current += step

def create_control_points():
    pts = []
    for i in range(6):
        x = 100 + ((width - 200) / 5) * i
        y = height / 2 + (random.random() - 0.5) * (height - 200)
        pts.append((x, y))
    return pts

def keyboard(key, x, y):
    global degree
    if key == b'D':
        degree += 1
        print(f"Increasing degree to {degree}")
    elif key == b'd':
        degree = max(1, degree - 1)
        print(f"Decreasing degree to {degree}")

def main():
    global control_points
    global parms

    parms = {'d': degree}
    control_points = create_control_points()

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("B-Spline Curve")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glutMainLoop()

if __name__ == "__main__":
    main()
