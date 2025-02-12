import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image


def load_texture(texture):
    image = Image.open(texture).convert('RGBA')

    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    img_data = np.array(list(image.getdata()), np.uint8)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texture_id


class Skybox:
    def __init__(self, size, texture):
        self.size = size
        self.texture = load_texture(texture)

    def draw(self):
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.day_texture)
        glColor4f(1.0, 1.0, 1.0, 1.0)

        # Definição dos vértices do cubo (posição relativa ao centro)
        vertices = [
            (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1),  # Frente
            (-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)  # Trás
        ]

        # Índices que formam as faces do cubo
        faces = [
            (0, 1, 2, 3),  # Frente
            (5, 4, 7, 6),  # Trás
            (3, 2, 5, 4),  # Esquerda
            (6, 7, 0, 1),  # Direita
            (1, 6, 5, 2),  # Topo
            (3, 4, 7, 0)  # Base
        ]

        # Coordenadas de textura padrão (supondo mapeamento cúbico)
        tex_coords = [
            (1, 0), (1, 1), (0, 1), (0, 0)  # Cada face usa esse padrão
        ]

        glBegin(GL_QUADS)
        for face in faces:
            for i, index in enumerate(face):
                glTexCoord2f(*tex_coords[i])  # Mapeamento de textura
                glVertex3f(*(self.size * v for v in vertices[index]))  # Ajuste pelo tamanho do cubo
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
