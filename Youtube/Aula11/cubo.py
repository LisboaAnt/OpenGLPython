from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class Cubo:
    def __init__(self, initial_position=[0.0, 0.0, 0.0],raio = 1, texture_atlas=None, texture_indices=[0, 1, 2, 3, 4, 5]):
        self.position = initial_position
        self.texture_atlas = texture_atlas
        self.texture_indices = texture_indices
        self.raio = raio

    def draw(self, x=0, y=0, z=0):
        vertices = [
            [-self.raio, -self.raio, -self.raio], [self.raio, -self.raio, -self.raio], [self.raio, self.raio, -self.raio], [-self.raio, self.raio, -self.raio],
            [-self.raio, -self.raio, self.raio], [self.raio, -self.raio, self.raio], [self.raio, self.raio, self.raio], [-self.raio, self.raio, self.raio]
        ]
        faces = [
            [0, 1, 2, 3],  # Face frontal
            [1, 5, 6, 2],  # Face direita
            [5, 4, 7, 6],  # Face traseira
            [4, 0, 3, 7],  # Face esquerda
            [3, 2, 6, 7],  # Face superior
            [4, 5, 1, 0]  # Face inferior
        ]
        normais = [
            [0, 0, -1],
            [1, 0, 0],
            [0, 0, 1],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0]
        ]

        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)

        if self.texture_atlas:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_atlas.texture_id)

        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glNormal3fv(normais[i])
            uvs = self.texture_atlas.get_uv_coords(self.texture_indices[i])
            for j, vertex in enumerate(face):
                glTexCoord2fv(uvs[j])
                glVertex3fv(vertices[vertex])
        glEnd()

        if self.texture_atlas:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()