from OpenGL.GL import *

def draw_sand_background(width, height):
    glDisable(GL_BLEND)  # Desabilita o blending (transparência)
    glBegin(GL_QUADS)
    glColor3f(0.96, 0.87, 0.70)  # Cor de areia
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, height)
    glVertex2f(0, height)
    glEnd()
