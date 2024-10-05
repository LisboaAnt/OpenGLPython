from OpenGL.GL import *
from OpenGL.GLU import *

class Obstacle:
    def __init__(self, x, y, width, height, color=(1.0, 0.0, 0.0), id=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color  # Cor padrão é vermelho
        self.id = id

    def desenha(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.5)

        # Define as propriedades do material do obstáculo
        ambient = [1, 0.2, 0.2, 1.0]  # Cor ambiente (cinza escuro)
        diffuse = self.color  # Cor difusa do obstáculo
        specular = [1.0, 1.0, 1.0, 1.0]  # Cor especular (branco)
        shininess = 50.0  # Brilho do material

        # Define o material
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

        # Desenha o obstáculo
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        glPopMatrix()

