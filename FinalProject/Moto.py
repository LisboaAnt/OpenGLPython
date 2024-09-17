from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import numpy as np
import glfw

from Obstacles import Obstacle


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

    def __init__(self, x=width / 2, y=height / 2, x_size=100, y_size=100, id=None):
        self.moto_texture = Moto.load_texture("./imgs/pixil-frame-0.png")  # Renomeado para moto_texture
        self.moto_angle = 0.0  # Ângulo da moto X/Y
        self.moto_position = [x, y]  # Posicao

        self.moto_speed = 0.5  # Velocidade padrao de movimento
        self.moto_speed_angle = 0.15    # Velocidade rotacao padrao
        self.camera_distance = -250  # Distância da câmera ao moto
        self.camera_angle = 45.0  # Ângulo de inclinação da câmera
        self.camera_height = 80.0  # Altura da câmera
        self.id = id  # Identificador único para a moto
        self.x_size = x_size
        self.y_size = y_size

    def movimento(self, window, dois, obstacles):
        moved = False  # Flag para indicar se a moto se
        DiminuirRotacao = False  # Diminue a velocidade de rotacionar a moto

        # Sempre se movimenta para frente
        new_x = self.moto_position[0] + self.moto_speed * math.cos(math.radians(self.moto_angle))
        new_y = self.moto_position[1] + self.moto_speed * math.sin(math.radians(self.moto_angle))
        if not self.check_collision(new_x, new_y, obstacles):
            self.moto_position[0] = new_x
            self.moto_position[1] = new_y
            moved = True

        if dois:    # MOTO TELA 2 UP,LEFT,RIGHT
            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS: # AUMENTA VELOCIDADE
                new_x = self.moto_position[0] + (self.moto_speed / 1) * math.cos(math.radians(self.moto_angle))
                new_y = self.moto_position[1] + (self.moto_speed / 1) * math.sin(math.radians(self.moto_angle))
                if not self.check_collision(new_x, new_y, obstacles):
                    self.moto_position[0] = new_x
                    self.moto_position[1] = new_y
                    moved = True
                    DiminuirRotacao = True
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:   # Gira a moto para a esquerda
                if DiminuirRotacao:
                    self.moto_angle += self.moto_speed_angle / 2
                else:
                    self.moto_angle += self.moto_speed_angle
            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:   # Gira a moto para a direita
                if DiminuirRotacao:
                    self.moto_angle -= self.moto_speed_angle / 2
                else:
                    self.moto_angle -= self.moto_speed_angle

        else:   # MOTO TELA 1 WAD
            if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:  # AUMENTA VELOCIDADE
                new_x = self.moto_position[0] + (self.moto_speed / 1) * math.cos(math.radians(self.moto_angle))
                new_y = self.moto_position[1] + (self.moto_speed / 1) * math.sin(math.radians(self.moto_angle))
                if not self.check_collision(new_x, new_y, obstacles):
                    self.moto_position[0] = new_x
                    self.moto_position[1] = new_y
                    moved = True
                    DiminuirRotacao = True
            if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:  # Gira a moto para a esquerda
                if DiminuirRotacao:
                    self.moto_angle += self.moto_speed_angle / 2
                else:
                    self.moto_angle += self.moto_speed_angle

            if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:  # Gira a moto para a direita
                if DiminuirRotacao:
                    self.moto_angle -= self.moto_speed_angle / 2
                else:
                    self.moto_angle -= self.moto_speed_angle

        if moved:
            self.atualizar_obstaculos(obstacles)  # Atualiza obstáculos apenas se a moto se moveu

    def check_collision(self, new_x, new_y, obstacles):
        for obstacle in obstacles:
            if obstacle.id == self.id:
                continue  # Ignora a colisão com a própria moto

            # Verifica a colisão com obstáculos
            if (new_x + self.x_size / 2 >= obstacle.x and new_x - self.x_size / 2 <= obstacle.x + obstacle.width and
                    new_y + self.y_size / 2 >= obstacle.y and new_y - self.y_size / 2 <= obstacle.y + obstacle.height):
                return True
        return False

    def desenha(self):
        # Desenha a moto
        glPushMatrix()
        glTranslatef(self.moto_position[0], self.moto_position[1], 1)
        glRotatef(self.moto_angle, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, self.moto_texture)  # Renomeado para moto_texture

        glColor3f(1, 1, 1)
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

    def calculate_camera_params(self):
        self.camera_angle = self.moto_angle  # Renomeado para moto_angle
        # Calcula os parâmetros da câmera com base nos atributos da instância de Moto
        camera_x = self.moto_position[0] + self.camera_distance * math.cos(math.radians(self.camera_angle))
        camera_y = self.moto_position[1] + self.camera_distance * math.sin(math.radians(self.camera_angle))
        camera_z = self.camera_height
        look_x, look_y, look_z = self.moto_position[0], self.moto_position[1], 0
        return (camera_x, camera_y, camera_z,
                look_x, look_y, look_z,
                0, 0, 1)

    def atualizar_obstaculos(self, obstacles):
        for i, obstacle in enumerate(obstacles):
            if obstacle.id == self.id:
                obstacles[i] = Obstacle(self.moto_position[0] - self.x_size / 2,
                                        self.moto_position[1] - self.y_size / 2, self.x_size, self.y_size, id=self.id)

    def get_back_position(self):    # Depois corrigir bug que o rastro não sai exatamente do ponto final da moto
        half_size = self.y_size / 1.5
        back_x = self.moto_position[0] - half_size * math.cos(math.radians(self.moto_angle))
        back_y = self.moto_position[1] - half_size * math.sin(math.radians(self.moto_angle))
        return back_x, back_y
