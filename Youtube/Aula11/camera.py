import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Camera:
    def __init__(self, width, height):
        self.camera_pos = np.array([0.0, 0.0, 3])
        self.camera_front = np.array([0.0, 0.0, -1.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.yaw, self.pitch = -90.0, 0.0  # Ângulos de orientação da câmera

        self.camera_speed = 0.2
        self.keys = {}

        # Variáveis Do Mause
        self.first_mouse = True  # Indicador para verificar se é a primeira vez que o mouse é movido
        self.cursor_disabled = False  # Indicador se o cursor está desativado
        self.esc_pressed = False  # Indicador se a tecla ESC está pressionada
        self.sensitivity = 0.1
        self.last_x, self.last_y = width / 2, height / 2

    def update_camera(self):
        glLoadIdentity()
        camera_target = self.camera_pos + self.camera_front
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2], camera_target[0], camera_target[1],
                       camera_target[2], self.camera_up[0], self.camera_up[1], self.camera_up[2])

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def process_input(self, window):
        if self.keys.get(glfw.KEY_W, False):
            self.camera_pos += self.camera_speed * self.camera_front
        if self.keys.get(glfw.KEY_S, False):
            self.camera_pos -= self.camera_speed * self.camera_front
        if self.keys.get(glfw.KEY_A, False):
            self.camera_pos -= np.cross(self.camera_front, self.camera_up) * self.camera_speed
        if self.keys.get(glfw.KEY_D, False):
            self.camera_pos += np.cross(self.camera_front, self.camera_up) * self.camera_speed

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not self.esc_pressed:
            self.cursor_disabled = not self.cursor_disabled
            mode = glfw.CURSOR_DISABLED if self.cursor_disabled else glfw.CURSOR_NORMAL
            glfw.set_input_mode(window, glfw.CURSOR, mode)
            self.esc_pressed = True
            self.first_mouse = self.cursor_disabled
        elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
            self.esc_pressed = False

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
