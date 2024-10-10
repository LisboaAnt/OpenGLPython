import glfw
from OpenGL.GL import *
import numpy as np


def init_glfw():
    if not glfw.init():
        return None
    window = glfw.create_window(800, 600, "Iluminação Simples", None, None)
    if not window:
        glfw.terminate()
        return None
    glfw.make_context_current(window)
    return window


def setup_lighting():
    # Ativar iluminação
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Configurar a posição da luz
    light_pos = [1.0, 1.0, 1.0, 0.0]  # Luz direcional
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    # Configurar a cor da luz
    ambient_light = [0.2, 0.2, 0.2, 1.0]
    diffuse_light = [1.0, 1.0, 1.0, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

    # Configurar material
    material_color = [0.8, 0.2, 0.2, 1.0]  # Cor do material
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_color)


def draw_cube():
    glBegin(GL_QUADS)

    # Frente
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)

    # Outras faces...
    # Adicione mais faces aqui para criar um cubo completo

    glEnd()


def main():
    window = init_glfw()
    glEnable(GL_DEPTH_TEST)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Posição da câmera
        glTranslatef(0.0, 0.0, -5.0)

        draw_cube()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
