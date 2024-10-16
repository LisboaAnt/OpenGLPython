from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image


class CuboA:
    def __init__(self, initial_position=[0.0, 0.0, 0.0], texture_file='minerio.jpg', atlas_size=(2, 2)):
        self.position = initial_position
        self.texture_id = None
        self.atlas_size = atlas_size  # Ex: (4, 4) para um atlas 4x4
        if texture_file:
            self.texture_id = self.load_texture(texture_file)

    def load_texture(self, texture_file):
        # Carregar a textura usando PIL
        image = Image.open(texture_file)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(image.getdata()), np.uint8)

        # Gerar e carregar a textura
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return texture_id

    def get_uv_coords(self, index):
        # Calcula as coordenadas UV para a célula index no atlas
        cols, rows = self.atlas_size
        col = index % cols
        row = index // cols

        u0 = col / cols
        v0 = row / rows
        u1 = (col + 1) / cols
        v1 = (row + 1) / rows

        return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

    def draw(self, x, y, z):
        vertices = [
            [-0.5, -0.5, -0.5],  # 0
            [0.5, -0.5, -0.5],  # 1
            [0.5, 0.5, -0.5],  # 2
            [-0.5, 0.5, -0.5],  # 3
            [-0.5, -0.5, 0.5],  # 4
            [0.5, -0.5, 0.5],  # 5
            [0.5, 0.5, 0.5],  # 6
            [-0.5, 0.5, 0.5],  # 7
        ]

        faces = [
            [0, 1, 2, 3],  # front
            [1, 5, 6, 2],  # right
            [5, 4, 7, 6],  # back
            [4, 0, 3, 7],  # left
            [3, 2, 6, 7],  # top
            [4, 5, 1, 0],  # bottom
        ]

        # Normais para cada face
        normais = [
            [0, 0, -1],  # front
            [1, 0, 0],  # right
            [0, 0, 1],  # back
            [-1, 0, 0],  # left
            [0, 1, 0],  # top
            [0, -1, 0],  # bottom
        ]

        # Defina os índices das texturas para cada face (cada face pode usar uma parte diferente do atlas)
        texture_indices = [2, 2, 2, 2, 2, 2]  # Exemplo: faces usam texturas diferentes

        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glNormal3fv(normais[i])
            uvs = self.get_uv_coords(texture_indices[i])
            for j, vertex in enumerate(face):
                glTexCoord2fv(uvs[j])  # Mapeamento UV da parte do atlas
                glVertex3fv(vertices[vertex])
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
