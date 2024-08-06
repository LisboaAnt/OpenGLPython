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
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5],
        ]
        colors = [
            [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [0.5, 0.5, 0.5], [1, 0.5, 0]
        ]
        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glColor3fv(colors[vertex])
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()