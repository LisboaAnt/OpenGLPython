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
from loadObjs import LoadObjs

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

def framebuffer_zise_callback(window, new_width, new_height):
    global width, height
    width, height = new_width, new_height
    glViewport(0,0,width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 5000)
    glMatrixMode(GL_MODELVIEW)

glfw.set_framebuffer_size_callback(window,framebuffer_zise_callback)

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
textura = TextureAtlas('./images/minecraft.jpg', (32,16))
minecraft = LoadObjs(obj_path="./objects/steve.obj",scale=(6, 6, 6), position=(10, 3.5, 10),)
stive = LoadObjs(obj_path="./objects/bikini.obj",scale=(100, 100, 100), position=(0, -20, 10),)
esfera = Esfera()


lista_cubos = [
    Cubo(inital_position=[2*i, 0.0, 2*j],raio = 1, texture_atlas =textura, texture_indices=[3,3,3,3,2,50])
    for i in range(10)
    for j in range(10)
]


teia = [66, 66 , 66, 66, 66, 66]
craftable = [141,142,141,142,140,140]
fornalha = [145,145,143,145,146,146]
fornalha2 = [145,145,144,145,146,146]

texture_Skybox = TextureAtlas('./images/skybox_atlas.png', (3,2))

novos_cubos = [
    Cubo(inital_position=[0, 0, 0], raio=2000, texture_atlas=texture_Skybox, texture_indices=[2,0,1,3,4,5], lighting = False),
    Cubo(inital_position=[7, 2.0, 7], raio=1, texture_atlas=textura, texture_indices=craftable),
    Cubo(inital_position=[9, 2.0, 7], raio=1, texture_atlas=textura, texture_indices=fornalha),
    Cubo(inital_position=[11, 2.0, 7], raio=1, texture_atlas=textura, texture_indices=fornalha2),
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

cuboAranha = Cubo(inital_position=[5, 2.0, 7], raio=0.995, texture_atlas=textura, texture_indices=teia)

frame_count = 0
start_time = time.time()

while not glfw.window_should_close(window):
    # Processa eventos de entrada (teclado/mouse)
    glfw.poll_events()
    camera.process_input(window)

    # Limpa os buffers de cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Atualiza a câmera (configura a matriz de modelo-visão)
    camera.update_camera()

    minecraft.draw()
    stive.draw()

    # Configura as luzes (deve ser feito após a atualização da câmera)
    luz.configurar_luz_potual(GL_LIGHT4, [2, 3, 0], [1, 0.2, 0.2], 0.1)
    luz.configurar_luz_direcional(GL_LIGHT5, [0, 0.4, 1], [0.8, 0.5, 0.5], 2)
    luz.configurar_luz_spot(GL_LIGHT6, [0, 5, 15], [1, -0.2, -1], [0.5, 0.5, 0.5], 100, 50, 20)

    # Desenha os objetos (após configurar as luzes)
    glCallList(lista_de_exebicao)  # Exibe a lista de exibição
    esfera.draw(3, 0, 0)  # Desenha a esfera
    cuboAranha.draw(0, 0, 0, camera.camera_pos)  # Desenha o cubo

    # Calcula e exibe o FPS
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        print(f"FPS: {frame_count}")
        frame_count = 0
        start_time = time.time()

    # Troca os buffers para exibir o frame
    glfw.swap_buffers(window)

# Finaliza o GLFW
glfw.terminate()
