import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# Selected object
selected = None

# Set of removed objects
removed = set()

# size of cube array
n = 3

# rotation parameters
angle = 0
prevx = 0
prevy = 0
rotating = False

windowSize = (500, 500)


# Variável para controlar a translação do cubo
cube_translations = []
# Inicializa as translações dos cubos
for i in range(n**3):
    cube_translations.append([0, 0, 0])

def draw_scene(flatColors=False):
    # Draw the scene with cubes
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
                if name in removed:
                    continue
                glLoadName(name)
                glPushMatrix()
                glTranslatef(x * size + cube_translations[name][0], y * size + cube_translations[name][1], z * size + cube_translations[name][2])
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
    glEnable(GL_MULTISAMPLE)

def reshape(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    global windowSize
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
    global selected, prevx, prevy, rotating
    if state == GLUT_DOWN:
        prevx, prevy = x, y
        selected = pick(x, y)
        rotating = True
        if selected >= 0:
            selected_cube = selected
            # Configura o movimento gradual do cubo
            start_translation = cube_translations[selected_cube].copy()
            target_translation = [start_translation[0] + 50, start_translation[1] + 50, start_translation[2] + 50]
            total_frames = 150  # Número total de quadros para completar o movimento
            frame = 0

            def lerp(a, b, t):
                return np.array(a) + (np.array(b) - np.array(a)) * t

            def update_translation(arg=None):
                nonlocal frame
                if frame >= total_frames:
                    # Finaliza o movimento
                    cube_translations[selected_cube] = target_translation
                else:
                    # Atualiza gradualmente as coordenadas de translação
                    t = frame / total_frames  # Calcula o fator de interpolação
                    cube_translations[selected_cube] = lerp(start_translation, target_translation, t)
                    frame += 1
                    glutTimerFunc(16, update_translation, None)  # Aguarda 16ms (aproximadamente 60 quadros por segundo) e chama novamente a função
                glutPostRedisplay()

            # Inicia o movimento
            update_translation()
    elif state == GLUT_UP:
        rotating = False
    glutPostRedisplay()

def mouseMotion(x, y):
    global angle, prevx, prevy, rotating
    if rotating:
        dx = x - prevx
        dy = y - prevy
        prevx = x
        prevy = y
        angle += (dx + dy) * 0.2  # Update angle based on both dx and dy
        glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("picking")
    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutMouseFunc(mousePressed)
    glutMotionFunc(mouseMotion)  # Added mouse motion callback
    glutMainLoop()

main()