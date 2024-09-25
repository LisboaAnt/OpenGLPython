from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import glfw
import pywavefront
import pywavefront.visualization

from Obstacles import Obstacle


class Moto:
    width, height = 800, 600

    @staticmethod
    def load_texture(number):
        if number == 1:
            texture = pywavefront.Wavefront('load_obj/LightCyclePlayer.obj', collect_faces=True)
        else:
            texture = pywavefront.Wavefront('load_obj/LightCycleIA.obj', collect_faces=True)
        return texture

    def __init__(self, x=width / 2, y=height / 2, x_size=100, y_size=100,HP = 0,trajetoria = 0, alturaCam=120, moto_angle=0.0, id=None):
        self.moto_texture = Moto.load_texture(id)  # TEXTURA
        self.moto_angle = moto_angle  # Ângulo da moto X/Y
        self.moto_position = [x, y]  # Posicao
        self.inclinacaoDaMoto = 0
        self.inclinacaoVelocidade = 0.05

        self.moto_speed = 5  # Velocidade padrao de movimento
        self.moto_speed_angle = 1.5  # Velocidade rotacao padrao
        self.camera_distance = -280  # Distância da câmera ao moto
        self.camera_angle = 45.0  # Ângulo de inclinação da câmera
        self.camera_height = alturaCam  # Altura da câmera
        self.id = id  # Identificador único para a moto

        self.cameraType = True

        self.trajetoria = trajetoria
        self.hp = HP
        self.x_size = x_size
        self.y_size = y_size

    def movimento(self, window, dois, obstacles):
        moved = False  # Flag para indicar se a moto se
        DiminuirRotacao = False  # Diminue a velocidade de rotacionar a moto
        target_inclinacao = 0  # Valor alvo da inclinação

        # Sempre se movimenta para frente
        new_x = self.moto_position[0] + self.moto_speed * math.cos(math.radians(self.moto_angle))
        new_y = self.moto_position[1] + self.moto_speed * math.sin(math.radians(self.moto_angle))
        if not self.check_collision(new_x, new_y, obstacles):
            self.moto_position[0] = new_x
            self.moto_position[1] = new_y
            moved = True

        if dois:  # MOTO TELA 2 UP,LEFT,RIGHT
            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:  # AUMENTA VELOCIDADE
                new_x = self.moto_position[0] + (self.moto_speed / 1) * math.cos(math.radians(self.moto_angle))
                new_y = self.moto_position[1] + (self.moto_speed / 1) * math.sin(math.radians(self.moto_angle))
                if not self.check_collision(new_x, new_y, obstacles):
                    self.moto_position[0] = new_x
                    self.moto_position[1] = new_y
                    moved = True
                    DiminuirRotacao = True
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                self.moto_angle += self.moto_speed_angle / (2 if DiminuirRotacao else 1)
                target_inclinacao = 5 if DiminuirRotacao else 10

            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.moto_angle -= self.moto_speed_angle / (2 if DiminuirRotacao else 1)
                target_inclinacao = -5 if DiminuirRotacao else -10

            if glfw.get_key(window, glfw.KEY_V) == glfw.PRESS:
                self.cameraType = not self.cameraType
                if self.cameraType:
                    self.camera_height = 3000
                else:
                    self.camera_height = 120


        else:  # Controle com teclas W, A, D

            if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
                new_x = self.moto_position[0] + (self.moto_speed / 1) * math.cos(math.radians(self.moto_angle))
                new_y = self.moto_position[1] + (self.moto_speed / 1) * math.sin(math.radians(self.moto_angle))
                if not self.check_collision(new_x, new_y, obstacles):
                    self.moto_position[0] = new_x
                    self.moto_position[1] = new_y
                    moved = True
                    DiminuirRotacao = True

            if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
                self.moto_angle += self.moto_speed_angle / (2 if DiminuirRotacao else 1)
                target_inclinacao = 5 if DiminuirRotacao else 10

            if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
                self.moto_angle -= self.moto_speed_angle / (2 if DiminuirRotacao else 1)
                target_inclinacao = -5 if DiminuirRotacao else -10

            if glfw.get_key(window, glfw.KEY_C) == glfw.PRESS:
                self.cameraType = not self.cameraType
                if self.cameraType:
                    self.camera_height = 3000
                else:
                    self.camera_height = 120

        # Suaviza a inclinação da moto
        self.inclinacaoDaMoto += (target_inclinacao - self.inclinacaoDaMoto) * self.inclinacaoVelocidade
        if moved:
            self.atualizar_obstaculos(obstacles)  # Atualiza obstáculos apenas se a moto se moveu

    def check_collision(self, new_x, new_y, obstacles):
        for obstacle in obstacles:
            if obstacle.id == self.id:
                continue

            if obstacle.id == 5:
                if (new_x + self.x_size / 2 >= obstacle.x and new_x - self.x_size / 2 <= obstacle.x + obstacle.width and
                        new_y + self.y_size / 2 >= obstacle.y and new_y - self.y_size / 2 <= obstacle.y + obstacle.height):
                    self.trajetoria.max_points = 90
                    return False

            # Verifica a colisão com obstáculos
            if (new_x + self.x_size / 2 >= obstacle.x and new_x - self.x_size / 2 <= obstacle.x + obstacle.width and
                    new_y + self.y_size / 2 >= obstacle.y and new_y - self.y_size / 2 <= obstacle.y + obstacle.height):

                if self.id == 1:
                    self.moto_angle = 180
                    self.hp[0] = self.hp[0] - 1
                    self.moto_position = [2000, 0]
                    self.trajetoria.reset_points()
                else:
                    self.moto_angle = 0
                    self.hp[0] = self.hp[0] - 1
                    self.moto_position = [-2000, 0]
                    self.trajetoria.reset_points()
                return True
        return False

    def desenha(self):
        glPushMatrix()

        # Translada e escala a moto
        glTranslatef(self.moto_position[0], self.moto_position[1], 20)
        glScalef(20, 20, 20)
        glRotatef(-90, 0, 1, 0)
        glRotatef(-90, 0, 0, 1)
        glRotatef(self.moto_angle, 0, 1, 0)
        glRotatef(self.inclinacaoDaMoto, 0, 0, 1)

        # Desenha a moto
        pywavefront.visualization.draw(self.moto_texture)

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

    def get_back_position(self):  # Depois corrigir bug que o rastro não sai exatamente do ponto final da moto
        half_size = self.y_size / 1.5
        back_x = self.moto_position[0] - half_size * math.cos(math.radians(self.moto_angle))
        back_y = self.moto_position[1] - half_size * math.sin(math.radians(self.moto_angle))
        return back_x, back_y
