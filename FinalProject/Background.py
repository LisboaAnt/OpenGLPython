import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


class TronBackground:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.create_background()

    def create_background(self):
        # Configurações iniciais
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        glLineWidth(1.0)  # Espessura das linhas

    def draw_background(self):
        glLineWidth(1)
        glBegin(GL_LINES)
        glColor3f(0, 0, 1)  # Cor azul brilhante
        # Desenhar linhas verticais
        for i in range(-self.width // 2, self.width // 2, self.grid_size):
            glVertex2f(i, -self.height // 2)
            glVertex2f(i, self.height // 2)
        # Desenhar linhas horizontais
        for i in range(-self.height // 2, self.height // 2, self.grid_size):
            glVertex2f(-self.width // 2, i)
            glVertex2f(self.width // 2, i)
        glEnd()

    def draw(self):
        self.draw_background()