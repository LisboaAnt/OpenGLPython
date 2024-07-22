from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Obstacle:
    def __init__(self, x, y, width, height, color=(1.0, 0.0, 0.0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color  # Cor padrão é vermelho

    def desenha(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

        # Define a cor do obstáculo
        glColor3f(*self.color)

        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        glPopMatrix()
