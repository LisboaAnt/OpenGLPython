import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from obstacle import Obstacle


class Camera:
    def __init__(self, keys, width, height, x_size, y_size, z_size, id=1):
        # Variáveis da câmera
        self.camera_pos = np.array([0.0, 0.0, 0])
        self.camera_front = np.array([0.0, 0.0, -1.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.yaw, self.pitch = -90.0, 0.0  # Ângulos de orientação da câmera
        self.camera_speed = 0.005
        self.keys = keys

        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

        self.id = id

        self.width = width
        self.height = height

        # Variáveis Do Mause
        self.first_mouse = True  # Indicador para verificar se é a primeira vez que o mouse é movido
        self.cursor_disabled = False  # Indicador se o cursor está desativado
        self.esc_pressed = False  # Indicador se a tecla ESC está pressionada
        self.sensitivity = 0.1
        self.last_x, self.last_y = self.width / 2, self.height / 2

    def camera(self):
        glLoadIdentity()
        camera_target = self.camera_pos + self.camera_front
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2], camera_target[0], camera_target[1], camera_target[2],
                  self.camera_up[0], self.camera_up[1], self.camera_up[2])
        glTranslatef(0, 0, self.z_size)


    def mouse_callback(self, window, xpos, ypos):

        # Se o cursor não estiver desativado, não faz nada com o movimento do mouse
        if not self.cursor_disabled:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        # Calcula o deslocamento do mouse em relação à última posição conhecida
        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos

        # Atualiza as últimas coordenadas do mouse
        self.last_x = xpos
        self.last_y = ypos

        # Aplica a sensibilidade do mouse aos deslocamentos
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        # Atualiza os ângulos de orientação da câmera com base no deslocamento do mouse
        self.yaw += xoffset
        self.pitch += yoffset

        # Limita o ângulo 'pitch' para não ultrapassar os limites superiores e inferiores
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.camera_front = direction / np.linalg.norm(direction)

    def process_input(self, window, obstacles):
        new_pos = self.camera_pos.copy()
        moved = False  # Variável para verificar se houve movimento

        if self.keys.get(glfw.KEY_W, False):
            new_pos += self.camera_speed * self.camera_front
            moved = True
        if self.keys.get(glfw.KEY_S, False):
            new_pos -= self.camera_speed * self.camera_front
            moved = True
        if self.keys.get(glfw.KEY_A, False):
            new_pos -= np.cross(self.camera_front, self.camera_up) * self.camera_speed
            moved = True
        if self.keys.get(glfw.KEY_D, False):
            new_pos += np.cross(self.camera_front, self.camera_up) * self.camera_speed
            moved = True

        if moved:  # Verifica colisão apenas se houve movimento
            if not self.check_collision(new_pos[0], new_pos[1], new_pos[2], obstacles):
                self.camera_pos = new_pos
                self.atualizar_obstaculos(obstacles)  # Atualiza obstáculos apenas se a moto se moveu

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not self.esc_pressed:
            self.cursor_disabled = not self.cursor_disabled
            mode = glfw.CURSOR_DISABLED if self.cursor_disabled else glfw.CURSOR_NORMAL
            glfw.set_input_mode(window, glfw.CURSOR, mode)
            self.esc_pressed = True
            self.first_mouse = self.cursor_disabled
            if not self.cursor_disabled:
                glfw.set_cursor_pos(window, self.last_x, self.last_y)
        elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
            self.esc_pressed = False

    def check_collision(self, new_x, new_y, new_z, obstacles):
        for obstacle in obstacles:
            if obstacle.id == self.id:
                continue  # Ignora a colisão com a própria câmera

            # Verifica a colisão com obstáculos no espaço tridimensional, considerando centralização
            if (new_x + self.x_size / 2 > obstacle.x and new_x - self.x_size / 2 < obstacle.x + obstacle.width and
                    new_y + self.y_size / 2 > obstacle.y and new_y - self.y_size / 2 < obstacle.y + obstacle.height and
                    new_z + self.z_size / 2 > obstacle.z and new_z - self.z_size / 2 < obstacle.z + obstacle.depth):
                return True
        return False

    def atualizar_obstaculos(self, obstacles):
        for i, obstacle in enumerate(obstacles):
            if obstacle.id == self.id:
                # Centralizar a hitbox em relação à câmera
                obstacles[i] = Obstacle(
                    self.camera_pos[0] - self.x_size / 2,
                    self.camera_pos[1] - self.y_size / 2,
                    self.camera_pos[2] - self.z_size / 2,
                    self.x_size, self.y_size, self.z_size, id=self.id
                )
    def get_hitbox(self):
        # Retorna os parâmetros para a criação de um Obstacle
        return (
            self.camera_pos[0] - self.x_size / 2,  # x
            self.camera_pos[1] - self.y_size / 2,  # y
            self.camera_pos[2] - self.y_size / 2,  # z
            self.x_size,  # width
            self.y_size,  # height
            self.z_size   # depth
        )