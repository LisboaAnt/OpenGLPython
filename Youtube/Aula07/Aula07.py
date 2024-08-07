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
yaw, pitch = -90.0, 0.0  # Ângulos de orientação da câmera

camera_speed = 0.001
keys = {}

#Variáveis Do Mause
first_mouse = True  # Indicador para verificar se é a primeira vez que o mouse é movido
cursor_disabled = False  # Indicador se o cursor está desativado
esc_pressed = False  # Indicador se a tecla ESC está pressionada
sensitivity = 0.1
last_x, last_y = width / 2, height / 2

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
    global camera_pos, camera_front, camera_up, camera_speed, cursor_disabled, esc_pressed, first_mouse
    if keys.get(glfw.KEY_W, False):
        camera_pos += camera_speed * camera_front
    if keys.get(glfw.KEY_S, False):
        camera_pos -= camera_speed * camera_front
    if keys.get(glfw.KEY_A, False):
        camera_pos -= np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_D, False):
        camera_pos += np.cross(camera_front, camera_up) * camera_speed


    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not esc_pressed:
        cursor_disabled = not cursor_disabled
        mode = glfw.CURSOR_DISABLED if cursor_disabled else glfw.CURSOR_NORMAL
        glfw.set_input_mode(window, glfw.CURSOR, mode)
        esc_pressed = True
        first_mouse = cursor_disabled
        if not cursor_disabled:
            glfw.set_cursor_pos(window, last_x, last_y)
    elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
        esc_pressed = False


def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse, camera_front, cursor_disabled, sensitivity

    # Se o cursor não estiver desativado, não faz nada com o movimento do mouse
    if not cursor_disabled:
        return

    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    # Calcula o deslocamento do mouse em relação à última posição conhecida
    xoffset = xpos - last_x
    yoffset = last_y - ypos

    # Atualiza as últimas coordenadas do mouse
    last_x = xpos
    last_y = ypos

    # Aplica a sensibilidade do mouse aos deslocamentos
    xoffset *= sensitivity
    yoffset *= sensitivity

    # Atualiza os ângulos de orientação da câmera com base no deslocamento do mouse
    yaw += xoffset
    pitch += yoffset

    # Limita o ângulo 'pitch' para não ultrapassar os limites superiores e inferiores
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


cubo = Cubo()

glClearColor(0, 0.2, 0.5, 1)
glfw.set_key_callback(window, key_callback)
glfw.set_cursor_pos_callback(window, mouse_callback)


while not glfw.window_should_close(window):
    glfw.poll_events()
    process_input()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    camera()

    cubo.draw(0, 0, 0)

    glfw.swap_buffers(window)

glfw.terminate()