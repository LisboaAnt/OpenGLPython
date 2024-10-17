import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import time  # Importa o módulo de tempo

from cubo import Cubo
from esfera import Esfera
from TextureAtlasLoader import TextureAtlasLoader
from camera import Camera
from iluminacao import Iluminacao

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 1200, 800
window = glfw.create_window(width, height, "Aula 3", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)
glfw.swap_interval(1)

# Ativa o teste de profundidade
glEnable(GL_DEPTH_TEST)


# Desativa a face front da camera
glEnable(GL_CULL_FACE)  # Habilita o culling
glCullFace(GL_FRONT)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

camera = Camera(width, height)
luz = Iluminacao()

texture_file = 'AtlasMinecrfat.jpg'
atlas_size = (32, 16)  # Suponha que o atlas é 2x4 (16 imagens)
atlas_loader = TextureAtlasLoader(texture_file, atlas_size)

lista_de_cubos = [
    Cubo(initial_position=[1.0 * i * 2, 0.0, 1.0 * j * 2], raio=1, texture_atlas=atlas_loader,
         texture_indices=[3, 3, 3, 3, 2, 50])
    for i in range(10)
    for j in range(10)
]

flor = 66
craft_table = [141,142,141,142,140,140]
fornalha1 = [145,145,143,145,146,146]
fornalha2 = [145,145,144,145,146,146]
novos_cubos = [
    Cubo(initial_position=[5, 2.0, 5], raio=1, texture_atlas=atlas_loader, texture_indices=[flor, flor, flor, flor, flor, flor]),
    Cubo(initial_position=[11, 2.0, 7], raio=1, texture_atlas=atlas_loader, texture_indices=fornalha1),
    Cubo(initial_position=[9, 2.0, 7], raio=1, texture_atlas=atlas_loader, texture_indices=fornalha2),
    Cubo(initial_position=[7, 2.0, 7], raio=1, texture_atlas=atlas_loader, texture_indices=craft_table)
]

lista_de_cubos.extend(novos_cubos)


# Gerar a lista de exibição
def gerar_lista_de_exibicao(cubos):
    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)

    for cubo in cubos:
        cubo.draw()  # Adiciona a chamada de desenho para cada cubo

    glEndList()
    return display_list


esfera = Esfera()

glfw.set_key_callback(window, camera.key_callback)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)

#ATIVA A TRANSPARENCIA
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#ATIVA A TRANSPARENCIA
display_list = gerar_lista_de_exibicao(lista_de_cubos)


# Variáveis para cálculo de FPS
frame_count = 0
start_time = time.time()

while not glfw.window_should_close(window):
    glfw.poll_events()
    camera.process_input(window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.update_camera()

    glCallList(display_list)


    #esfera.draw(3, 4, 0)

    #luz.configurar_luz_potual(GL_LIGHT2, [2, 1, 0], [0.6, 0.2, 0.2], 0.1)
    #luz.configurar_luz_potual(GL_LIGHT3, [0, 1, 2], [0.2, 0.2, 1], 0.1)
    #luz.configurar_luz_potual(GL_LIGHT4, [7, 4, 7], [0.6, 0.2, 0.2], 0.1)
    luz.configurar_luz_direcional(GL_LIGHT5, [1, 1, 1], [0.5, 0.5, 0.5], 1)
    luz.configurar_luz_spot(GL_LIGHT6, [0, 5, 15], [1, -0.2, -1], [0.5, 0.5, 0.5], 100, 50, 20)

    # Atualiza contagem de FPS
    frame_count += 1
    elapsed_time = time.time() - start_time

    if elapsed_time >= 1.0:  # Se 1 segundo se passou
        print(f"FPS: {frame_count}")  # Exibe o FPS no terminal
        frame_count = 0  # Reseta a contagem de frames
        start_time = time.time()  # Reseta o tempo

    glfw.swap_buffers(window)

glfw.terminate()
