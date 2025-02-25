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
from loadObjs import LoasObjs
from colisao import Colisao

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
textura = TextureAtlas('./images/minecraft.jpg', (32, 16))
esfera = Esfera()

# Exemplo de uso:
colisao = Colisao()
colisao.adicionar_objeto("obj1", (0, 0, 0), (2, 2, 2))
colisao.adicionar_objeto("obj2", (5, 2.0, 7), (2, 2, 2))


steve = LoasObjs(obj_path="./objects/steve.obj", scale=(10, 10, 10), position=(10, 5, 10))
bikini = LoasObjs(obj_path="./objects/bikini.obj", scale=(100, 100, 100), position=(10, -20, 10))
naruto = LoasObjs(obj_path="./objects/naruto.obj", scale=(1, 1, 1), position=(5, 0, 10))

lista_cubos = [
    Cubo(inital_position=[2 * i, 0.0, 2 * j], raio=1, texture_atlas=textura, texture_indices=[3, 3, 3, 3, 2, 50])
    for i in range(10)
    for j in range(10)
]

teia = [66, 66, 66, 66, 66, 66]
craftable = [141, 142, 141, 142, 140, 140]
fornalha = [145, 145, 143, 145, 146, 146]
fornalha2 = [145, 145, 144, 145, 146, 146]

texture_Skybox = TextureAtlas('./images/skybox_atlas.png', (3, 2))

novos_cubos = [
    Cubo(inital_position=[0, 0, 0], raio=2000, texture_atlas=texture_Skybox, texture_indices=[2, 0, 1, 3, 4, 5],
         lighting=False),
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

    steve.draw()
    naruto.draw()
    bikini.draw()

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
    glfw.poll_events()
    camera.process_input(window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera.update_camera()

    glCallList(lista_de_exebicao)
    print(colisao.pode_mover("obj1", (camera.camera_pos[0], camera.camera_pos[1], camera.camera_pos[2])))
    colisao.atualizar_posicao("obj1", (camera.camera_pos[0], camera.camera_pos[1], camera.camera_pos[2]))
    colisao.desenhar_colisao()
    esfera.draw(3, 0, 0)

    #luz.configurar_luz_potual(GL_LIGHT2, [2, 1, 0], [0.6, 0.2, 0.2], 0.1)

    #luz.configurar_luz_potual(GL_LIGHT3, [0, 1, 2], [0.2, 0.2, 1], 0.1)

    luz.configurar_luz_potual(GL_LIGHT4, [2, 3, 0], [1, 0.2, 0.2], 0.1)

    luz.configurar_luz_direcional(GL_LIGHT5, [1, 1, 1], [0.5, 0.5, 0.5], 2)

    luz.configurar_luz_spot(GL_LIGHT6, [0, 5, 15], [1, -0.2, -1], [0.5, 0.5, 0.5], 100, 50, 20)

    frame_count += 1
    elapsed_time = time.time() - start_time

    cuboAranha.draw(0, 0, 0, camera.camera_pos)

    if elapsed_time >= 1:
        print(f"FPS: {frame_count}")
        frame_count = 0
        start_time = time.time()

    glfw.swap_buffers(window)

glfw.terminate()
