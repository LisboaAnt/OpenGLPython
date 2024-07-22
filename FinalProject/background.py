import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_sand_background():
    width, height = 800, 600
    glBegin(GL_QUADS)
    glColor3f(0.96, 0.87, 0.70)  # Cor de areia
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, height)
    glVertex2f(0, height)
    glEnd()