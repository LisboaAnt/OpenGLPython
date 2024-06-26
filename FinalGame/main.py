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
window = glfw.create_window(width * 2, height, "Trabalho de Álgebra", None, None)  # Janela dividida

if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

glfw.make_context_current(window)





class tron1:
    def __init__(self):
        self.tank_angle = 0.0
        self.tank_position = [width / 2, height / 2]
        self.tank_speed = 0.1  # Velocidade do tanque
        self.camera_distance = -200.0  # Distância da câmera ao tanque
        self.camera_angle = 45.0  # Ângulo de inclinação da câmera
        self.camera_height = 80.0  # Altura da câmera acima do tanque

    def movimento(self):
        # Atualiza a posição do tanque com base nas teclas pressionadas
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.tank_angle += 0.05  # Gira o tanque para a esquerda
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.tank_angle -= 0.05  # Gira o tanque para a direita
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.tank_position[0] +=  self.tank_speed * math.cos(math.radians(self.tank_angle))
            self.tank_position[1] +=  self.tank_speed * math.sin(math.radians(self.tank_angle))
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.tank_position[0] -= self.tank_speed * math.cos(math.radians(self.tank_angle))
            self.tank_position[1] -= self.tank_speed * math.sin(math.radians(self.tank_angle))

    def desenha(self):
        # Desenha o tanque
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


def screen1():
    tank_angle = 0.0
    tank_position = [width / 2, height / 2]
    tank_speed = 0.1  # Velocidade do tanque
    self.camera_distance = -200.0  # Distância da câmera ao tanque
    self.camera_angle = 45.0  # Ângulo de inclinação da câmera
    self.camera_height = 80.0  # Altura da câmera acima do tanque

    camera_angle = tank_angle
    # Posiciona e orienta a câmera em relação ao tanque
    camera_x = tank_position[0] + camera_distance * math.cos(math.radians(camera_angle))
    camera_y = tank_position[1] + camera_distance * math.sin(math.radians(camera_angle))

    # Desenhar visualização dianteira
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000)
    gluLookAt(camera_x, camera_y, camera_height, tank_position[0], tank_position[1], 0, 0, 0, 1)

    # Desenha o fundo de areia
    draw_sand_background()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending


# Posição e ângulo inicial do tanque
tank_angle = 0.0
tank_position = [width / 2, height / 2]
tank_speed = 0.1  # Velocidade do tanque

# Posição e ângulo inicial do tanque 2
tank_angle2 = 0.0
tank_position2 = [width / 2, height / 2]
tank_speed2 = 0.1  # Velocidade do tanque

# Posição e ângulo inicial da câmera
camera_distance = -200.0  # Distância da câmera ao tanque
camera_angle = 45.0  # Ângulo de inclinação da câmera
camera_height = 80.0  # Altura da câmera acima do tanque

# Posição e ângulo inicial da câmera
camera_distance2 = -200.0  # Distância da câmera ao tanque
camera_angle2 = 45.0  # Ângulo de inclinação da câmera
camera_height2 = 80.0  # Altura da câmera acima do tanque


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
tank_texture = load_texture("pixil-frame-0.png")

# Loop principal do jogo


while not glfw.window_should_close(window):
    glfw.poll_events()

    # Limpa o buffer de cores e de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_angle = tank_angle
    # Posiciona e orienta a câmera em relação ao tanque
    camera_x = tank_position[0] + camera_distance * math.cos(math.radians(camera_angle))
    camera_y = tank_position[1] + camera_distance * math.sin(math.radians(camera_angle))

    # Desenhar visualização dianteira
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000)
    gluLookAt(camera_x, camera_y, camera_height, tank_position[0], tank_position[1], 0, 0, 0, 1)

    # Desenha o fundo de areia
    draw_sand_background()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

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

    # Desenha o tanque
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

    # Desenha o tanque
    glPushMatrix()
    glTranslatef(tank_position2[0], tank_position2[1], 0)
    glRotatef(tank_angle2, 0, 0, 1)
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

    # Desabilita o blending e desativa a textura
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

    camera_angle2 = tank_angle2
    # Posiciona e orienta a câmera em relação ao tanque
    camera_x2 = tank_position2[0] + camera_distance * math.cos(math.radians(camera_angle2))
    camera_y2 = tank_position2[1] + camera_distance * math.sin(math.radians(camera_angle2))

    # Desenhar visualização traseira
    glViewport(width, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000)
    gluLookAt(camera_x2, camera_y2, camera_height2, tank_position2[0], tank_position2[1], 0, 0, 0, 1)

    # Desenha o fundo de areia
    draw_sand_background()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending



    # Atualiza a posição do tanque com base nas teclas pressionadas
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        tank_angle2 += 0.05  # Gira o tanque para a esquerda
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        tank_angle2 -= 0.05  # Gira o tanque para a direita
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        tank_position2[0] += tank_speed * math.cos(math.radians(tank_angle2))
        tank_position2[1] += tank_speed * math.sin(math.radians(tank_angle2))
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        tank_position2[0] -= tank_speed * math.cos(math.radians(tank_angle2))
        tank_position2[1] -= tank_speed * math.sin(math.radians(tank_angle2))


    # Desenha o tanque
    glPushMatrix()
    glTranslatef(tank_position2[0], tank_position2[1], 0)
    glRotatef(tank_angle2, 0, 0, 1)
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

    # Desenha o tanque
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
    # Desabilita o blending e desativa a textura
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)



    # Troca os buffers e atualiza a janela
    glfw.swap_buffers(window)

# Finaliza o GLFW
glfw.terminate()
