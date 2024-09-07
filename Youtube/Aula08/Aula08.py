import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from obj_loader import ObjLoader  # Importando a classe ObjLoader

# Inicialização e configuração da janela
if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600
window = glfw.create_window(width, height, "Aula 8 - Carregando Modelos 3D", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)

# Configuração OpenGL
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Configuração da câmera
camera_pos = np.array([0.0, 0.0, 3])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw, pitch = -90.0, 0.0
camera_speed = 0.005
keys = {}

first_mouse = True
cursor_disabled = False
esc_pressed = False
sensitivity = 0.1
last_x, last_y = width / 2, height / 2

# Funções de manipulação da câmera
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

    if not cursor_disabled:
        return

    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos

    last_x = xpos
    last_y = ypos

    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    pitch = max(-89.0, min(89.0, pitch))

    front = np.array([
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
    ])
    camera_front = front / np.linalg.norm(front)

glfw.set_key_callback(window, key_callback)
glfw.set_cursor_pos_callback(window, mouse_callback)

# Carregar o modelo OBJ
obj_loader = ObjLoader('house_obj.obj')
obj_loader.load()

# Loop principal
while not glfw.window_should_close(window):
    process_input()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    camera()

    # Renderizar o objeto carregado
    obj_loader.render()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
