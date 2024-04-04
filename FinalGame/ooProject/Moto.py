import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import numpy as np


class Moto:
    width, height = 800, 600

    @staticmethod
    def load_texture(filename):
        image = Image.open(filename)
        image = image.convert("RGBA")
        width, height = image.size
        texture_data = np.array(list(image.getdata()), np.uint8)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        return texture

    def __init__(self):
        self.tank_texture = Moto.load_texture("pixil-frame-0.png")
        self.tank_angle = 0.0
        self.tank_position = [self.width / 2, self.height / 2]
        self.tank_speed = 0.1  # Velocidade do tanque
        self.camera_distance = -200.0  # Distância da câmera ao tanque
        self.camera_angle = 45.0  # Ângulo de inclinação da câmera
        self.camera_height = 80.0  # Altura da câmera acima do tanque

    def movimento(self, window):
        # Atualiza a posição do tanque com base nas teclas pressionadas
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.tank_angle += 0.05  # Gira o tanque para a esquerda
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.tank_angle -= 0.05  # Gira o tanque para a direita
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.tank_position[0] += self.tank_speed * math.cos(math.radians(self.tank_angle))
            self.tank_position[1] += self.tank_speed * math.sin(math.radians(self.tank_angle))
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.tank_position[0] -= self.tank_speed * math.cos(math.radians(self.tank_angle))
            self.tank_position[1] -= self.tank_speed * math.sin(math.radians(self.tank_angle))

    def desenha(self):
        # Desenha o tanque
        glPushMatrix()
        glTranslatef(self.tank_position[0], self.tank_position[1], 0)
        glRotatef(self.tank_angle, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, self.tank_texture)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-50, -30)
        glTexCoord2f(1, 0)
        glVertex2f(50, -30)
        glTexCoord2f(1, 1)
        glVertex2f(50, 30)
        glTexCoord2f(0, 1)
        glVertex2f(-50, 30)
        glEnd()

        glPopMatrix()
