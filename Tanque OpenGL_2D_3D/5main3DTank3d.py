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

# Posição e ângulo inicial do tanque
tank_angle = 0.0
tank_position = [width / 2, height / 2]
tank_speed = 0.10  # Velocidade do tanque

# Posição e ângulo inicial da câmera
camera_distance = -200.0  # Distância da câmera ao tanque
camera_angle = 45.0  # Ângulo de inclinação da câmera
camera_height = 80.0  # Altura da câmera acima do tanque

def draw_sand_background():
    glDisable(GL_BLEND)  # Desabilita o blending (transparência)
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
tank_texture = load_texture("tank.png")

# Função para desenhar um cubo 3D
def draw_tank(x, y, z, width, height, length):
    half_width = width / 2
    half_height = height / 2
    half_length = length / 2

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0); # Cor verde


    # Face frontal
    glVertex3f(x - half_width, y - half_height, z + half_length)
    glVertex3f(x + half_width, y - half_height, z + half_length)
    glVertex3f(x + half_width, y + half_height, z + half_length)
    glVertex3f(x - half_width, y + half_height, z + half_length)

    # Face traseira
    glVertex3f(x - half_width, y - half_height, z - half_length)
    glVertex3f(x + half_width, y - half_height, z - half_length)
    glVertex3f(x + half_width, y + half_height, z - half_length)
    glVertex3f(x - half_width, y + half_height, z - half_length)

    # Face lateral esquerda
    glVertex3f(x - half_width, y - half_height, z + half_length)
    glVertex3f(x - half_width, y - half_height, z - half_length)
    glVertex3f(x - half_width, y + half_height, z - half_length)
    glVertex3f(x - half_width, y + half_height, z + half_length)

    # Face lateral direita
    glVertex3f(x + half_width, y - half_height, z + half_length)
    glVertex3f(x + half_width, y - half_height, z - half_length)
    glVertex3f(x + half_width, y + half_height, z - half_length)
    glVertex3f(x + half_width, y + half_height, z + half_length)

    # Face superior
    glVertex3f(x - half_width, y + half_height, z + half_length)
    glVertex3f(x + half_width, y + half_height, z + half_length)
    glVertex3f(x + half_width, y + half_height, z - half_length)
    glVertex3f(x - half_width, y + half_height, z - half_length)

    # Face inferior
    glVertex3f(x - half_width, y - half_height, z + half_length)
    glVertex3f(x + half_width, y - half_height, z + half_length)
    glVertex3f(x + half_width, y - half_height, z - half_length)
    glVertex3f(x - half_width, y - half_height, z - half_length)

    glEnd()




# Loop principal do jogo
while not glfw.window_should_close(window):
    glfw.poll_events()

    #LUZ

    
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
    draw_sand_background()

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

    # Desenha o tanque como um cubo 3D
    glPushMatrix()
    glTranslatef(tank_position[0], tank_position[1], 0)
    glRotatef(tank_angle, 0, 0, 1)
    draw_tank(0, 0, 0, 50,50,50)  # Desenha o cubo 3D do tanque
    glPopMatrix()

    # Troca os buffers e atualiza a janela
    glfw.swap_buffers(window)

# Finaliza o GLFW
glfw.terminate()
