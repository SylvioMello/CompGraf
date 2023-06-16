import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
from random import choice
from math import *
import vector
import math

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
windowSize = (0, 0)
# Variável para controlar a translação do cubo
cube_translations = []
# Inicializa as translações dos cubos
for i in range(n**3):
    cube_translations.append([0, 0, 0])
# Direction the cube can move
move_left = [-40, 0, 0]
move_right = [40, 0, 0]
move_back = [0, 40, 0]
move_front = [0, -40, 0]
move_up = [0, 0, 40]
move_down = [0, 0, -40]
directions = [move_left, move_right, move_back, move_front, move_up, move_down]
# Target translation for each cube
right_translation = [] 
for i in range(n):
    for j in range(n):
        for k in range(n):
            coord = choice(directions).copy()
            if i == 0:
                coord[0] = -1 * abs(coord[0])
            if i == 2:
                coord[0] = abs(coord[0])
            if j == 0:
                coord[1] = -1 * abs(coord[1])
            if j == 2:
                coord[1] = abs(coord[1])
            if k == 0:
                coord[2] = -1 * abs(coord[2])
            if k == 2:
                coord[2] = abs(coord[2])
            right_translation.append(coord)

class ArcBall(object):
    """Implements an arcball manipulator for specifying rotations."""
    
    def __init__(self, center, radius):
        """Creates a new arcball manipulator. 
        @param center: Center point of the sphere (in window coordinates).
        @param radius: Radius of the sphere (in window coordinates).
        """
        self.center = center
        self.radius = radius
        
    def _rotby2vectors (self, startvector, endvector):
        """Given two unit vectors returns the rotation axis and rotation angle 
        that maps the first onto the second.
        @param startvector: original vector.
        @param endvector: destination vector.
        @return: (angle,axis).
        """
        r = vector.cross(startvector, endvector)
        l = vector.length (r)
        if l<1e-10: return 0,(0,0,1)
        angle = acos(vector.dot(startvector,endvector))
        #angle = asin (l)
        axis = vector.scale(r,1.0/l)
        return (angle,axis)
    
    def _projvector (self, x, y):
        """Given a ray with origin (x,y,inf) and direction (0,0,-inf), translate
        it to the arcball's local coordinate system and return the intersection
        point with that sphere of unit radius and centered at the origin. If no 
        intersection exists, intersect it with the plane z=0 and project that
        that point onto the unit sphere.
        @param x,y: coordinates for the ray.
        @return: projected vector.
        """
        v = vector.scale ((x-self.center[0],y-self.center[1],0.0), 1.0/self.radius)
        l = vector.length(v)
        if l>=1.0: return vector.scale(v,1.0/l)
        z = sqrt (1.0 - l*l)
        return (v[0],v[1],z)
                
    def rot (self, x0, y0, x1, y1):
        """Given two screen points, returns the arcball rotation that maps
        the first onto the second.
        @param x0,y0: first point.
        @param x1,y1: second point.
        @return: (angle,axis).
        """
        return self._rotby2vectors (self._projvector(x0,y0), self._projvector(x1,y1))

def rotatecallback (x, y):
    global startx,starty,matrix
    angle, axis = arcball.rot (startx, height - starty, x, height - y) # retorna um angulo de rotacao e um eixo de rotacao
    # assumindo que foi feito um gesto que comeca em startx e (height - starty)
    # e fez um drag ate x e (height - y)
    glLoadIdentity ()
    glRotatef (degrees(angle),*axis) # multiplica por uma matriz de rotacao com angulo angle e no eixo axis
    glMultMatrixd (matrix) # pega a matriz anterior e multiplica pela matriz de rotacao
    matrix = glGetDoublev(GL_MODELVIEW_MATRIX) # retorna o resultado da multiplicacao
    startx,starty = x,y
    glutPostRedisplay()

def draw_cube_with_image(image_path):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, windowSize[0], 0, windowSize[1], -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = Image.open(image_path)
    width, height = image.size
    image_data = image.tobytes("raw", "RGB", 0, -1)
    glEnable(GL_TEXTURE_2D)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(windowSize[0], 0)
    glTexCoord2f(1, 1)
    glVertex2f(windowSize[0], windowSize[1])
    glTexCoord2f(0, 1)
    glVertex2f(0, windowSize[1])
    glEnd()
    glDisable(GL_TEXTURE_2D)

def loadTexture (filename):
    "Loads an image from a file as a texture"
    # Read file and get pixels
    imagefile = Image.open(filename)
    sx,sy = imagefile.size[0:2]
    global pixels
    pixels = imagefile.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    # Create an OpenGL texture name and load image into it
    image = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, image)  
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, sx, sy, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
    # Set other texture mapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL) # mudar GL_DECAL para GL_MODULATE?
    # tem que ligar a iluminacao??
    # Return texture name (an integer)
    return image

# fazer quatro faces com as flechas e duas faces brancas
# tem que ser resolvivel...
# se tiver algum bloco no caminho de outro, esse outro precisa ficar parado
def drawCube(size):
    glBegin(GL_QUADS)  # Start Drawing The Cube

    # Front Face (note that the texture's corners have to match the quad's corners)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * size, -1.0 * size, 1.0 * size)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0 * size, -1.0 * size, 1.0 * size)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * size, 1.0 * size, 1.0 * size)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0 * size, 1.0 * size, 1.0 * size)  # Top Left Of The Texture and Quad

    # Back Face
    glNormal3f(0, 0, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0 * size, -1.0 * size, -1.0 * size)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0 * size, 1.0 * size, -1.0 * size)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0 * size, 1.0 * size, -1.0 * size)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0 * size, -1.0 * size, -1.0 * size)  # Bottom Left Of The Texture and Quad

    # Top Face
    glNormal3f(0, 1, 0)
    glTexCoord2f(0.75, 0.75)
    glVertex3f(-1.0 * size, 1.0 * size, -1.0 * size)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.75, 0.75)
    glVertex3f(-1.0 * size, 1.0 * size, 1.0 * size)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(0.75, 0.75)
    glVertex3f(1.0 * size, 1.0 * size, 1.0 * size)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(0.75, 0.75)
    glVertex3f(1.0 * size, 1.0 * size, -1.0 * size)  # Top Right Of The Texture and Quad

    # Bottom Face
    glNormal3f(0, -1, 0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(-1.0 * size, -1.0 * size, -1.0 * size)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.5, 0.5)
    glVertex3f(1.0 * size, -1.0 * size, -1.0 * size)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.5, 0.5)
    glVertex3f(1.0 * size, -1.0 * size, 1.0 * size)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(0.5, 0.5)
    glVertex3f(-1.0 * size, -1.0 * size, 1.0 * size)  # Bottom Right Of The Texture and Quad

    # Right face
    glNormal3f(1, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0 * size, -1.0 * size, -1.0 * size)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * size, 1.0 * size, -1.0 * size)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0 * size, 1.0 * size, 1.0 * size)  # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0 * size, -1.0 * size, 1.0 * size)  # Bottom Left Of The Texture and Quad

    # Left Face
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * size, -1.0 * size, -1.0 * size)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0 * size, -1.0 * size, 1.0 * size)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0 * size, 1.0 * size, 1.0 * size)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0 * size, 1.0 * size, -1.0 * size)  # Top Left Of The Texture and Quad

    glEnd()

def draw_scene(flatColors=False):
    # Draw the scene with cubes
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -3)
    glMultMatrixd (matrix)
    glRotatef(-80, 1, 0, 0)
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
                # Texture initialization
                loadTexture("arrow2.jpeg") 
                # Rotate cube to align with the x-axis
                x_rot, y_rot, z_rot = right_translation[name][0] / 40, right_translation[name][1] / 40, right_translation[name][2] / 40
                if x_rot == 1.0:
                    glRotatef(-90, 0, 0, 1)
                elif x_rot == -1.0:
                    glRotatef(90, 0, 0, 1)
                elif y_rot == 1.0:
                    pass # No rotation needed
                elif y_rot == -1.0:
                    glRotatef(180, 0, 0, 1)
                elif z_rot == 1.0:
                    glRotatef(90, 1, 0 , 0)
                elif z_rot == -1.0:
                    glRotatef(-90, 1, 0 , 0)
                drawCube(size * 0.401)
                glPopMatrix()
    if len(removed) == n**3:
        draw_cube_with_image("youwin.png")  # Replace with the actual image path

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
    glEnable(GL_TEXTURE_2D)

    # Helps with antialiasing
    glEnable(GL_MULTISAMPLE)

    global matrix 
    matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

def reshape(w, h):
    global width,height
    width, height = w, h
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    global windowSize
    windowSize = width, height
    projectionArgs = 50, width / height, 0.1, 20
    gluPerspective(*projectionArgs)
    glViewport(0, 0, width, height)

def pick(x, y):
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    draw_scene(True)
    glFlush()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    buf = glReadPixels(x, windowSize[1] - y, 1, 1, GL_RGB, GL_FLOAT)
    pixel = buf[0][0]
    r, g, b = pixel
    i, j, k = int(r* n - 1), int(g * n - 1), int(b * n - 1)
    if i >= 0:
        return [i, j, k]
    return [-1, -1, -1]

def mousePressed(button, state, x, y):
    global selected, prevx, prevy
    if state == GLUT_DOWN:
        
        global arcball
        arcball = ArcBall ((width/2,height/2,0), width/2)
        global startx, starty
        startx, starty = x,y
        glutMotionFunc (rotatecallback)
    elif state == GLUT_UP:
        prevx, prevy = x, y
        coordinates = pick(x, y)
        selected = (coordinates[0] * n + coordinates[1]) * n + coordinates[2]
        if selected >= 0:
            neighbor = selected + (right_translation[selected][0]/40) * 9 + (right_translation[selected][1]/40) * 3 + (right_translation[selected][2]/40) * 1
            pass_through = False
            if coordinates[0] != 1 or coordinates[1] != 1 or coordinates[2] != 1:
                if coordinates[0] == 0:
                    if  right_translation[selected] == [-40, 0, 0]:
                        pass_through = True
                if coordinates[0] == 2:
                    if  right_translation[selected] == [40, 0, 0]:
                        pass_through = True
                if coordinates[1] == 0:
                    if  right_translation[selected] == [0,-40, 0]: # If moves back
                        pass_through = True
                if coordinates[1] == 2:
                    if  right_translation[selected] == [0, 40, 0]: # If moves forward
                        pass_through = True
                if coordinates[2] == 0:
                    if  right_translation[selected] == [0, 0, -40]: # If moves down
                        pass_through = True
                if coordinates[2] == 2:
                    if  right_translation[selected] == [0, 0, 40]: # If moves up
                        pass_through = True
            if (neighbor in removed) == True:
                pass_through = True
            if pass_through == True:
                selected_cube = selected
                # Configura o movimento gradual do cubo
                start_translation = cube_translations[selected_cube].copy()
                target_translation = right_translation[selected_cube].copy()
                total_frames = 150  # Número total de quadros para completar o movimento
                frame = 0
                def lerp(a, b, t):
                    return np.array(a) + (np.array(b) - np.array(a)) * t
                def update_translation(arg=None):
                    nonlocal frame
                    if frame >= total_frames/10:
                        # Finaliza o movimento
                        removed.add(selected_cube)
                        cube_translations[selected_cube] = target_translation
                    else:
                        # Atualiza gradualmente as coordenadas de translação
                        t = frame / total_frames  # Calcula o fator de interpolação
                        cube_translations[selected_cube] = lerp(start_translation, target_translation, t)
                        frame += 2
                        glutTimerFunc(16, update_translation, None)  # Aguarda 16ms (aproximadamente 60 quadros por segundo) e chama novamente a função
                    glutPostRedisplay()
                # Inicia o movimento
                update_translation()
            else: 
                selected_cube = selected
                # Configura o movimento gradual do cubo
                start_translation = cube_translations[selected_cube].copy()
                target_translation = [x/500 for x in right_translation[selected_cube].copy()]
                total_frames = 3  # Número total de quadros para completar o movimento
                frame = 0
                def lerp(a, b, t):
                    return np.array(a) + (np.array(b) - np.array(a)) * t
                def update_translation(arg=None):
                    nonlocal frame
                    if frame >= total_frames:
                        # Finaliza o movimento
                        cube_translations[selected_cube] = start_translation
                    else:
                        # Atualiza gradualmente as coordenadas de translação
                        t = frame / total_frames  # Calcula o fator de interpolação
                        cube_translations[selected_cube] = lerp(start_translation, target_translation, t)
                        frame += 1
                        glutTimerFunc(4, update_translation, None)  # Aguarda 16ms (aproximadamente 60 quadros por segundo) e chama novamente a função
                    glutPostRedisplay()
                # Inicia o movimento
                update_translation()
                cube_translations[selected_cube] = [0,0,0]
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
    glutMainLoop()

main()