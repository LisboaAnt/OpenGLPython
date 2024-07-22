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

        # Define a cor do obstáculo
        glColor3f(*self.color)

        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        glPopMatrix()

    def desenhar_hitbox(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 5)

        # Define a cor da hitbox (cor preta para contraste)
        glColor3f(0.0, 0.0, 0.0)  # Preto

        # Desenha a hitbox como um retângulo com linhas
        glBegin(GL_LINE_LOOP)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

        glPopMatrix()
