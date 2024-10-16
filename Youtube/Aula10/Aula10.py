import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

from cubo import Cubo
from esfera import Esfera

from camera import Camera
from iluminacao import Iluminacao

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600
window = glfw.create_window(width, height, "Aula 3", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)
glfw.swap_interval(1)

glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

camera = Camera(width, height)
luz = Iluminacao()

cubo = Cubo()
esfera = Esfera()

glClearColor(0, 0, 0, 1)
glfw.set_key_callback(window, camera.key_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)



while not glfw.window_should_close(window):
    glfw.poll_events()
    camera.process_input(window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.update_camera()

    cubo.draw(0, 0, 0)

    esfera.draw(3, 0, 0)

    #luz.configurar_luz_potual(GL_LIGHT2, [2, 1, 0], [0.6, 0.2, 0.2], 0.1)

    #luz.configurar_luz_potual(GL_LIGHT3, [0, 1, 2], [0.2, 0.2, 1], 0.1)

    luz.configurar_luz_potual(GL_LIGHT4, [0, 1, -2], [0.2, 0.6, 0.2], 0.1)

    luz.configurar_luz_direcional(GL_LIGHT5, [1, 1, 1], [0.5, 0.5, 0.5], 0.8)

    #luz.configurar_luz_spot(GL_LIGHT6, [0, 0, -5], [0, -1, 1], [0.5, 0.5, 0.5], 1, 50, 20)


    glfw.swap_buffers(window)

glfw.terminate()
