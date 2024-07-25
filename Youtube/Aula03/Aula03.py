import glfw
from OpenGL.GL import *
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
    [0.5, 0.5, 0.0], # D S
    [-0.5, 0.0, 0.0], # E I
    [0.5, 0.0, 0.0], # D I
])

def draw():
    glColor4f(1, 0, 0, 0.5)
    glBegin(GL_QUADS)
    for vertex in vertices:
        glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()


glClearColor(0, 0.2, 0.5, 1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    draw()


    glfw.swap_buffers(window)
glfw.terminate()