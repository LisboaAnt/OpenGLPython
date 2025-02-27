import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import time

from cubo import Cubo

from camera import Camera
from iluminacao import Iluminacao
from textureAtlas import TextureAtlas
from Mesh import Mesh
from cilindro import Cilindro

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600
window = glfw.create_window(width, height, "Desafio Monitoria", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "./images/icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)
glfw.swap_interval(1)


def framebuffer_zise_callback(window, new_width, new_height):
    global width, height
    width, height = new_width, new_height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 5000)
    glMatrixMode(GL_MODELVIEW)


glfw.set_framebuffer_size_callback(window, framebuffer_zise_callback)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glMatrixMode(GL_PROJECTION)

glLoadIdentity()
gluPerspective(45, width / height, 0.1, 5000)
glMatrixMode(GL_MODELVIEW)

camera = Camera(width, height)
luz = Iluminacao()

textura = TextureAtlas('./images/Basquete.png', (1, 1))
textura_placar = TextureAtlas('./images/Texturas_atlas.png', (6, 2))

mesh = Mesh(start_pos=[-7.5, -14], end_pos=[7.5, 14], normal=[0.0, 0.0, -1.0], total_polygons=10000,
            texture_atlas=textura, texture_index=3)

lista_cubos = [

    Cubo(inital_position=[0, -2, 0], altura=0.99, largura=16.0, profundidade=29.0, cores_faces=[
        [0.31, 0.10, 0.05, 1.00],  # Frente - Vermelho
        [0.31, 0.10, 0.05, 1.00],  # Direita - Verde
        [0.31, 0.10, 0.05, 1.00],  # Trás - Azul
        [0.31, 0.10, 0.05, 1.00],  # Esquerda - Amarelo
        [0.64, 0.70, 0.73, 1.00],  # Superior - Magenta
        [0.64, 0.70, 0.73, 1.00], ]),

    Cubo(inital_position=[0, -2, -18], altura=1, largura=7.0, profundidade=3, cores_faces=[
        [0.64, 0.70, 0.73, 1.00],  # Frente - Vermelho
        [0.64, 0.70, 0.73, 1.00],  # Direita - Verde
        [0.64, 0.70, 0.73, 1.00],  # Trás - Azul
        [0.64, 0.70, 0.73, 1.00],  # Esquerda - Amarelo
        [0.64, 0.70, 0.73, 1.00],  # Superior - Magenta
        [0.64, 0.70, 0.73, 1.00], ]),

    Cubo(inital_position=[0, -2, 18], altura=1, largura=7.0, profundidade=3, cores_faces=[
        [0.64, 0.70, 0.73, 1.00],  # Frente - Vermelho
        [0.64, 0.70, 0.73, 1.00],  # Direita - Verde
        [0.64, 0.70, 0.73, 1.00],  # Trás - Azul
        [0.64, 0.70, 0.73, 1.00],  # Esquerda - Amarelo
        [0.64, 0.70, 0.73, 1.00],  # Superior - Magenta
        [0.64, 0.70, 0.73, 1.00], ]),

    Cubo(inital_position=[0, 2, 18], altura=8, largura=0.5, profundidade=0.5, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 2, -18], altura=8, largura=0.5, profundidade=0.5, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 4.8, -17], altura=4, largura=0.3, profundidade=0.3, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ], rotation=[35, 0, 0]),

    Cubo(inital_position=[0, 4.8, 17], altura=4, largura=0.3, profundidade=0.3, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ], rotation=[-35, 0, 0]),

    Cubo(inital_position=[0, 6.28, 16.25], altura=4, largura=0.5, profundidade=0.5, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ], rotation=[-75, 0, 0]),

    Cubo(inital_position=[0, 6.28, -16.25], altura=4, largura=0.5, profundidade=0.5, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ], rotation=[75, 0, 0]),

    Cubo(inital_position=[0, 7.5, -14.3], altura=4, largura=5, profundidade=0.1, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 7.5, 14.3], altura=4, largura=5, profundidade=0.1, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 7.5, -14.23], altura=3.7, largura=4.7, profundidade=0.01, cores_faces=[
        [0.9, 0.9, 0.9, 1.00],  # Frente - Vermelho
        [0.9, 0.9, 0.9, 1.00],  # Direita - Verde
        [0.9, 0.9, 0.9, 1.00],  # Trás - Azul
        [0.9, 0.9, 0.9, 1.00],  # Esquerda - Amarelo
        [0.9, 0.9, 0.9, 1.00],  # Superior - Magenta
        [0.9, 0.9, 0.9, 1.00], ]),

    Cubo(inital_position=[0, 7.5, 14.23], altura=3.7, largura=4.7, profundidade=0.01, cores_faces=[
        [0.9, 0.9, 0.9, 1.00],  # Frente - Vermelho
        [0.9, 0.9, 0.9, 1.00],  # Direita - Verde
        [0.9, 0.9, 0.9, 1.00],  # Trás - Azul
        [0.9, 0.9, 0.9, 1.00],  # Esquerda - Amarelo
        [0.9, 0.9, 0.9, 1.00],  # Superior - Magenta
        [0.9, 0.9, 0.9, 1.00], ]),

    Cubo(inital_position=[0, 7.9, -14.2], altura=0.1, largura=2.6, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 7.9, 14.2], altura=0.1, largura=2.6, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 6, -14.2], altura=0.1, largura=2.6, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[0, 6, 14.2], altura=0.1, largura=2.6, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[1.3, 6.95, 14.2], altura=2.0, largura=0.1, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[1.3, 6.95, -14.2], altura=2.0, largura=0.1, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[-1.3, 6.95, -14.2], altura=2.0, largura=0.1, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[-1.3, 6.95, 14.2], altura=2.0, largura=0.1, profundidade=0.01, cores_faces=[
        [0.08, 0.10, 0.11, 1.00],  # Frente - Vermelho
        [0.08, 0.10, 0.11, 1.00],  # Direita - Verde
        [0.08, 0.10, 0.11, 1.00],  # Trás - Azul
        [0.08, 0.10, 0.11, 1.00],  # Esquerda - Amarelo
        [0.08, 0.10, 0.11, 1.00],  # Superior - Magenta
        [0.08, 0.10, 0.11, 1.00], ]),

    Cubo(inital_position=[13, 10, 0], altura=7.0, largura=1, profundidade=12, cores_faces=[
        [0.26, 0.26, 0.26, 1.00],  # Frente - Vermelho
        [0.26, 0.26, 0.26, 1.00],  # Direita - Verde
        [0.26, 0.26, 0.26, 1.00],  # Trás - Azul
        [0.26, 0.26, 0.26, 1.00],  # Esquerda - Amarelo
        [0.26, 0.26, 0.26, 1.00],  # Superior - Magenta
        [0.26, 0.26, 0.26, 1.00], ]),

    Cubo(inital_position=[12.5, 9, 3.5], altura=3.5, largura=0.01, profundidade=3.5, cores_faces=[
        [0.15, 0.13, 0.13, 1.00],  # Frente - Vermelho
        [0.15, 0.13, 0.13, 1.00],  # Direita - Verde
        [0.15, 0.13, 0.13, 1.00],  # Trás - Azul
        [0.15, 0.13, 0.13, 1.00],  # Esquerda - Amarelo
        [0.15, 0.13, 0.13, 1.00],  # Superior - Magenta
        [0.15, 0.13, 0.13, 1.00], ]),

    Cubo(inital_position=[12.45, 9, 3.5], altura=3.5, largura=0.01, profundidade=3.5, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 3, 5, 5], lighting=False),

    Cubo(inital_position=[12.45, 12, 3.5], altura=3.5, largura=0.01, profundidade=3.5, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 1, 5, 5], lighting=False),

    Cubo(inital_position=[12.5, 9, -3.5], altura=3.5, largura=0.01, profundidade=3.5, cores_faces=[
        [0.15, 0.13, 0.13, 1.00],  # Frente - Vermelho
        [0.15, 0.13, 0.13, 1.00],  # Direita - Verde
        [0.15, 0.13, 0.13, 1.00],  # Trás - Azul
        [0.15, 0.13, 0.13, 1.00],  # Esquerda - Amarelo
        [0.15, 0.13, 0.13, 1.00],  # Superior - Magenta
        [0.15, 0.13, 0.13, 1.00], ]),

    Cubo(inital_position=[12.45, 9, -3.5], altura=3.5, largura=0.01, profundidade=3.5, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 8, 5, 5], lighting=False),

    Cubo(inital_position=[12.45, 12, -3.5], altura=3.5, largura=0.01, profundidade=3.5, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 0, 5, 5], lighting=False),

    Cubo(inital_position=[12.5, 12, 0], altura=1.5, largura=0.01, profundidade=3, cores_faces=[
        [0.15, 0.13, 0.13, 1.00],  # Frente - Vermelho
        [0.15, 0.13, 0.13, 1.00],  # Direita - Verde
        [0.15, 0.13, 0.13, 1.00],  # Trás - Azul
        [0.15, 0.13, 0.13, 1.00],  # Esquerda - Amarelo
        [0.15, 0.13, 0.13, 1.00],  # Superior - Magenta
        [0.15, 0.13, 0.13, 1.00], ]),

    Cubo(inital_position=[12.45, 12, 0], altura=2.5, largura=0.01, profundidade=2.5, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 4, 5, 5], lighting=False),

    Cubo(inital_position=[12.5, 10, 0], altura=1, largura=0.01, profundidade=1, cores_faces=[
        [0.15, 0.13, 0.13, 1.00],  # Frente - Vermelho
        [0.15, 0.13, 0.13, 1.00],  # Direita - Verde
        [0.15, 0.13, 0.13, 1.00],  # Trás - Azul
        [0.15, 0.13, 0.13, 1.00],  # Esquerda - Amarelo
        [0.15, 0.13, 0.13, 1.00],  # Superior - Magenta
        [0.15, 0.13, 0.13, 1.00], ]),

    Cubo(inital_position=[12.45, 10, 0], altura=1, largura=0.01, profundidade=1, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 9, 5, 5], lighting=False),

    Cubo(inital_position=[12.4, 10.8, 0], altura=1.3, largura=0.01, profundidade=1.3, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 2, 5, 5], lighting=False),

    Cubo(inital_position=[12.5, 7.7, -1], altura=1, largura=0.01, profundidade=1, cores_faces=[
        [0.15, 0.13, 0.13, 1.00],  # Frente - Vermelho
        [0.15, 0.13, 0.13, 1.00],  # Direita - Verde
        [0.15, 0.13, 0.13, 1.00],  # Trás - Azul
        [0.15, 0.13, 0.13, 1.00],  # Esquerda - Amarelo
        [0.15, 0.13, 0.13, 1.00],  # Superior - Magenta
        [0.15, 0.13, 0.13, 1.00], ]),

    Cubo(inital_position=[12.45, 7.7, -1], altura=1, largura=0.01, profundidade=1, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 10, 5, 5], lighting=False),

    Cubo(inital_position=[12.45, 8.7, -1], altura=1, largura=0.01, profundidade=1, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 7, 5, 5], lighting=False),

    Cubo(inital_position=[12.5, 7.7, 1], altura=1, largura=0.01, profundidade=1, cores_faces=[
        [0.15, 0.13, 0.13, 1.00],  # Frente - Vermelho
        [0.15, 0.13, 0.13, 1.00],  # Direita - Verde
        [0.15, 0.13, 0.13, 1.00],  # Trás - Azul
        [0.15, 0.13, 0.13, 1.00],  # Esquerda - Amarelo
        [0.15, 0.13, 0.13, 1.00],  # Superior - Magenta
        [0.15, 0.13, 0.13, 1.00], ]),

    Cubo(inital_position=[12.45, 7.7, 1], altura=1, largura=0.01, profundidade=1, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 10, 5, 5], lighting=False),

    Cubo(inital_position=[12.45, 8.7, 1], altura=1, largura=0.01, profundidade=1, texture_atlas=textura_placar,
         texture_indices=[5, 5, 5, 7, 5, 5], lighting=False),

    Cubo(inital_position=[0, 6.6, -14.07], altura=0.2, largura=0.4, profundidade=0.4, cores_faces=[
        [0.9, 0.1, 0.1, 1.00],  # Frente - Vermelho
        [0.9, 0.1, 0.1, 1.00],  # Direita - Verde
        [0.9, 0.1, 0.1, 1.00],  # Trás - Azul
        [0.9, 0.1, 0.1, 1.00],  # Esquerda - Amarelo
        [0.9, 0.1, 0.1, 1.00],  # Superior - Magenta
        [0.9, 0.1, 0.1, 1.00]]),

    Cubo(inital_position=[0, 6.4, -14.12], altura=0.2, largura=0.4, profundidade=0.2, cores_faces=[
        [0.9, 0.1, 0.1, 1.00],  # Frente - Vermelho
        [0.9, 0.1, 0.1, 1.00],  # Direita - Verde
        [0.9, 0.1, 0.1, 1.00],  # Trás - Azul
        [0.9, 0.1, 0.1, 1.00],  # Esquerda - Amarelo
        [0.9, 0.1, 0.1, 1.00],  # Superior - Magenta
        [0.9, 0.1, 0.1, 1.00]]),

    Cubo(inital_position=[0, 6.5, -14.2], altura=0.5, largura=0.5, profundidade=0.01, cores_faces=[
        [0.9, 0.1, 0.1, 1.00],  # Frente - Vermelho
        [0.9, 0.1, 0.1, 1.00],  # Direita - Verde
        [0.9, 0.1, 0.1, 1.00],  # Trás - Azul
        [0.9, 0.1, 0.1, 1.00],  # Esquerda - Amarelo
        [0.9, 0.1, 0.1, 1.00],  # Superior - Magenta
        [0.9, 0.1, 0.1, 1.00]]),


    Cilindro(inital_position=[0, 6.7, -13], altura=0.2, raio=0.8, cores_faces=[
        [1.0, 0.0, 0.0, 0.0],  # Base inferior - vermelho
        [1.0, 0.0, 0.0, 1.0],  # Lateral - verde
        [1.0, 0.0, 0.0, 0.0]  # Base superior - azul
    ], rotation=[90, 0, 0]),


    Cilindro(inital_position=[0, 6.7, -12.6], altura=1, raio=0.79, cores_faces=[
        [1.0, 0.0, 0.0, 0.0],  # Base inferior - vermelho
        [1.0, 1.0, 1.0, 0.5],  # Lateral - verde
        [1.0, 0.0, 0.0, 0.0]  # Base superior - azul
    ], rotation=[90, 0, 0]),
##
    Cubo(inital_position=[0, 6.6, 14.07], altura=0.2, largura=0.4, profundidade=0.4, cores_faces=[
        [0.9, 0.1, 0.1, 1.00],  # Frente - Vermelho
        [0.9, 0.1, 0.1, 1.00],  # Direita - Verde
        [0.9, 0.1, 0.1, 1.00],  # Trás - Azul
        [0.9, 0.1, 0.1, 1.00],  # Esquerda - Amarelo
        [0.9, 0.1, 0.1, 1.00],  # Superior - Magenta
        [0.9, 0.1, 0.1, 1.00]]),

    Cubo(inital_position=[0, 6.4, 14.12], altura=0.2, largura=0.4, profundidade=0.2, cores_faces=[
        [0.9, 0.1, 0.1, 1.00],  # Frente - Vermelho
        [0.9, 0.1, 0.1, 1.00],  # Direita - Verde
        [0.9, 0.1, 0.1, 1.00],  # Trás - Azul
        [0.9, 0.1, 0.1, 1.00],  # Esquerda - Amarelo
        [0.9, 0.1, 0.1, 1.00],  # Superior - Magenta
        [0.9, 0.1, 0.1, 1.00]]),

    Cubo(inital_position=[0, 6.5, 14.2], altura=0.5, largura=0.5, profundidade=0.01, cores_faces=[
        [0.9, 0.1, 0.1, 1.00],  # Frente - Vermelho
        [0.9, 0.1, 0.1, 1.00],  # Direita - Verde
        [0.9, 0.1, 0.1, 1.00],  # Trás - Azul
        [0.9, 0.1, 0.1, 1.00],  # Esquerda - Amarelo
        [0.9, 0.1, 0.1, 1.00],  # Superior - Magenta
        [0.9, 0.1, 0.1, 1.00]]),

    Cilindro(inital_position=[0, 6.7, 13.2], altura=0.2, raio=0.8, cores_faces=[
        [1.0, 0.0, 0.0, 0.0],  # Base inferior - vermelho
        [1.0, 0.0, 0.0, 1.0],  # Lateral - verde
        [1.0, 0.0, 0.0, 0.0]  # Base superior - azul
    ], rotation=[90, 0, 0]),

    Cilindro(inital_position=[0, 6.7, 13.6], altura=1, raio=0.79, cores_faces=[
        [1.0, 0.0, 0.0, 0.0],  # Base inferior - vermelho
        [1.0, 1.0, 1.0, 0.5],  # Lateral - verde
        [1.0, 0.0, 0.0, 0.0]  # Base superior - azul
    ], rotation=[90, 0, 0]),

]


def listaExibicao(lista_cubos):
    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)

    for cubo in lista_cubos:
        cubo.draw(0, 0, 0)

    glEndList()
    return display_list


glClearColor(0.0, 0.184, 0.365, 1.0)
glfw.set_key_callback(window, camera.key_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)

lista_de_exebicao = listaExibicao(lista_cubos)

frame_count = 0
start_time = time.time()

while not glfw.window_should_close(window):
    glfw.poll_events()
    camera.process_input(window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.update_camera()

    mesh.draw()

    glCallList(lista_de_exebicao)


    luz.configurar_luz_direcional(GL_LIGHT5, [1, 1, 1], [0.5, 0.5, 0.5], 0.5)

    luz.configurar_luz_spot(GL_LIGHT6, [0, 5, 15], [0, -3, -1], [0.5, 0.5, 0.5], 100, 50, 20)
    luz.configurar_luz_spot(GL_LIGHT7, [0, 5, -15], [0, -3, 1], [0.5, 0.5, 0.5], 100, 50, 20)

    frame_count += 1
    elapsed_time = time.time() - start_time

    if elapsed_time >= 1:
        print(f"FPS: {frame_count}")
        frame_count = 0
        start_time = time.time()

    glfw.swap_buffers(window)

glfw.terminate()
