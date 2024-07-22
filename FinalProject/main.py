import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

from cubo import Cubo
from Moto import Moto
from Obstacles import Obstacle

from background import draw_sand_background

# Inicialização do GLFW

if not glfw.init():
    raise Exception("Failed to initialize GLFW")

width, height = 800, 600
window = glfw.create_window(width * 2, height, "Trabalho de Álgebra", None, None)  # Janela dividida

if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

glfw.make_context_current(window)

cubo = Cubo(tamanho=50.0, cor=(0.5, 1, 1))
cubo.transladar(200.0, 200.0, 20.0)

# Loop principal do jogo

moto1 = Moto(100, 200, x_size=100, y_size=100, id=1)
moto2 = Moto(id=2)


# Obstacles
obstacles = [Obstacle(cubo.posicao[0]-cubo.tamanho, cubo.posicao[1]-cubo.tamanho, cubo.tamanho*2, cubo.tamanho*2)]

# Adiciona as motos como obstáculos
obstacles.append(Obstacle(moto1.tank_position[0] - moto1.x_size/2, moto1.tank_position[1] - moto1.y_size/2, moto1.x_size, moto1.y_size, id=moto1.id))
obstacles.append(Obstacle(moto2.tank_position[0] - moto2.x_size/2, moto2.tank_position[1] - moto2.y_size/2, moto2.x_size, moto2.y_size, id=moto2.id))


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
    draw_sand_background(width, height)

    # Desenha o cubo
    cubo.desenhar()
    for obstacle in obstacles:
        obstacle.desenha()
        obstacle.desenhar_hitbox()

    #Textura
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending



    # Desenha e move 1
    moto1.movimento(window, False, obstacles)
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
    draw_sand_background(width, height)

    # Desenha o cubo
    cubo.desenhar()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

    # Movimento e Desenho MOTO 2
    moto2.movimento(window, True, obstacles)
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
