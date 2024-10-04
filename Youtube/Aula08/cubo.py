from OpenGL.GL import *
import numpy as np

class Cubo:
    def __init__(self, inital_position=[0.0, 0.0, 0.0]):
        self.position = inital_position

    def draw(self, x, y, z):
        vertices = [
            [-1, -1, -1],  # Vértice 0
            [1, -1, -1],  # Vértice 1
            [1, 1, -1],  # Vértice 2
            [-1, 1, -1],  # Vértice 3
            [-1, -1, 1],  # Vértice 4
            [1, -1, 1],  # Vértice 5
            [1, 1, 1],  # Vértice 6
            [-1, 1, 1]  # Vértice 7
        ]

        # Normais para cada face
        normais = [
            [0, 0, -1],  # Normal da face frontal (eixo Z negativo)
            [1, 0, 0],  # Normal da face direita (eixo X positivo)
            [0, 0, 1],  # Normal da face traseira (eixo Z positivo)
            [-1, 0, 0],  # Normal da face esquerda (eixo X negativo)
            [0, 1, 0],  # Normal da face superior (eixo Y positivo)
            [0, -1, 0]  # Normal da face inferior (eixo Y negativo)
        ]

        faces = [
            [0, 1, 2, 3],  # Face frontal
            [1, 5, 6, 2],  # Face direita
            [5, 4, 7, 6],  # Face traseira
            [4, 0, 3, 7],  # Face esquerda
            [3, 2, 6, 7],  # Face superior
            [4, 5, 1, 0]  # Face inferior
        ]
        colors = [
            [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [0.5, 0.5, 0.5], [1, 0.5, 0]
        ]

        # Define as propriedades do material do objeto
        ambient = [0.8, 0.8, 0.8, 1.0]  # Cor ambiente (branco)
        diffuse = [0.8, 0.8, 0.8, 1.0]  # Cor difusa (branco)
        specular = [0.8, 0.8, 0.8, 1.0]  # Cor especular (branco)
        shininess = 50.0  # Brilho do material

        # Define o material
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glNormal3fv(normais[i])

            for vertex in face:
                glColor3fv(colors[vertex])
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()