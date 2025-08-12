import glfw
from OpenGL.GL import *
from shader import Shader
from forma import Forma
from camera import Camera
import numpy as np

class Renderer:
    def __init__(self, width=800, height=600, title="OpenGL com Shaders"):
        if not glfw.init():
            raise Exception("GLFW não pôde ser inicializado!")

        self.width = width
        self.height = height
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Falha ao criar a janela GLFW")

        glfw.make_context_current(self.window)
        
        # Configurações do OpenGL
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.3, 0.3, 1.0)

        # Inicializa a câmera
        self.camera = Camera(width, height)
        
        # Configura callbacks
        glfw.set_key_callback(self.window, self.camera.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.camera.mouse_callback)

        self.shader = Shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
        self.formas = []
        
        # Cria matriz de projeção
        self.projection = self.create_projection_matrix(45.0, width/height, 0.1, 100.0)

    def create_projection_matrix(self, fov, aspect, near, far):
        # Cria matriz de projeção em perspectiva
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        projection = np.zeros((4, 4), dtype=np.float32)
        projection[0, 0] = f / aspect
        projection[1, 1] = f
        projection[2, 2] = (far + near) / (near - far)
        projection[2, 3] = 2.0 * far * near / (near - far)
        projection[3, 2] = -1.0
        return projection

    def adicionar_triangulo(self):
        # Triângulo simples no centro da tela
        vertices_triangulo = [
            # Posição      Normal    UV       Cor
            -0.5, -0.5, 0.0,  0,0,1,  0.0,0.0,  1.0,0.0,0.0,  # Vermelho
             0.5, -0.5, 0.0,  0,0,1,  1.0,0.0,  0.0,1.0,0.0,  # Verde
             0.0,  0.5, 0.0,  0,0,1,  0.5,1.0,  0.0,0.0,1.0,  # Azul
        ]
        self.formas.append(Forma(self.shader, vertices_triangulo))

    def executar(self):
        while not glfw.window_should_close(self.window):
            # Processa entrada
            self.camera.process_input(self.window)
            
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Obtém a matriz de visualização da câmera
            view_matrix = self.camera.get_view_matrix()

            # Desenha todas as formas
            for forma in self.formas:
                forma.draw(view_matrix, self.projection)

            glfw.swap_buffers(self.window)

    def cleanup(self):
        for forma in self.formas:
            forma.cleanup()
        glfw.terminate() 