import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from cubo import Cubo


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

#Variáveis da câmera
camera_pos = np.array([0.0, 0.0, 3])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
camera_speed = 0.001

keys = {}

def camera():
    global camera_pos, camera_front, camera_up
    glLoadIdentity()
    camera_target = camera_pos + camera_front
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], camera_target[0], camera_target[1], camera_target[2], camera_up[0], camera_up[1], camera_up[2])

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

def process_input():
    global camera_pos, camera_front, camera_up, camera_speed
    if keys.get(glfw.KEY_W, False):
        camera_pos += camera_speed * camera_front
    if keys.get(glfw.KEY_S, False):
        camera_pos -= camera_speed * camera_front
    if keys.get(glfw.KEY_A, False):
        camera_pos -= np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_D, False):
        camera_pos += np.cross(camera_front, camera_up) * camera_speed



cubo = Cubo()

glClearColor(0 , 0.2, 0.5, 1)
glfw.set_key_callback(window, key_callback)

while not glfw.window_should_close(window):
    glfw.poll_events()
    process_input()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    camera()

    cubo.draw(0, 0, 0)


    glfw.swap_buffers(window)
glfw.terminate()