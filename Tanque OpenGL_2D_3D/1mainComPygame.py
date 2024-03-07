import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Inicialização do Pygame
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Trabalho de Álgebra")
icone = pygame.image.load("icone.png")
pygame.display.set_icon(icone)
# Configurações de OpenGL
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, width, 0, height)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

def draw_sand_background():
    glBegin(GL_QUADS)
    glColor3f(0.96, 0.87, 0.70)  # Cor de areia
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, height)
    glVertex2f(0, height)
    glEnd()
    
# Função para carregar a textura do tanque com transparência preservada
def load_texture():
    texture_surface = pygame.image.load("tank.png").convert_alpha()  # Convertendo para suportar transparência
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture

# Variáveis de controle do tanque
tank_texture = load_texture()
tank_angle = 0.0
tank_position = [width / 2, height / 2]
tank_speed = 0.06

# Dicionário para armazenar o estado das teclas
keys = {}

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            keys[event.key] = True  # Define a tecla pressionada como True
        elif event.type == KEYUP:
            keys[event.key] = False  # Define a tecla liberada como False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Desenhar o fundo de areia
    draw_sand_background()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # Habilita o blending para suportar transparência
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Define a função de blending

    # Verifica o estado das teclas e atualiza a posição do tanque
    if keys.get(K_a):
        tank_angle += 0.03  # Girar para a esquerda
    if keys.get(K_d):
        tank_angle -= 0.03  # Girar para a direita
    if keys.get(K_w):
        # Movimentar para frente na direção do ângulo
        tank_position[0] += tank_speed * math.cos(math.radians(tank_angle))
        tank_position[1] += tank_speed * math.sin(math.radians(tank_angle))
    if keys.get(K_s):
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

    pygame.display.flip()
