from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from PIL import Image

def loadTexture(filename):
    """Loads an image from a file as a texture"""
    imagefile = Image.open(filename)
    sx, sy = imagefile.size[0:2]
    pixels = imagefile.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    image = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, image)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, sx, sy, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return image

def drawCube():
    """Draws a cube with textures"""
    glBindTexture(GL_TEXTURE_2D, textureId)
    glBegin(GL_QUADS)

    # Front Face
    glNormal3f(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)

    # Back Face
    glNormal3f(0, 0, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Top Face
    glNormal3f(0, 1, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)

    # Bottom Face
    glNormal3f(0, -1, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)

    # Right Face
    glNormal3f(1, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Left Face
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)

    glEnd()

# Screen width and height
width, height = 500, 500

# Current rotation angle in degrees
angle = 0

def init():
    """Initialize state"""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_TEXTURE_2D)

    global textureId
    textureId = loadTexture("arrow2.jpeg")

def display():
    """Display callback"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(-80, 1, 0, 0)
    glRotatef(angle, 0, 1, 1)
    drawCube()
    glutSwapBuffers()

def reshape(w, h):
    """Reshape Callback"""
    glViewport(0, 0, w, h)
    global width, height
    width, height = w, h
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 1, 10)

def idle():
    """Idle callback"""
    global angle
    angle += 0.4
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(width, height)
glutCreateWindow("Textured Cube")
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutIdleFunc(idle)
init()
glutMainLoop()
