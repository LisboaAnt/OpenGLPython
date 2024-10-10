import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from cubo import Cubo
from camera import Camera
from Mesh import Mesh

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

glClearColor(0, 0, 0, 1)
glfw.set_key_callback(window, camera.key_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)

#LUZ
glEnable(GL_LIGHTING)
glEnable(GL_DEPTH_TEST)

glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.15, 0.15, 0.15, 1])


def configurar_luz_potual(light_id, position, color, intensity):
    glLightfv(light_id, GL_POSITION, position + [1])
    glLightfv(light_id, GL_DIFFUSE, [color[0] * intensity, color[1] * intensity, color[2] * intensity, 1])
    glLightfv(light_id, GL_SPECULAR, color + [1])

    glLightf(light_id, GL_CONSTANT_ATTENUATION, 0)
    glLightf(light_id, GL_LINEAR_ATTENUATION, 0.1)
    glLightf(light_id, GL_QUADRATIC_ATTENUATION, 0.01)

    glEnable(light_id)

    desenhar_esfera(position, color)


def desenhar_esfera(position, cor):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])

    shininess = 50

    glMaterialfv(GL_FRONT, GL_DIFFUSE, cor + [1])
    glMaterialfv(GL_FRONT, GL_SPECULAR, cor + [1])
    glMaterialfv(GL_FRONT, GL_AMBIENT, cor + [1])
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess)

    quadric = gluNewQuadric()
    gluSphere(quadric, 0.5, 32, 32)
    glPopMatrix()


def configurar_luz_direcional(light_id, direction, color, intensity):
    glLightfv(light_id, GL_POSITION, direction + [0])

    glLightfv(light_id, GL_DIFFUSE, [color[0] * intensity, color[1] * intensity, color[2] * intensity, 1])
    glLightfv(light_id, GL_SPECULAR, color + [1])

    glLightf(light_id, GL_CONSTANT_ATTENUATION, 1)
    glLightf(light_id, GL_LINEAR_ATTENUATION, 0)
    glLightf(light_id, GL_QUADRATIC_ATTENUATION, 0)

    glEnable(light_id)
    desenhar_linha(direction)


def desenhar_linha(direction):
    glPushMatrix()
    glTranslatef(0, 0, 0)

    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(direction[0], direction[1], direction[2])
    glEnd()
    glPopMatrix()


def configurar_luz_spot(light_id, position, direction, color, intensity, cutoff, exponent):
    glLightfv(light_id, GL_POSITION, position + [1])

    glLightfv(light_id, GL_SPOT_DIRECTION, direction)

    glLightfv(light_id, GL_DIFFUSE, [color[0] * intensity, color[1] * intensity, color[2] * intensity, 1])
    glLightfv(light_id, GL_SPECULAR, color + [1])

    glLightf(light_id, GL_SPOT_CUTOFF, cutoff)
    glLightf(light_id, GL_SPOT_EXPONENT, exponent)

    glLightf(light_id, GL_CONSTANT_ATTENUATION, 0)
    glLightf(light_id, GL_LINEAR_ATTENUATION, 0.1)
    glLightf(light_id, GL_QUADRATIC_ATTENUATION, 0.01)

    glEnable(light_id)

    desenhar_esfera(position, color)
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])

    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(direction[0], direction[1], direction[2])
    glEnd()
    glPopMatrix()


mesh = Mesh([-5, -5, 0], [5, 5, 0], [0, 0, -1], 10000)

while not glfw.window_should_close(window):
    glfw.poll_events()
    camera.process_input(window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.update_camera()

    #cubo.draw(0, 0, 0)

    #configurar_luz_potual(GL_LIGHT2, [2, 1, 0], [0.6, 0.2, 0.2], 0.1)

    #configurar_luz_potual(GL_LIGHT3, [0, 1, 2], [0.2, 0.2, 1], 0.1)

    #configurar_luz_potual(GL_LIGHT4, [0, 1, -2], [0.2, 0.6, 0.2], 0.1)

    configurar_luz_direcional(GL_LIGHT5, [1, 1, 1], [0.5, 0.5, 0.5], 0.2)

    configurar_luz_spot(GL_LIGHT6, [0, 0, -5], [0, -1, 1], [0.5, 0.5, 0.5], 1, 50, 20)

    glTranslatef(0, -2, 0)
    glRotatef(90, 1, 0, 0)
    mesh.draw()

    glfw.swap_buffers(window)

glfw.terminate()
