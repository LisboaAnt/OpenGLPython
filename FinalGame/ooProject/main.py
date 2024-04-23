import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

from Moto import *  #Class moto

# Inicialização do GLFW

if not glfw.init():
    raise Exception("Failed to initialize GLFW")

width, height = 800, 600
window = glfw.create_window(width * 2, height, "Trabalho de Álgebra", None, None)  # Janela dividida

if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

glfw.make_context_current(window)


def draw_sand_background():
    glBegin(GL_QUADS)
    glColor3f(0.96, 0.87, 0.70)  # Cor de areia
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, height)
    glVertex2f(0, height)
glEnd()


# Loop principal do jogo

moto1 = Moto()
moto2 = Moto()

while not glfw.window_should_close(window):
    glfw.poll_events()
    # Limpa o buffer de cores e de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    #   CAMERA 1 ////////////////////////////////////////////////////////////////////////////////////////////////
    # Desenhar Camera 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000)
    gluLookAt(*moto1.calculate_camera_params())

    # Desenha o fundo de areia
    draw_sand_background()

    #Textura
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

    # Desenha e move 1
    moto1.movimento(window, False)
    moto1.desenha()

    # Desenha moto 2
    moto2.desenha()

    # Desabilita o blending e desativa a textura

    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

    #CAMERA 2 //////////////////////////////////////////////////////////////////////////////////////////////////////////

    # Desenhar CAMERA 2
    glViewport(width, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000)
    gluLookAt(*moto2.calculate_camera_params())

    # Desenha o fundo de areia
    draw_sand_background()


    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

    # Movimento e Desenho MOTO 2
    moto2.movimento(window, True)
    moto2.desenha()

    # Desenha MOTO 1
    moto1.desenha()
    # Desabilita o blending e desativa a textura
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

    # Troca os buffers e atualiza a janela
    glfw.swap_buffers(window)

# Finaliza o GLFW
glfw.terminate()
