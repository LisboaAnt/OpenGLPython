from OpenGL.GL import *
import numpy as np

class Cubo:
    def __init__(self, initial_position=[0.0, 0.0, -5.0], size=1.0):
        self.position = np.array(initial_position)
        self.size = size

    def draw(self, x, y, z):
        half_size = self.size / 2.0
        vertices = [
            [-half_size, -half_size, -half_size],
            [half_size, -half_size, -half_size],
            [half_size, half_size, -half_size],
            [-half_size, half_size, -half_size],
            [-half_size, -half_size, half_size],
            [half_size, -half_size, half_size],
            [half_size, half_size, half_size],
            [-half_size, half_size, half_size],
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

    def get_hitbox(self):
        half_size = self.size / 2.0
        return (
            self.position[0] - half_size,  # x
            self.position[1] - half_size,  # y
            self.position[2] + half_size,  # z
            self.size,  # width
            self.size,  # height
            self.size   # depth
        )
