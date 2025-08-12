from OpenGL.GL import *
import numpy as np
import ctypes

class Forma:
    def __init__(self, shader, vertices):
        self.shader = shader
        self.vertices = np.array(vertices, dtype=np.float32)
        self.setup_buffers()
        self.model = np.identity(4, dtype=np.float32)

    def setup_buffers(self):
        # Criando VAO e VBO
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Configuração dos atributos
        # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        # Textura
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)
        # Cor
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(8 * 4))
        glEnableVertexAttribArray(3)

    def draw(self, view_matrix, projection_matrix):
        self.shader.use()
        self.shader.set_int("useTexture", 0)
        
        # Enviando as matrizes para o shader
        self.shader.set_mat4("model", self.model)
        self.shader.set_mat4("view", view_matrix)
        self.shader.set_mat4("projection", projection_matrix)

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices) // 11)

    def cleanup(self):
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteBuffers(1, [self.VBO]) 