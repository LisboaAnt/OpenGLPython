from OpenGL.GL import *
import numpy as np

class Cubo:
    def __init__(self, inital_position=[0.0, 0.0, 0.0]):
        self.position = inital_position

    def draw(self, x, y, z):
        vertices = [
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
        ]
        faces = [
            [0, 1, 2, 3], # front
            [1, 5, 6, 2], # dir
            [5, 4, 7, 6], # tras
            [4, 0, 3, 7], # esq
            [3, 2, 6, 7], # sup
            [4, 5, 1, 0], # inf
        ]

        normais = [
            [0, 0, -1],
            [1, 0, 0],
            [0, 0, 1],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0]
        ]

        color = [1, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, color)
        glMaterialfv(GL_FRONT, GL_AMBIENT, color)
        glMaterialfv(GL_FRONT, GL_SHININESS, 100)

        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glNormal3fv(normais[i])
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()