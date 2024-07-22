from OpenGL.GL import *


class Cube:
    def __init__(self, x, y, width, height, color=(0.0, 1.0, 0.0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def desenha(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.width)

        # Define a cor do cubo
        glColor3f(*self.color)

        glBegin(GL_QUADS)

        # Face frontal
        glVertex3f(0, 0, 0)
        glVertex3f(self.height, 0, 0)
        glVertex3f(self.height, self.height, 0)
        glVertex3f(0, self.height, 0)

        # Face traseira
        glVertex3f(0, 0, self.height)
        glVertex3f(self.height, 0, self.height)
        glVertex3f(self.height, self.height, self.height)
        glVertex3f(0, self.height, self.height)

        # Face lateral esquerda
        glVertex3f(0, 0, 0)
        glVertex3f(0, self.height, 0)
        glVertex3f(0, self.height, self.height)
        glVertex3f(0, 0, self.height)

        # Face lateral direita
        glVertex3f(self.height, 0, 0)
        glVertex3f(self.height, self.height, 0)
        glVertex3f(self.height, self.height, self.height)
        glVertex3f(self.height, 0, self.height)

        # Face superior
        glVertex3f(0, self.height, 0)
        glVertex3f(self.height, self.height, 0)
        glVertex3f(self.height, self.height, self.height)
        glVertex3f(0, self.height, self.height)

        # Face inferior
        glVertex3f(0, 0, 0)
        glVertex3f(self.height, 0, 0)
        glVertex3f(self.height, 0, self.height)
        glVertex3f(0, 0, self.height)

        glEnd()

        glPopMatrix()
