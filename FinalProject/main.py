import glfw
import pygame
import time
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from PIL import Image

from Cubo import Cubo
from Moto import Moto
from Obstacles import Obstacle

from Trajetoria import Trajetoria

# MAPA
from Background import TronBackground
from Skybox import Skybox

# Menu
from Menu import MainMenu  # Importa a classe MainMenu

pygame.init()
pygame.font.init()

# Carregar uma fonte
font = pygame.font.SysFont("Arial", 48)
HP1 = 100
HP2 = 100

#intervalo para decrescer de HP
intervalo_atualizacao = 0.0000000000001


def render_text(text, x, y):
    # Renderizar o texto em uma superfície do pygame
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    # Configurar a projeção ortográfica para renderizar em 2D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)  # Aqui definimos uma tela de 800x600
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Renderizar a textura do texto
    glRasterPos2f(x, y)
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    # Restaurar a matriz original
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


# Inicializando a biblioteca GLFW
if not glfw.init():
    raise Exception("Falha ao inicializar o GLFW")
width, height = 800, 600
window = glfw.create_window(width , height, "TRON - OpenGL", None, None)  # Janela dividida
if not window:


    glfw.terminate()
    raise Exception("Falha ao criar a janela GLFW")



# Definir o ícone da janela
icon_path = "./imgs/icon.png"
glfw.set_window_icon(window, 1, Image.open(icon_path))

def framebuffer_size_callback(window, fb_width, fb_height):
    global width, height
    width, height = fb_width // 2, fb_height
    glViewport(0, 0, fb_width, fb_height)
    if glfw.get_window_attrib(window, glfw.MAXIMIZED):
        primary_monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(primary_monitor)
        glfw.set_window_size(window, mode.size.width, mode.size.height)

glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# Criar o menu inicial
menu = MainMenu(window)

# Configurar o contexto da janela criada
glfw.make_context_current(window)


# Instancia a classe TronBackground
tron_background = TronBackground(5000, 5000, 100)
tron_background.create_background()

# Instancia o Skybox
skybox = Skybox(size=10000)

#Cubo
cubo = Cubo(tamanho=50.0, cor=(0.5, 0.5, 1))
cubo.transladar(200.0, 200.0, 20.0)

#Cubo2
#cubo2 = Cubo(tamanho=50.0, cor=(0.5, 0.5, 1))
#cubo2.transladar(500.0, 500.0, 20.0)

#Moto
moto1 = Moto(500, 500, x_size=100, y_size=100, id=1)
moto2 = Moto(10,10,id=2)

#Trajetoria
trajetoria1 = Trajetoria(max_points=30, interval=0.1)
trajetoria2 = Trajetoria(max_points=30, interval=0.1)

# Obstacles
obstacles = []

# Adicione os cubos
#obstacles.append(Obstacle(cubo.posicao[0]-cubo.tamanho, cubo.posicao[1]-cubo.tamanho, cubo.tamanho*2, cubo.tamanho*2))
#obstacles.append(Obstacle(cubo2.posicao[0]-cubo2.tamanho, cubo2.posicao[1]-cubo2.tamanho, cubo2.tamanho*2, cubo2.tamanho*2))
# Adiciona as motos como obstáculos
obstacles.append(Obstacle(moto1.moto_position[0] - moto1.x_size/2, moto1.moto_position[1] - moto1.y_size/2, moto1.x_size, moto1.y_size, id=moto1.id))
obstacles.append(Obstacle(moto2.moto_position[0] - moto2.x_size/2, moto2.moto_position[1] - moto2.y_size/2, moto2.x_size, moto2.y_size, id=moto2.id))


# Principal Loping
while not glfw.window_should_close(window):
    glfw.poll_events()
    # Limpa o buffer de cores e de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if not menu.game_started:
        glClearColor(1.0, 1.0, 1.0, 1)  #branco
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Configuração para blending

        menu.handle_events()  # Manipular eventos do menu
        menu.draw()  # Desenhar o menu

        glfw.swap_buffers(window)

    else:
        glClearColor(0.0, 0.0, 0.0, 1.0)  # preto
        glEnable(GL_DEPTH_TEST)


        # Renderizar o placar de HP no canto superior esquerdo
         # Pode ser atualizado conforme o jogo progride
        render_text(f"HP: {HP2}", 10, 550)

        #   CAMERA 1 ////////////////////////////////////////////////////////////////////////////////////////////////
        # Desenhar Camera 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 0.1, 20000)
        gluLookAt(*moto1.calculate_camera_params())

        # Desenha a SkyBox
        skybox.draw()

        # Desenhar fundo
        tron_background.draw()

        trajetoria1.draw(color=[1, 1, 0])
        trajetoria2.draw(color=[0, 0, 1])


        # Desenha o cubo
        #cubo.desenhar()
        #cubo2.desenhar()

        #Hit box
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

        # Adicionar o ponto da parte de trás do quadrado na trajetória
        back_x, back_y = moto1.get_back_position()
        trajetoria1.add_point(back_x, back_y)

        # Desenha moto 2
        moto2.desenha()



        glfw.poll_events()

        tempo_ultima_atualizacao = time.time()

        # Verificar colisão do quadrado com a trajetória
        if trajetoria1.check_collision(moto1.moto_position[0], moto1.moto_position[1], moto1.x_size):
            print("Colisão detectada 1!")

            tempo_atual = time.time()
            if tempo_atual - tempo_ultima_atualizacao >= intervalo_atualizacao:
                HP1 -= 1
                render_text(f"HP: {HP1}", 10, 550)
                moto1 = Moto(100, 100)
                trajetoria1 = Trajetoria(max_points=30, interval=0.1)

            if HP1 < 0:
                HP1 = 0

        if trajetoria2.check_collision(moto1.moto_position[0], moto1.moto_position[1], moto1.x_size):
            print("Colisão detectada 1!")
            tempo_atual = time.time()
            if tempo_atual - tempo_ultima_atualizacao >= intervalo_atualizacao:
                HP1 -= 1
                render_text(f"HP: {HP1}", 10, 550)
                moto1 = Moto(100, 100)
                trajetoria1 = Trajetoria(max_points=30, interval=0.1)
            if HP1 < 0:
                HP1 = 0
            print(HP1)
            print(tempo_atual)
            print(tempo_ultima_atualizacao)

        # Desabilita o blending e desativa a textura
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        # Renderizar o placar de HP no canto superior esquerdo
         # Pode ser atualizado conforme o jogo progride
        render_text(f"HP: {HP1}", 10, 550)


        #CAMERA 2 //////////////////////////////////////////////////////////////////////////////////////////////////////////
        # Desenhar CAMERA 2
        glViewport(width, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 0.1, 20000)
        gluLookAt(*moto2.calculate_camera_params())

        # Desenha a SkyBox
        skybox.draw()

        # Desenhar fundo
        tron_background.draw()

        trajetoria1.draw(color=[1, 1, 0])
        trajetoria2.draw(color=[0, 0, 1])

        # Desenha o cubo
        #cubo.desenhar()
        #cubo2.desenhar()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

        # Movimento e Desenho MOTO 2
        moto2.movimento(window, True, obstacles)
        moto2.desenha()

        # Adicionar o ponto da parte de trás do quadrado na trajetória
        back_x, back_y = moto2.get_back_position()
        trajetoria2.add_point(back_x, back_y)

        # Desenha MOTO 1
        moto1.desenha()

        tempo_ultima_atualizacao = time.time()

        # Verificar colisão do quadrado com a trajetória
        if trajetoria2.check_collision(moto2.moto_position[0], moto2.moto_position[1], moto2.x_size):
            print("Colisão detectada 2!")

            tempo_atual = time.time()
            if tempo_atual - tempo_ultima_atualizacao >= intervalo_atualizacao:
                HP2 -= 1
                render_text(f": {HP2}", 10, 550)
                moto2 = Moto(500, 500)
                trajetoria2 = Trajetoria(max_points=30, interval=0.1)
            if HP2 < 0:
                HP2 = 0
            print(HP2)

        if trajetoria1.check_collision(moto2.moto_position[0], moto2.moto_position[1], moto2.x_size):
            print("Colisão detectada 2!")
            tempo_atual = time.time()
            if tempo_atual - tempo_ultima_atualizacao >= intervalo_atualizacao:
                HP2 -= 1
                render_text(f"HP: {HP2}", 10, 550)
                moto2 = Moto(500, 500)
                trajetoria2 = Trajetoria(max_points=30, interval=0.1)
            if HP2 < 0:
                HP2 = 0
            print(HP2)





        menu.paused()
        # Desabilita o blending e desativa a textura
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        # Troca os buffers e atualiza a janela
        glfw.swap_buffers(window)

# Finaliza o GLFW
glfw.terminate()
