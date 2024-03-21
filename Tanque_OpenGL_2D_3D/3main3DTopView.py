import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import numpy as np

# Inicialização do GLFW
if not glfw.init():
    raise Exception("Failed to initialize GLFW")

width, height = 800, 600
window = glfw.create_window(width, height, "Trabalho de Álgebra", None, None)

if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

glfw.make_context_current(window)

# Posição e ângulo inicial da câmera
camera_position = [width / 2, height / 2]
camera_angle = 0.1

def draw_sand_background():
    glBegin(GL_QUADS)
    glColor3f(0.96, 0.87, 0.70)  # Cor de areia
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, height)
    glVertex2f(0, height)
    glEnd()

# Função para carregar a textura do tanque
def load_texture(filename):
    image = Image.open(filename)
    image = image.convert("RGBA")
    width, height = image.size
    texture_data = np.array(list(image.getdata()), np.uint8)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture

# Variáveis de controle do tanque
tank_texture = load_texture("./tank.png")
tank_angle = 0.0
tank_position = [width / 2, height / 2]
tank_speed = 0.06

# Loop principal do jogo
while not glfw.window_should_close(window):
    glfw.poll_events()

    # Movimentar a câmera para seguir o tanque
    camera_position[0] = tank_position[0]
    camera_position[1] = tank_position[1]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Carregar a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(camera_position[0] - width / 2, camera_position[0] + width / 2, camera_position[1] - height / 2, camera_position[1] + height / 2)

    # Carregar a matriz de modelagem e visualização
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-camera_position[0]/10, -camera_position[1]/10, 0)

    # Desenhar o fundo de areia
    draw_sand_background()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

    # Verifica o estado das teclas e atualiza a posição do tanque
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        tank_angle += 0.03  # Girar para a esquerda
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        tank_angle -= 0.03  # Girar para a direita
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        # Movimentar para frente na direção do ângulo
        tank_position[0] += tank_speed * math.cos(math.radians(tank_angle))
        tank_position[1] += tank_speed * math.sin(math.radians(tank_angle))
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        # Movimentar para trás na direção oposta ao ângulo
        tank_position[0] -= tank_speed * math.cos(math.radians(tank_angle))
        tank_position[1] -= tank_speed * math.sin(math.radians(tank_angle))

    glPushMatrix()
    glTranslatef(tank_position[0], tank_position[1], 0)
    glRotatef(tank_angle, 0, 0, 1)
    glBindTexture(GL_TEXTURE_2D, tank_texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-50, -30)
    glTexCoord2f(1, 0)
    glVertex2f(50, -30)
    glTexCoord2f(1, 1)
    glVertex2f(50, 30)
    glTexCoord2f(0, 1)
    glVertex2f(-50, 30)
    glEnd()

    glPopMatrix()
    glDisable(GL_BLEND)  # Desabilita o blending
    glDisable(GL_TEXTURE_2D)

    glfw.swap_buffers(window)

glfw.terminate()
