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


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
vertices = np.array([
    [-0.5, 0.5, 0.0], # E S
    [-0.5, 0.0, 0.0], # E I
    [0.5, 0.0, 0.0], # D I
    [0.5, 0.5, 0.0],  # D S
])
def quads():
    glColor4f(1, 0, 0, 0.8)
    glBegin(GL_QUADS)
    for vertex in vertices:
        glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()
def trangulos():
    glBegin(GL_TRIANGLES)
    for vertex in vertices:
        glColor3f(vertex[0]+0.5, vertex[1] + 0.5, vertex[2])
        glVertex3f(vertex[0], vertex[1] - 0.6, vertex[2])
    glEnd()
def circulo(x, y, raio, segments):
    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        angle = 2 * np.pi * i/segments
        glVertex2f(x + np.cos(angle) * raio, y + np.sin(angle) * raio)
    glEnd()

glClearColor(0, 0.2, 0.5, 1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    circulo(0, 0, 0.1, 10)

    glfw.swap_buffers(window)
glfw.terminate()