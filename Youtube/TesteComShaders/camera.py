import numpy as np
import glfw
from OpenGL.GL import *
import math

class Camera:
    def __init__(self, width, height):
        self.position = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self.world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 0.05
        self.sensitivity = 0.1
        
        self.keys = {}
        self.first_mouse = True
        self.last_x = width / 2
        self.last_y = height / 2
        self.cursor_disabled = False
        self.esc_pressed = False
        
        self.update_camera_vectors()
        
    def update_camera_vectors(self):
        # Calcula o vetor front
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)
        
        # Recalcula os vetores right e up
        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)
        
        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)
    
    def get_view_matrix(self):
        # Cria a matriz de visualização
        view = np.identity(4, dtype=np.float32)
        
        # Primeiro, calculamos o vetor z (direção oposta ao front)
        z = -self.front
        z = z / np.linalg.norm(z)
        
        # Calculamos o vetor x (right)
        x = np.cross(self.up, z)
        x = x / np.linalg.norm(x)
        
        # Calculamos o vetor y (up)
        y = np.cross(z, x)
        
        # Construímos a matriz de rotação
        view[0, 0:3] = x
        view[1, 0:3] = y
        view[2, 0:3] = z
        
        # Adicionamos a translação
        view[0, 3] = -np.dot(x, self.position)
        view[1, 3] = -np.dot(y, self.position)
        view[2, 3] = -np.dot(z, self.position)
        
        return view
    
    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False
    
    def process_input(self, window):
        # Movimento da câmera
        if self.keys.get(glfw.KEY_W, False):
            self.position += self.speed * self.front
        if self.keys.get(glfw.KEY_S, False):
            self.position -= self.speed * self.front
        if self.keys.get(glfw.KEY_A, False):
            self.position -= self.speed * self.right
        if self.keys.get(glfw.KEY_D, False):
            self.position += self.speed * self.right
        
        # Ativar/desativar o cursor
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not self.esc_pressed:
            self.cursor_disabled = not self.cursor_disabled
            mode = glfw.CURSOR_DISABLED if self.cursor_disabled else glfw.CURSOR_NORMAL
            glfw.set_input_mode(window, glfw.CURSOR, mode)
            self.esc_pressed = True
            self.first_mouse = self.cursor_disabled
        elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
            self.esc_pressed = False
    
    def mouse_callback(self, window, xpos, ypos):
        if not self.cursor_disabled:
            return
            
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
        
        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos  # Invertido pois y cresce para baixo
        
        self.last_x = xpos
        self.last_y = ypos
        
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity
        
        self.yaw += xoffset
        self.pitch += yoffset
        
        # Limita o pitch para evitar que a câmera vire de cabeça para baixo
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0
            
        self.update_camera_vectors() 