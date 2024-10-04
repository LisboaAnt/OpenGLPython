import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from cubo import Cubo
from camera import Camera
import numpy as np

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

camera = Camera(width, height)
cubo = Cubo()

glClearColor(0, 0.2, 0.5, 1)
glfw.set_key_callback(window, camera.key_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)

# LUZ
glEnable(GL_LIGHTING)
glEnable(GL_DEPTH_TEST)

# Configurar luz ambiente global
global_ambient = [0.15, 0.15, 0.15, 1]
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)


def configurar_luz(light_id, position, color, intensity):
    # Definição das propriedades da luz
    glLightfv(light_id, GL_POSITION, [position[0], position[1], position[2], 1.0])
    glLightfv(light_id, GL_DIFFUSE, [color[0] * intensity, color[1] * intensity, color[2] * intensity, 1.0])
    glLightfv(light_id, GL_SPECULAR, [color[0], color[1], color[2], 1.0])

    # Ajustar a atenuação da luz
    glLightf(light_id, GL_CONSTANT_ATTENUATION, 0.0)  # Diminuir a constante
    glLightf(light_id, GL_LINEAR_ATTENUATION, 0.1)  # Ativar atenuação linear (experimente valores diferentes)
    glLightf(light_id, GL_QUADRATIC_ATTENUATION, 0.01)  # Atenuação quadrática mais leve

    # Habilitar a luz
    glEnable(light_id)


def desenhar_esfera(position, cor):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])  # Move para a posição da luz

    shininess = 50.0  # Brilho do material

    # Define o material
    glMaterialfv(GL_FRONT, GL_AMBIENT, cor)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, cor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, cor)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

    # Desenha a esfera
    quadric = gluNewQuadric()
    gluSphere(quadric, 1, 32, 32)  # RAIO, PAREDES

    glPopMatrix()


posicao1 = [4, 0, 0]

posicao2 = [10, 0, 6]

while not glfw.window_should_close(window):
    glfw.poll_events()
    camera.process_input(window)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.update_view()

    cubo.draw(0, 0, 0)

    configurar_luz(GL_LIGHT2, posicao1, [0.4, 0, 0], 1)
    desenhar_esfera(posicao1, [1, 0.5, 0.5])

    configurar_luz(GL_LIGHT3, posicao2, [0, 0, 0.4], 1)
    desenhar_esfera(posicao2, [0.5, 0.5, 1])

    configurar_luz(GL_LIGHT4, [0, 10, 0], [1, 1, 1], 1)
    desenhar_esfera([0, 10, 0], [1, 1, 1])

    glfw.swap_buffers(window)

glfw.terminate()
