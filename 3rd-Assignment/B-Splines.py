import sys
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18

# Control points
control_points = []
degree = 0
nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
random_nums = []

# Initialize window dimensions
width = 800
height = 600

# Mouse state variables
selected_index = -1
prev_mouse_x = 0
prev_mouse_y = 0

def generate_random_nums():
    for _ in range(6):
        random_nums.append(random.random())

generate_random_nums()

def create_control_points():
    pts = []
    for i in range(6):
        x = 100 + ((width - 200) / 5) * i
        y = height / 2 + (random_nums[i] - 0.5) * (height - 200)
        pts.append((x, y))
    return pts

control_points = create_control_points()

def draw_control_points():
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for point in control_points:
        glVertex2f(point[0], point[1])
    glEnd()

def draw_control_point_labels():
    glColor3f(0.0, 0.0, 0.0)
    for i, point in enumerate(control_points):
        glRasterPos2f(point[0] + 10, point[1] - 10)
        for char in str(i + 1):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

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

def sample_curve(pts, step=0.01):
    n = len(pts)
    b = [B(k, degree, nodes) for k in range(n)]
    sample = []
    for u in frange(degree, n, step):
        sum_x, sum_y = 0, 0
        for k, p in enumerate(pts):
            w = b[k](u)
            sum_x += w * p[0]
            sum_y += w * p[1]
        sample.append((sum_x, sum_y))
    return sample

def draw_sample_curve():
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.0, 0.0, 0.2)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    sample = sample_curve(control_points)
    for point in sample:
        glVertex2f(point[0], point[1])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    draw_control_points()
    draw_control_point_labels()
    draw_sample_curve()
    glFlush()

def reshape(w, h):
    global width, height, control_points
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    control_points = create_control_points()

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

def keyboard(key, x, y):
    global degree
    if key == b'D':
        degree = min(5, degree + 1)
        glutPostRedisplay()
        print(f"Increasing degree to {degree}")
    elif key == b'd':
        degree = max(0, degree - 1)
        glutPostRedisplay()
        print(f"Decreasing degree to {degree}")

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