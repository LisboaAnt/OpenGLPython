import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Skybox:
    def __init__(self, size):
        self.size = size
        self.texture0 = self.load_texture(0)
        self.texture1 = self.load_texture(1)
        self.texture2 = self.load_texture(2)
        self.texture3 = self.load_texture(3)
        self.texture4 = self.load_texture(4)
        self.texture5 = self.load_texture(5)
        self.id = 1

    def load_texture(self, number):
        # Carrega textura para o Skybox

        texture_path = [
                        './imgs/skybox/skyboxF.png',
                        './imgs/skybox/skyboxBack.png',
                        './imgs/skybox/skyboxL.png',
                        './imgs/skybox/skyboxR.png', #R
                        './imgs/skybox/skyboxB.png', # 3
                        './imgs/skybox/skyboxT.png', # 4
                        ]

        image = Image.open(texture_path[number]).convert('RGBA')  # Converter para RGBA
        image = image.rotate(-90*(number))
        img_data = np.array(list(image.getdata()), dtype=np.uint8)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Carregar a textura
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # Configurar parâmetros de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        return texture

    def draw(self):
        # Lado1
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture0)

        glBegin(GL_QUADS)
        glTexCoord2f(1, 0), glVertex3f(self.size, -self.size, -self.size)
        glTexCoord2f(1, 1), glVertex3f(self.size, self.size, -self.size)
        glTexCoord2f(0, 1), glVertex3f(self.size, self.size, self.size)
        glTexCoord2f(0, 0), glVertex3f(self.size, -self.size, self.size)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Lado2
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture1)

        glBegin(GL_QUADS)
        glTexCoord2f(1, 0), glVertex3f(-self.size, -self.size, self.size)
        glTexCoord2f(1, 1), glVertex3f(-self.size, self.size, self.size)
        glTexCoord2f(0, 1), glVertex3f(-self.size, self.size, -self.size)
        glTexCoord2f(0, 0), glVertex3f(-self.size, -self.size, -self.size)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Lado3
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture2)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0), glVertex3f(-self.size, self.size, -self.size)
        glTexCoord2f(1, 0), glVertex3f(self.size, self.size, -self.size)
        glTexCoord2f(1, 1), glVertex3f(self.size, self.size, self.size)
        glTexCoord2f(0, 1), glVertex3f(-self.size, self.size, self.size)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Lado4
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture3)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0), glVertex3f(-self.size, -self.size, self.size)
        glTexCoord2f(1, 0), glVertex3f(self.size, -self.size, self.size)
        glTexCoord2f(1, 1), glVertex3f(self.size, -self.size, -self.size)
        glTexCoord2f(0, 1), glVertex3f(-self.size, -self.size, -self.size)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Down
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture4)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-self.size, -self.size, -self.size)
        glTexCoord2f(1, 0)
        glVertex3f(self.size, -self.size, -self.size)
        glTexCoord2f(1, 1)
        glVertex3f(self.size, self.size, -self.size)
        glTexCoord2f(0, 1)
        glVertex3f(-self.size, self.size, -self.size)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Up
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture5)

        glBegin(GL_QUADS)
        glTexCoord2f(1, 0)
        glVertex3f(self.size, -self.size, self.size)
        glTexCoord2f(0, 0)
        glVertex3f(-self.size, -self.size, self.size)
        glTexCoord2f(0, 1)
        glVertex3f(-self.size, self.size, self.size)
        glTexCoord2f(1, 1)
        glVertex3f(self.size, self.size, self.size)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        glEnable(GL_LIGHTING)
