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

def piramide():
    vertices = [
        [1, 1, 1],
        [-1, -1, 1],
        [-1, 1, -1],
        [1, -1, -1],
    ]
    faces = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3],
    ]
    cores = [
        [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0],
    ]
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glColor3fv(cores[vertex])
            glVertex3fv(vertices[vertex])
    glEnd()


def hexagonal(x, y, raio):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0, 1, 0)
    glVertex2f(x, y)
    for i in range(7):
        angulo = 2*np.pi * i/6
        glColor3f(i/6, 1-(i/6), 0.5)
        glVertex2f(x + np.cos(angulo) * raio, y + np.sin(angulo) * raio)
    glEnd()

def sphere(radius, slices, stacks):
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = radius * np.sin(lat0)
        zr0 = radius * np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = radius * np.sin(lat1)
        zr1 = radius * np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices+1):
            lng = 2 * np.pi * float(j) /slices
            x = np.cos(lng)
            y = np.sin(lng)
            glColor3f(j/ slices, i/stacks, 1 - (i/stacks))
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x*zr1, y*zr1, z1)
        glEnd()

glClearColor(0 , 0.2, 0.5, 1)
angle = 0

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0, 0, -20)
    glRotatef(angle, 1, 1, 1)

    sphere(3, 20, 20)

    angle +=0.05

    glfw.swap_buffers(window)
glfw.terminate()