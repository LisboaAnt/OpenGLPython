import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Skybox:
    def __init__(self, size, day_atlas_path):
        self.size = size
        self.day_texture = self.load_texture_atlas(day_atlas_path)  # Textura diurna
    def load_texture_atlas(self, texture):
        # Carrega o atlas de textura
        image = Image.open(texture).convert('RGBA')  # Converter para RGBA

        # Inverte a imagem horizontalmente (o que está em cima vai para baixo e vice-versa)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

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
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)

        # Misturar as texturas diurna e noturna com base no fator alpha
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.day_texture)
        glColor4f(1.0, 1.0, 1.0, 1.0)  # Aplicar transparência para a textura diurna


        # Lado1 (Frente)
        glBegin(GL_QUADS)
        glTexCoord2f(1 / 3, 0), glVertex3f(self.size, -self.size, self.size)  # Vértice inferior direito da face frontal
        glTexCoord2f(1 / 3, 0.5), glVertex3f(self.size, self.size, self.size)  # Vértice superior direito da face frontal
        glTexCoord2f(0, 0.5), glVertex3f(self.size, self.size,-self.size)  # Vértice superior esquerdo da face frontal
        glTexCoord2f(0, 0), glVertex3f(self.size, -self.size,-self.size)  # Vértice inferior esquerdo da face frontal
        glEnd()

        # Lado2 (Trás)
        glBegin(GL_QUADS)
        glTexCoord2f(1/3, 1/2), glVertex3f(-self.size, -self.size,-self.size)  # Vértice inferior direito da face traseira
        glTexCoord2f(1/3, 1), glVertex3f(-self.size, self.size,-self.size)  # Vértice superior direito da face traseira
        glTexCoord2f(0, 1), glVertex3f(-self.size, self.size,self.size)  # Vértice superior esquerdo da face traseira
        glTexCoord2f(0, 1/2), glVertex3f(-self.size, -self.size,self.size)  # Vértice inferior esquerdo da face traseira
        glEnd()

        # ESQUERDA
        glBegin(GL_QUADS)
        glTexCoord2f(3/3, 1), glVertex3f(self.size, self.size, -self.size)  # Vértice inferior direito da base
        glTexCoord2f(2/3, 1), glVertex3f(-self.size, self.size, -self.size)  # Vértice superior direito da base
        glTexCoord2f(2/3, 0.5), glVertex3f(-self.size, -self.size, -self.size)  # Vértice superior esquerdo da base
        glTexCoord2f(3/3, 0.5), glVertex3f(self.size, -self.size, -self.size)  # Vértice inferior esquerdo da base
        glEnd()

        # DIREITA
        glBegin(GL_QUADS)
        glTexCoord2f(2/3, 1/2), glVertex3f(-self.size, -self.size, self.size)  # Vértice inferior direito
        glTexCoord2f(2/3, 1), glVertex3f(-self.size, self.size, self.size)  # Vértice superior direito
        glTexCoord2f(1/3, 1), glVertex3f(self.size, self.size, self.size)  # Vértice superior esquerdo
        glTexCoord2f(1/3, 1/2), glVertex3f(self.size, -self.size, self.size)  # Vértice inferior esquerdo
        glEnd()

        # TOP
        glBegin(GL_QUADS)
        glTexCoord2f(2/3, 0), glVertex3f(-self.size, self.size,-self.size)  # Vértice inferior direito da face esquerda
        glTexCoord2f(2/3, 0.5), glVertex3f(self.size, self.size,-self.size)  # Vértice superior direito da face esquerda
        glTexCoord2f(1/3, 0.5), glVertex3f(self.size, self.size,self.size)  # Vértice superior esquerdo da face esquerda
        glTexCoord2f(1/3, 0), glVertex3f(-self.size, self.size,self.size)  # Vértice inferior esquerdo da face esquerda
        glEnd()

        # DOWN
        glBegin(GL_QUADS)
        glTexCoord2f(1, 1 / 2), glVertex3f(-self.size, -self.size, -self.size)  # Vértice 2 -> Vértice 1
        glTexCoord2f(2 / 3, 1 / 2), glVertex3f(-self.size, -self.size, self.size)  # Vértice 3 -> Vértice 2
        glTexCoord2f(2 / 3, 0), glVertex3f(self.size, -self.size, self.size)  # Vértice 4 -> Vértice 3
        glTexCoord2f(1, 0), glVertex3f(self.size, -self.size, -self.size)  # Vértice 1 -> Vértice 4
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
