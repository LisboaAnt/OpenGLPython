from OpenGL.GL import *
from OpenGL.GLU import *

class Cubo:
    def __init__(self, tamanho=1.0, cor=(1.0, 1.0, 1.0)):
        self.tamanho = tamanho
        self.cor = cor
        self.posicao = [500.0, 500.0, 0.0]

    def desenhar(self):
        r, g, b = self.cor
        self.desenhar_cubo(self.tamanho, r, g, b)

    def transladar(self, x, y, z):
        self.posicao = [x, y, z]

    def desenhar_cubo(self, lado, r, g, b):
        # Define a cor do cubo
        glColor3f(r, g, b)

        vertices = [
            [-1, -1, -1],  # Vértice 0
            [1, -1, -1],   # Vértice 1
            [1, 1, -1],    # Vértice 2
            [-1, 1, -1],   # Vértice 3
            [-1, -1, 1],   # Vértice 4
            [1, -1, 1],    # Vértice 5
            [1, 1, 1],     # Vértice 6
            [-1, 1, 1]     # Vértice 7
        ]

        # Normais para cada face
        normais = [
            [0, 0, -1],   # Normal da face frontal (eixo Z negativo)
            [1, 0, 0],    # Normal da face direita (eixo X positivo)
            [0, 0, 1],    # Normal da face traseira (eixo Z positivo)
            [-1, 0, 0],   # Normal da face esquerda (eixo X negativo)
            [0, 1, 0],    # Normal da face superior (eixo Y positivo)
            [0, -1, 0]    # Normal da face inferior (eixo Y negativo)
        ]

        faces = [
            [0, 1, 2, 3],  # Face frontal
            [1, 5, 6, 2],  # Face direita
            [5, 4, 7, 6],  # Face traseira
            [4, 0, 3, 7],  # Face esquerda
            [3, 2, 6, 7],  # Face superior
            [4, 5, 1, 0]   # Face inferior
        ]

        ambient = [1, 1, 1, 1]  # Cor ambiente (roxo)
        diffuse = [1, 1, 1, 1]  # Cor difusa (roxo)
        specular = [1.0, 1.0, 1.0, 1.0]  # Cor especular (branco)
        shininess = 1.0  # Brilho do material

        # Define o material
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

        # Desenhar o cubo com normais
        for i, face in enumerate(faces):
            glBegin(GL_QUADS)
            glNormal3fv(normais[i])  # Define a normal da face atual
            for vertice_index in face:
                glVertex3f(
                    self.posicao[0] + vertices[vertice_index][0] * lado / 2,
                    self.posicao[1] + vertices[vertice_index][1] * lado / 2,
                    self.posicao[2] + vertices[vertice_index][2] * lado / 2
                )
            glEnd()
