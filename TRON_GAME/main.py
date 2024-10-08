import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from PIL import Image
import time

# IMPORT ELEMENTOS
from Cubo import Cubo
from Moto import Moto

# HIT BOXS
from Obstacles import Obstacle  #HIT BOX QUADRADO -> QUADRADO 2D
from Trajetoria import Trajetoria  #HIT BOX QUADRADO -> LINHAS 2D

# MAPA
from Background import TronBackground  #CHÃO
from Skybox import Skybox  #SKYBOX
from Iluminacao import Iluminacao

# Menu e Placar de Vidas
from Menu import MainMenu  # MENU DO JOGO
from PlacarDeVida import PlacarDeVida

# Inicializando a biblioteca GLFW
if not glfw.init():
    raise Exception("Falha ao inicializar o GLFW")
width, height = 1600, 650
window = glfw.create_window(width, height, "TRON - OpenGL", None, None)  # Janela dividida
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a janela GLFW")

# Definir o ícone da janela
icon_path = "./imgs/icon.png"
glfw.set_window_icon(window, 1, Image.open(icon_path))


# CONTROLHE DO BUFFER
def framebuffer_size_callback(window, fb_width, fb_height):
    global width, height
    width, height = fb_width // 2, fb_height
    glViewport(0, 0, fb_width, fb_height)
    if glfw.get_window_attrib(window, glfw.MAXIMIZED):
        primary_monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(primary_monitor)
        glfw.set_window_size(window, mode.size.width, mode.size.height)


glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# Configurar o contexto da janela criada
glfw.make_context_current(window)

# Criar o menu inicial
menu = MainMenu(window)

# Instancia Placar de Vida
placarDeVida = PlacarDeVida()
HP1 = [3]
HP2 = [3]

# Instancia Iluminacao
iluminacao = Iluminacao()
iluminacao.create_light(position=[0.0, 0.0, 15.0, 1.0], intensity=30.0, distance=60, color=[1, 1, 0],
                        light_id=GL_LIGHT1)
iluminacao.create_light(position=[0.0, 0.0, 15.0, 1.0], intensity=30.0, distance=60, color=[0, 1, 1],
                        light_id=GL_LIGHT2)

# Instancia a classe TronBackground
tron_background = TronBackground(5000, 5000, 100)
tron_background.create_background()

# Instancia o Skybox
skybox = Skybox(size=5000)

# Trajetória
trajetoria1 = Trajetoria(max_points=100, interval=0.1)
trajetoria2 = Trajetoria(max_points=100, interval=0.1)

# Moto
moto1 = Moto(2000, 0, x_size=70, y_size=70, moto_angle=180, HP=HP1, trajetoria=trajetoria1, id=1)
moto2 = Moto(-2000, 0, x_size=70, y_size=70, HP=HP2, trajetoria=trajetoria2, id=2)

# Cubo
cubo1 = Cubo(tamanho=50.0, textura_path="./imgs/Red_X.jpg")
cubo1.transladar(1000, -1000, 20.0)
cubo2 = Cubo(tamanho=50.0, textura_path="./imgs/Red_X.jpg")
cubo2.transladar(1000, 1000, 20.0)
cubo3 = Cubo(tamanho=50.0, textura_path="./imgs/Red_X.jpg")
cubo3.transladar(-1000, 1000, 20.0)
cubo4 = Cubo(tamanho=50.0, textura_path="./imgs/Red_X.jpg")
cubo4.transladar(-1000, -1000, 20.0)

# Obstacles
obstacles = []

# Adicione os cubos
obstacles.append(
    Obstacle(cubo1.posicao[0] - cubo1.tamanho / 2, cubo1.posicao[1] - cubo1.tamanho / 2, cubo1.tamanho, cubo1.tamanho))
obstacles.append(
    Obstacle(cubo2.posicao[0] - cubo2.tamanho / 2, cubo2.posicao[1] - cubo2.tamanho / 2, cubo2.tamanho, cubo2.tamanho))
obstacles.append(
    Obstacle(cubo3.posicao[0] - cubo3.tamanho / 2, cubo3.posicao[1] - cubo3.tamanho / 2, cubo3.tamanho, cubo3.tamanho))
obstacles.append(
    Obstacle(cubo4.posicao[0] - cubo4.tamanho / 2, cubo4.posicao[1] - cubo4.tamanho / 2, cubo4.tamanho, cubo4.tamanho))

# Adiciona as motos como obstaculos
obstacles.append(
    Obstacle(moto1.moto_position[0] - moto1.x_size / 2, moto1.moto_position[1] - moto1.y_size / 2, moto1.x_size,
             moto1.y_size, id=moto1.id))
obstacles.append(
    Obstacle(moto2.moto_position[0] - moto2.x_size / 2, moto2.moto_position[1] - moto2.y_size / 2, moto2.x_size,
             moto2.y_size, id=moto2.id))
obstacles.extend([  #PAREDES LATERAIS
    Obstacle(2500, -2500, 100, 5000, id=3),
    Obstacle(-2600, -2500, 100, 5000, id=3),
    Obstacle(-2500, -2600, 5000, 100, id=3),
    Obstacle(-2500, 2500, 5000, 100, id=3),
])

# Variaveis para calcular FPS
previous_time = glfw.get_time()
frame_count = 0

# Defina uma constante para o limite de FPS
FPS_LIMIT = 60
FRAME_TIME = 1.0 / FPS_LIMIT  # Tempo por quadro em segundos

#Liga a Luz, no meio do código eu ligo ela várias vezes kkk
glEnable(GL_LIGHTING)
glEnable(GL_DEPTH_TEST)


def verificar_colisao_e_redefinir(trajetoria, moto, HP):
    global trajetoria1, trajetoria2
    if trajetoria.check_collision(moto.moto_position[0], moto.moto_position[1], moto.x_size):
        # Diminui o HP
        HP[0] -= 1
        if moto.id == 1:
            trajetoria1.reset_points()
            moto.moto_position = [2000, 0]
            moto.moto_angle = 180
        else:
            trajetoria2.reset_points()
            moto.moto_position = [-2000, 0]
            moto.moto_angle = 0


ganhou = 0

# Principal loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    start_time = glfw.get_time()

    # Limpa o buffer de cores e de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    iluminacao.move_light(GL_LIGHT2, moto1.get_back_position() + tuple([80, 1]))
    iluminacao.move_light(GL_LIGHT1, moto2.get_back_position() + tuple([80, 1]))

    if not menu.game_started:
        ganhou = 0
        moto1.moto_position = [2000, 0]
        moto1.moto_angle = 180
        moto2.moto_angle = 0
        moto2.moto_position = [-2000, 0]
        trajetoria1.reset_points()
        trajetoria2.reset_points()
        HP1[0], HP2[0] = 3, 3
        glClearColor(1.0, 1.0, 1.0, 1)  # branco
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Configuração para blending

        menu.handle_events()  # Manipular eventos do menu
        menu.draw()  # Desenhar o menu

        glfw.swap_buffers(window)
        glfw.poll_events()

    else:
        if HP1[0] <= 0:
            ganhou = 2
        if HP2[0] <= 0:
            ganhou = 1
        glClearColor(0.0, 0.0, 0.0, 1.0)  # preto
        glEnable(GL_DEPTH_TEST)
        iluminacao.configure_environment()

        #   CAMERA 1 ////////////////////////////////////////////////////////////////////////////////////////////////
        # Desenhar Camera 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, width / height, 0.1, 15000)
        gluLookAt(*moto1.calculate_camera_params())

        placarwidth = width / 2.3
        if width > 900:
            placarwidth = (width / 2.7)
        # Placar 1
        placarDeVida.render_text(f"HP: {HP1[0]}", placarwidth, 550, color=[0, 255, 255])
        if ganhou == 2: placarDeVida.mostrar_vencedor(vencedor=f"DERROTA", color=[255, 0, 0])
        if ganhou == 1: placarDeVida.mostrar_vencedor(vencedor=f"VITORIA", color=[0, 255, 0])

        iluminacao.show_lights()

        # Desenha a SkyBox
        skybox.draw()

        # Desenhar fundo
        tron_background.draw()

        trajetoria2.draw(color=[1, 1, 0])
        trajetoria1.draw(color=[0, 1, 1])

        # Desenha o cubo
        cubo1.desenhar()
        cubo2.desenhar()
        cubo3.desenhar()
        cubo4.desenhar()

        # Textura
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

        # Desenha e move 1
        moto1.movimento(window, False, obstacles)
        moto1.desenha()

        # Adicionar o ponto da parte de trás do quadrado na trajetória
        back_x, back_y = moto1.get_back_position()
        trajetoria1.add_point(back_x, back_y)

        # Desenha moto 2
        moto2.desenha()

        verificar_colisao_e_redefinir(trajetoria1, moto1, HP1)
        verificar_colisao_e_redefinir(trajetoria2, moto1, HP1)

        # CAMERA 2 //////////////////////////////////////////////////////////////////////////////////////////////////////////
        # Desenhar CAMERA 2
        glViewport(width, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, width / height, 0.1, 15000)
        gluLookAt(*moto2.calculate_camera_params())

        # Iluminacao
        iluminacao.show_lights()

        # Placar
        placarwidth = width / 2.3
        if width > 900:
            placarwidth = (width / 2.7)
        placarDeVida.render_text(f"HP: {HP2[0]}", placarwidth, 550, color=[255, 255, 0])
        if ganhou == 1: placarDeVida.mostrar_vencedor(vencedor=f"DERROTA", color=[255, 0, 0])
        if ganhou == 2: placarDeVida.mostrar_vencedor(vencedor=f"VITORIA", color=[0, 255, 0])

        # Desenha a SkyBox
        skybox.draw()

        # Desenhar fundo
        tron_background.draw()

        trajetoria2.draw(color=[1, 1, 0])
        trajetoria1.draw(color=[0, 1, 1])

        # Desenha o cubo
        cubo1.desenhar()
        cubo2.desenhar()
        cubo3.desenhar()
        cubo4.desenhar()

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

        # Verificar colisão do quadrado com a trajetória
        verificar_colisao_e_redefinir(trajetoria1, moto2, HP2)
        verificar_colisao_e_redefinir(trajetoria2, moto2, HP2)

        menu.paused()

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Calcular FPS
    current_time = glfw.get_time()
    elapsed_time = current_time - previous_time
    frame_count += 1

    if elapsed_time > 1.0:
        fps = frame_count / elapsed_time

        print(f"FPS: {fps:.2f}")
        frame_count = 0
        previous_time = current_time

    # Calcule o tempo de execução e faça uma pausa para manter o FPS
    end_time = glfw.get_time()  # Tempo de fim da iteração
    frame_duration = end_time - start_time  # Duração da iteração
    if frame_duration < FRAME_TIME:
        time.sleep(FRAME_TIME - frame_duration)  # Pausa para manter o FPS

    if ganhou:
        time.sleep(3)
        menu.game_started = False

glfw.terminate()
