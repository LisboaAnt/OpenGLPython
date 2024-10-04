import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, width, height):
        self.camera_pos = np.array([0.0, 0.0, 3.0])
        self.camera_front = np.array([0.0, 0.0, -1.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.yaw, self.pitch = -90.0, 0.0

        self.camera_speed = 0.005
        self.sensitivity = 0.1

        self.keys = {}
        self.cursor_disabled = False
        self.first_mouse = True
        self.esc_pressed = False
        self.last_x = width / 2
        self.last_y = height / 2

    def update_view(self):
        glLoadIdentity()
        camera_target = self.camera_pos + self.camera_front
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],
                  camera_target[0], camera_target[1], camera_target[2],
                  self.camera_up[0], self.camera_up[1], self.camera_up[2])

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

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def mouse_callback(self, window, xpos, ypos):
        if not self.cursor_disabled:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos
        self.last_x = xpos
        self.last_y = ypos

        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

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
