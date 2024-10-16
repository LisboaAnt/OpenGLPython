from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image


class Cubo:
    def __init__(self, inital_position=[0.0, 0.0, 0.0], texture_file="grass.jpg"):
        self.position = inital_position
        self.texture_id = None
        if texture_file:
            self.texture_id = self.load_texture(texture_file)

    def load_texture(self, texture_file):
        image = Image.open(texture_file)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

        img_data = np.array(list(image.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return texture_id

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
            [0, 1, 2, 3],  # front
            [1, 5, 6, 2],  # dir
            [5, 4, 7, 6],  # tras
            [4, 0, 3, 7],  # esq
            [3, 2, 6, 7],  # sup
            [4, 5, 1, 0],  # inf
        ]

        normais = [
            [0, 0, -1],
            [1, 0, 0],
            [0, 0, 1],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0]
        ]

        uvs = [
            [0, 0], [1, 0], [1, 1], [0, 1],
            [0, 0], [1, 0], [1, 1], [0, 1],
            [0, 0], [1, 0], [1, 1], [0, 1],
            [0, 0], [1, 0], [1, 1], [0, 1],
            [0, 0], [1, 0], [1, 1], [0, 1],
            [0, 0], [1, 0], [1, 1], [0, 1],
        ]

        color = [1, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, color)
        glMaterialfv(GL_FRONT, GL_AMBIENT, color)
        glMaterialfv(GL_FRONT, GL_SHININESS, 100)

        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glNormal3fv(normais[i])
            for j, vertex in enumerate(face):
                glTexCoord2fv(uvs[j])
                glVertex3fv(vertices[vertex])
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
        glPopMatrix()
