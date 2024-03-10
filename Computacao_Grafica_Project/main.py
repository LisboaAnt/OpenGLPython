import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import numpy as np
from background import draw_sand_background
from cube import Cube
from tank import Tank

# Inicialização do GLFW
if not glfw.init():
    raise Exception("Failed to initialize GLFW")

width, height = 800, 600
window = glfw.create_window(width, height, "Trabalho de Álgebra", None, None)

if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

glfw.make_context_current(window)

# Habilita o teste de profundidade
glEnable(GL_DEPTH_TEST)

# Posição e ângulo inicial do tanque
tank_angle = 0.0
tank_position = [width / 2, height / 2]
tank_speed = 0.10  # Velocidade do tanque

# Posição e ângulo inicial da câmera
camera_distance = -200.0  # Distância da câmera ao tanque
camera_angle = 45.0  # Ângulo de inclinação da câmera
camera_height = 80.0  # Altura da câmera acima do tanque

# Loop principal do jogo
while not glfw.window_should_close(window):
    glfw.poll_events()

    # Limpa o buffer de cores e de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Atualiza o ângulo da câmera para seguir o ângulo do tanque
    camera_angle = tank_angle

    # Posiciona e orienta a câmera em relação ao tanque
    camera_x = tank_position[0] + camera_distance * math.cos(math.radians(camera_angle))
    camera_y = tank_position[1] + camera_distance * math.sin(math.radians(camera_angle))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000)
    gluLookAt(camera_x, camera_y, camera_height, tank_position[0], tank_position[1], 0, 0, 0, 1)

    # Desenha o fundo de areia
    draw_sand_background(width, height)

    # Atualiza a posição do tanque com base nas teclas pressionadas
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        tank_angle += 0.05  # Gira o tanque para a esquerda
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        tank_angle -= 0.05  # Gira o tanque para a direita
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        tank_position[0] += tank_speed * math.cos(math.radians(tank_angle))
        tank_position[1] += tank_speed * math.sin(math.radians(tank_angle))
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        tank_position[0] -= tank_speed * math.cos(math.radians(tank_angle))
        tank_position[1] -= tank_speed * math.sin(math.radians(tank_angle))

    # Desenha os cubos
    cube1 = Cube(50, 50, 10, 50, 0, 1, 1, 100)
    cube2 = Cube(700, 500, 10, 50, 0, 1, 1, 100)
    cube1.draw()
    cube2.draw()

    # Desenha o tanque como um cubo 3D
    tank = Tank(tank_position[0], tank_position[1], 0, 50, 50, 50, tank_angle)
    tank.draw()

    # Troca os buffers e atualiza a janela
    glfw.swap_buffers(window)

# Finaliza o GLFW
glfw.terminate()
