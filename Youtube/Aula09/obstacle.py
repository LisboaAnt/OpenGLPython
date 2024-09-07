from OpenGL.GL import *
from OpenGL.GLU import *


class Obstacle:
    def __init__(self, x, y, z, width, height, depth, id=0):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.color = (1.0, 0.0, 0.0)
        self.id = id

    def desenha(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        # Define a cor do obstáculo
        glColor3f(*self.color)

        glBegin(GL_QUADS)
        # Frente
        glVertex3f(0, 0, 0)
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, self.height, 0)
        glVertex3f(0, self.height, 0)

        # Trás
        glVertex3f(0, 0, -self.depth)
        glVertex3f(self.width, 0, -self.depth)
        glVertex3f(self.width, self.height, -self.depth)
        glVertex3f(0, self.height, -self.depth)

        # Esquerda
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, -self.depth)
        glVertex3f(0, self.height, -self.depth)
        glVertex3f(0, self.height, 0)

        # Direita
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, 0, -self.depth)
        glVertex3f(self.width, self.height, -self.depth)
        glVertex3f(self.width, self.height, 0)

        # Topo
        glVertex3f(0, self.height, 0)
        glVertex3f(self.width, self.height, 0)
        glVertex3f(self.width, self.height, -self.depth)
        glVertex3f(0, self.height, -self.depth)

        # Base
        glVertex3f(0, 0, 0)
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, 0, -self.depth)
        glVertex3f(0, 0, -self.depth)
        glEnd()

        glPopMatrix()

    def desenhar_hitbox(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        # Define a cor da hitbox (cor preta para contraste)
        glColor3f(0.0, 0.0, 0.0)  # Preto

        # Desenha a hitbox como um cubo com linhas
        glBegin(GL_LINE_LOOP)
        # Frente
        glVertex3f(0, 0, 0)
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, self.height, 0)
        glVertex3f(0, self.height, 0)

        # Trás
        glVertex3f(0, 0, -self.depth)
        glVertex3f(self.width, 0, -self.depth)
        glVertex3f(self.width, self.height, -self.depth)
        glVertex3f(0, self.height, -self.depth)

        # Esquerda
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, -self.depth)
        glVertex3f(0, self.height, -self.depth)
        glVertex3f(0, self.height, 0)

        # Direita
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, 0, -self.depth)
        glVertex3f(self.width, self.height, -self.depth)
        glVertex3f(self.width, self.height, 0)

        # Topo
        glVertex3f(0, self.height, 0)
        glVertex3f(self.width, self.height, 0)
        glVertex3f(self.width, self.height, -self.depth)
        glVertex3f(0, self.height, -self.depth)

        # Base
        glVertex3f(0, 0, 0)
        glVertex3f(self.width, 0, 0)
        glVertex3f(self.width, 0, -self.depth)
        glVertex3f(0, 0, -self.depth)
        glEnd()

        glPopMatrix()
