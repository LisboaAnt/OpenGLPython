import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Skybox:
    def __init__(self, size):
        self.size = size
        self.textures = self.load_textures()

    def load_textures(self):
        # Carregar as texturas do Skybox (6 imagens)
        faces = [
            './imgs/skybox.png', './imgs/skybox.png',
            './imgs/skybox.png', './imgs/skybox.png',
            './imgs/skybox.png', './imgs/skybox.png'
        ]
        textures = glGenTextures(6)
        for i, face in enumerate(faces):
            glBindTexture(GL_TEXTURE_2D, textures[i])
            image = Image.open(face)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = np.array(image, dtype=np.uint8)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return textures

    def draw(self):
        glPushMatrix()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        # Direita
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(self.size, -self.size, -self.size)
        glTexCoord2f(1, 0); glVertex3f(self.size, -self.size, self.size)
        glTexCoord2f(1, 1); glVertex3f(self.size, self.size, self.size)
        glTexCoord2f(0, 1); glVertex3f(self.size, self.size, -self.size)
        glEnd()

        # Esquerda
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-self.size, -self.size, self.size)
        glTexCoord2f(1, 0); glVertex3f(-self.size, -self.size, -self.size)
        glTexCoord2f(1, 1); glVertex3f(-self.size, self.size, -self.size)
        glTexCoord2f(0, 1); glVertex3f(-self.size, self.size, self.size)
        glEnd()

        # Topo
        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-self.size, self.size, -self.size)
        glTexCoord2f(1, 0); glVertex3f(self.size, self.size, -self.size)
        glTexCoord2f(1, 1); glVertex3f(self.size, self.size, self.size)
        glTexCoord2f(0, 1); glVertex3f(-self.size, self.size, self.size)
        glEnd()

        # Base
        glBindTexture(GL_TEXTURE_2D, self.textures[3])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-self.size, -self.size, self.size)
        glTexCoord2f(1, 0); glVertex3f(self.size, -self.size, self.size)
        glTexCoord2f(1, 1); glVertex3f(self.size, -self.size, -self.size)
        glTexCoord2f(0, 1); glVertex3f(-self.size, -self.size, -self.size)
        glEnd()

        # Frente
        glBindTexture(GL_TEXTURE_2D, self.textures[4])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-self.size, -self.size, -self.size)
        glTexCoord2f(1, 0); glVertex3f(self.size, -self.size, -self.size)
        glTexCoord2f(1, 1); glVertex3f(self.size, self.size, -self.size)
        glTexCoord2f(0, 1); glVertex3f(-self.size, self.size, -self.size)
        glEnd()

        # Trás
        glBindTexture(GL_TEXTURE_2D, self.textures[5])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(self.size, -self.size, self.size)
        glTexCoord2f(1, 0); glVertex3f(-self.size, -self.size, self.size)
        glTexCoord2f(1, 1); glVertex3f(-self.size, self.size, self.size)
        glTexCoord2f(0, 1); glVertex3f(self.size, self.size, self.size)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
