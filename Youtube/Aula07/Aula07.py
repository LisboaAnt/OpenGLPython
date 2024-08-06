import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

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

# Variáveis de controle da câmera
camera_pos = np.array([0.0, 0.0, 3.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
camera_speed = 0.05
yaw, pitch = -90.0, 0.0
last_x, last_y = width / 2, height / 2
first_mouse = True
cursor_disabled = True

def cube():
    vertices = [
        [-0.5, -0.5, -0.5],
        [0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5],
        [0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [-0.5, 0.5, 0.5],
    ]
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 3, 7, 4],
        [1, 2, 6, 5],
    ]
    colors = [
        [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [0.5, 0.5, 0.5], [1, 0.5, 0]
    ]

    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(colors[vertex])
            glVertex3fv(vertices[vertex])
    glEnd()

def camera():
    global camera_pos, camera_front, camera_up
    glLoadIdentity()
    camera_target = camera_pos + camera_front
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])

def key_callback(window, key, scancode, action, mods):
    global camera_pos, camera_front, camera_up, camera_speed, cursor_disabled
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:
            camera_pos += camera_speed * camera_front
        if key == glfw.KEY_S:
            camera_pos -= camera_speed * camera_front
        if key == glfw.KEY_A:
            camera_pos -= np.cross(camera_front, camera_up) * camera_speed
        if key == glfw.KEY_D:
            camera_pos += np.cross(camera_front, camera_up) * camera_speed
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            cursor_disabled = not cursor_disabled
            if cursor_disabled:
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            else:
                glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

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

glClearColor(0 , 0.2, 0.5, 1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    camera()
    cube()

    glfw.swap_buffers(window)

glfw.terminate()
