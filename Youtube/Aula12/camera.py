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

        self.camera_speed = 0.1
        self.keys = {}

        # Variáveis do mouse
        self.first_mouse = True  # Indicador para verificar se é a primeira vez que o mouse é movido
        self.cursor_disabled = False  # Indicador se o cursor está desativado
        self.esc_pressed = False  # Indicador se a tecla ESC está pressionada
        self.sensitivity = 0.1
        self.last_x, self.last_y = width / 2, height / 2

        # Variáveis de projeção
        self.width = width
        self.height = height
        self.update_projection()

    def update_projection(self):
        """Atualiza a matriz de projeção com base no tamanho atual da janela."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 50000.0)
        glMatrixMode(GL_MODELVIEW)

    def update_window_size(self, new_width, new_height):
        """Atualiza o tamanho da janela e a matriz de projeção."""
        self.width = new_width
        self.height = new_height
        self.update_projection()

    def update_camera(self):
        """Atualiza a matriz de visualização da câmera."""
        glLoadIdentity()
        camera_target = self.camera_pos + self.camera_front
        gluLookAt(
            self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],
            camera_target[0], camera_target[1], camera_target[2],
            self.camera_up[0], self.camera_up[1], self.camera_up[2]
        )

    def key_callback(self, window, key, scancode, action, mods):
        """Callback para eventos de teclado."""
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def process_input(self, window):
        """Processa as entradas do teclado para mover a câmera."""
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
        """Callback para eventos de movimento do mouse."""
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

        # Atualiza o vetor de direção da câmera
        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.camera_front = direction / np.linalg.norm(direction)