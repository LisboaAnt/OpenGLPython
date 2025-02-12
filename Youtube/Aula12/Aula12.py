import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import time

from cubo import Cubo
from esfera import Esfera

from camera import Camera
from iluminacao import Iluminacao
from textureAtlas import TextureAtlas

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600
window = glfw.create_window(width, height, "Aula 3", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "./images/icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)
glfw.swap_interval(1)


# Função de callback para redimensionamento da janela
def framebuffer_size_callback(window, new_width, new_height):
    """
    Callback chamado quando o framebuffer (área de desenho) é redimensionado.
    """
    global width, height
    width, height = new_width, new_height
    glViewport(0, 0, width, height)  # Atualiza o viewport
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 50000.0)  # Atualiza a matriz de projeção
    glMatrixMode(GL_MODELVIEW)


# Registra o callback de redimensionamento
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50000.0)
glMatrixMode(GL_MODELVIEW)

camera = Camera(width, height)
luz = Iluminacao()
textura = TextureAtlas('./images/minecraft.jpg', (32, 16))
esfera = Esfera()
textura_Skybox = TextureAtlas('./images/skybox_atlas.png', (3, 2))

lista_cubos = [
    Cubo(inital_position=[2 * i, 0.0, 2 * j], texture_atlas=textura, texture_indices=[3, 3, 3, 3, 2, 50])
    for i in range(10)
    for j in range(10)
]

teia = [66, 66, 66, 66, 66, 66]
craftable = [141, 142, 141, 142, 140, 140]
fornalha = [145, 145, 143, 145, 146, 146]
fornalha2 = [145, 145, 144, 145, 146, 146]

novos_cubos = [
    Cubo(inital_position=[0, 0, 0], raio=20000, texture_atlas=textura_Skybox, texture_indices=[2, 0, 1, 3, 4, 5],
         lighting=True),
    Cubo(inital_position=[7, 2.0, 7], texture_atlas=textura, texture_indices=craftable),
    Cubo(inital_position=[9, 2.0, 7], texture_atlas=textura, texture_indices=fornalha),
    Cubo(inital_position=[11, 2.0, 7], texture_atlas=textura, texture_indices=fornalha2),
]

lista_cubos.extend(novos_cubos)


def listaExibicao(cubos):
    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)

    for cubo in lista_cubos:
        cubo.draw(0, 0, 0)

    glEndList()
    return display_list


glClearColor(0, 0, 0, 1)
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

    glCallList(lista_de_exebicao)

    esfera.draw(3, 0, 0)

    #luz.configurar_luz_potual(GL_LIGHT2, [2, 1, 0], [0.6, 0.2, 0.2], 0.1)

    #luz.configurar_luz_potual(GL_LIGHT3, [0, 1, 2], [0.2, 0.2, 1], 0.1)

    luz.configurar_luz_potual(GL_LIGHT4, [2, 3, 0], [1, 0.2, 0.2], 0.1)

    luz.configurar_luz_direcional(GL_LIGHT5, [1, 1, 1], [0.5, 0.5, 0.5], 2)

    luz.configurar_luz_spot(GL_LIGHT6, [0, 5, 15], [1, -0.2, -1], [0.5, 0.5, 0.5], 100, 50, 20)

    frame_count += 1
    elapsed_time = time.time() - start_time
    teiaCubo = Cubo(inital_position=[5, 2.0, 7], raio=0.995, texture_atlas=textura, texture_indices=teia)
    teiaCubo.draw(0, 0, 0, camera.camera_pos)

    if elapsed_time >= 1:
        print(f"FPS: {frame_count}")
        frame_count = 0
        start_time = time.time()

    glfw.swap_buffers(window)

glfw.terminate()
