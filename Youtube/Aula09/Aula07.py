import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from cubo import Cubo
from camera import Camera
from obstacle import Obstacle
import pyassimp
import pyassimp.postprocess

class ObjLoader:
    def __init__(self, file_name):
        # Carrega o modelo usando pyassimp
        self.scene = pyassimp.load(file_name, pyassimp.postprocess.aiProcess_Triangulate)
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.extract_data()

    def extract_data(self):
        for mesh in self.scene.meshes:
            self.vertices.extend(mesh.vertices)
            if mesh.normals.any():
                self.normals.extend(mesh.normals)
            if mesh.has_texture_coords(0):
                self.texcoords.extend(mesh.texturecoords[0])

    def draw(self):
        glBegin(GL_TRIANGLES)
        for i in range(0, len(self.vertices), 3):
            if len(self.normals) > i:
                glNormal3fv(self.normals[i])
            if len(self.texcoords) > i:
                glTexCoord2fv(self.texcoords[i])
            glVertex3fv(self.vertices[i])
        glEnd()

    def release(self):
        pyassimp.release(self.scene)

if not glfw.init():
    raise Exception("Falha ao iniciar")

width, height = 800, 600
window = glfw.create_window(width, height, "Aula 3", None, None)
if not window:
    raise Exception("Falha ao criar a janela")

icon = "icon.png"
glfw.set_window_icon(window, 1, Image.open(icon))
glfw.make_context_current(window)

glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Variáveis
keys = {}

cubo = Cubo()
camera1 = Camera(keys, width, height, 0.5, 0.5, 0.5)

obstacles = []
hitbox = camera1.get_hitbox()
obstacles.append(Obstacle(hitbox[0], hitbox[1], hitbox[2], hitbox[3], hitbox[4], hitbox[5], 1))
hitbox = cubo.get_hitbox()
obstacles.append(Obstacle(hitbox[0], hitbox[1], hitbox[2], hitbox[3], hitbox[4], hitbox[5], 2))

# Carregando o modelo .obj
obj_loader = ObjLoader('house_obj.obj')

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

glClearColor(0, 0.2, 0.5, 1)
glfw.set_key_callback(window, key_callback)
glfw.set_cursor_pos_callback(window, camera1.mouse_callback)

while not glfw.window_should_close(window):
    glfw.poll_events()
    camera1.process_input(window, obstacles)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    camera1.camera()

    cubo.draw(0, 0, 0)
    obstacles[1].desenha()
    obstacles[0].desenhar_hitbox()

    # Desenhando o modelo carregado
    obj_loader.draw()

    glfw.swap_buffers(window)

glfw.terminate()
obj_loader.release()
