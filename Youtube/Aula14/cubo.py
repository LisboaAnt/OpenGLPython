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
            [-self.raio, -self.raio, -self.raio],  # 0: Inferior Esquerdo Frontal
            [-self.raio, self.raio, -self.raio],  # 1: Superior Esquerdo Frontal
            [self.raio, self.raio, -self.raio],  # 2: Superior Direito Frontal
            [self.raio, -self.raio, -self.raio],  # 3: Inferior Direito Frontal
            [-self.raio, -self.raio, self.raio],  # 4: Inferior Esquerdo Traseiro
            [-self.raio, self.raio, self.raio],  # 5: Superior Esquerdo Traseiro
            [self.raio, self.raio, self.raio],  # 6: Superior Direito Traseiro
            [self.raio, -self.raio, self.raio]  # 7: Inferior Direito Traseiro
        ]

        faces = [
            [3, 0, 1, 2],  # Face frontal (anti-horário)
            [7, 3, 2, 6],  # Face direita (anti-horário)
            [4, 7, 6, 5],  # Face traseira (anti-horário)
            [0, 4, 5, 1],  # Face esquerda (anti-horário)
            [1, 5, 6, 2],  # Face superior (anti-horário)
            [4, 0, 3, 7]  # Face inferior (anti-horário)
        ]

        normais = [
            [0, 0, -1],  # Normal para a face frontal
            [1, 0, 0],  # Normal para a face direita
            [0, 0, 1],  # Normal para a face traseira
            [-1, 0, 0],  # Normal para a face esquerda
            [0, 1, 0],  # Normal para a face superior
            [0, -1, 0]  # Normal para a face inferior
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