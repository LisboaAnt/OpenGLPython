import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from cube import Cube

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600
window = glfw.create_window(width, height, "Aula 3", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)

glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

camera_pos = np.array([0.0, 0.0, 3.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
camera_speed = 2.5  # Unidades por segundo
yaw, pitch = -90.0, 0.0
last_x, last_y = width / 2, height / 2
first_mouse = True
cursor_disabled = True
keys = {}


def camera():
    global camera_pos, camera_front, camera_up
    glLoadIdentity()
    camera_target = camera_pos + camera_front
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])


def key_callback(window, key, scancode, action, mods):
    global cursor_disabled
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        cursor_disabled = not cursor_disabled
        if cursor_disabled:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        else:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)


def process_input():
    global camera_pos, camera_front, camera_up, camera_speed
    velocity = camera_speed
    if keys.get(glfw.KEY_W, False):
        camera_pos += velocity * camera_front
    if keys.get(glfw.KEY_S, False):
        camera_pos -= velocity * camera_front
    if keys.get(glfw.KEY_A, False):
        camera_pos -= np.cross(camera_front, camera_up) * velocity
    if keys.get(glfw.KEY_D, False):
        camera_pos += np.cross(camera_front, camera_up) * velocity


def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse, camera_front
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos
    last_x = xpos
    last_y = ypos

    sensitivity = 0.1
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

    direction = np.array([
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
    ])
    camera_front = direction / np.linalg.norm(direction)


glfw.set_key_callback(window, key_callback)
glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

glClearColor(0, 0.2, 0.5, 1)

cube = Cube()

while not glfw.window_should_close(window):

    glfw.poll_events()
    process_input()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    camera()
    for i in range(10):
        cube.draw(i, i, i)
        cube.draw(-i, -i, -i)

    glfw.swap_buffers(window)

glfw.terminate()
