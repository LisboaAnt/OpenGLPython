from OpenGL.GL import *
from OpenGL.GLU import *

class Cubo:
    def __init__(self, tamanho=1.0, cor=(1.0, 1.0, 1.0)):
        self.tamanho = tamanho
        self.cor = cor
        self.posicao = [500.0, 500.0, 0.0]

    def desenhar(self):
        r, g, b = self.cor
        x, y, z = self.posicao
        self.desenhar_cubo(self.tamanho, r, g, b)

    def transladar(self, x, y, z):
        self.posicao = [x, y, z]

    def desenhar_cubo(self, lado, r, g, b):
        # Define a cor do cubo
        glColor3f(r, g, b)

        vertices = [
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ]

        faces = [
            [0, 1, 2, 3],  # Face frontal
            [1, 5, 6, 2],  # Face direita
            [5, 4, 7, 6],  # Face traseira
            [4, 0, 3, 7],  # Face esquerda
            [3, 2, 6, 7],  # Face superior
            [4, 5, 1, 0]   # Face inferior
        ]

        # Começa a desenhar o cubo
        for face in faces:
            glBegin(GL_QUADS)
            for vertice_index in face:
                glVertex3f(
                    self.posicao[0] + vertices[vertice_index][0] * lado / 2,
                    self.posicao[1] + vertices[vertice_index][1] * lado / 2,
                    self.posicao[2] + vertices[vertice_index][2] * lado / 2
                )
            glEnd()
