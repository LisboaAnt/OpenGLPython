from OpenGL.GL import *
import numpy as np
import ctypes
from PIL import Image


class Esfera:
    def __init__(self, initial_position=[0.0, 0.0, 0.0], texture_file='./images/world.jpg'):
        self.position = initial_position
        self.texture_id = self.load_texture(texture_file)
        
        # Configuração dos vértices e VBOs
        self.setup_mesh()
        
    def load_texture(self, texture_file):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Configurações de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Carrega a imagem
        try:
            image = Image.open(texture_file)
            img_data = np.array(list(image.getdata()), np.uint8)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)
        except Exception as e:
            print(f"Erro ao carregar textura: {e}")
            return 0
            
        return texture_id
    
    def setup_mesh(self, radius=1.0, slices=40, stacks=40):
        vertices = []
        indices = []
        
        # Gerar vértices
        for i in range(stacks + 1):
            V = i / stacks
            phi = V * np.pi
            
            for j in range(slices + 1):
                U = j / slices
                theta = U * 2 * np.pi
                
                # Coordenadas esféricas para cartesianas
                x = radius * np.sin(phi) * np.cos(theta)
                y = radius * np.cos(phi)
                z = radius * np.sin(phi) * np.sin(theta)
                
                # Normal (normalizada)
                nx = x / radius
                ny = y / radius
                nz = z / radius
                
                # Coordenadas de textura
                u = U
                v = V
                
                # Adicionar vértice
                vertices.extend([x, y, z, nx, ny, nz, u, v])
        
        # Gerar índices
        for i in range(stacks):
            for j in range(slices):
                first = i * (slices + 1) + j
                second = first + slices + 1
                
                # Primeiro triângulo
                indices.extend([first, second, first + 1])
                
                # Segundo triângulo
                indices.extend([second, second + 1, first + 1])
        
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        
        # Criar VAO, VBO e EBO
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        
        # Vincular VAO
        glBindVertexArray(self.VAO)
        
        # Configurar VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # Configurar EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        
        # Configurar atributos de vértice
        # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        # Coordenadas de textura
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)
        
        # Desvincula o VAO
        glBindVertexArray(0)
    
    def draw(self, x, y, z, shader, view_matrix, projection_matrix, radius=None, slices=None, stacks=None):
        # Recria a malha se os parâmetros mudaram
        if (radius and radius != self.radius) or (slices and slices != self.slices) or (stacks and stacks != self.stacks):
            self.setup_mesh(radius or self.radius, slices or self.slices, stacks or self.stacks)
        
        shader.use()
        
        # Configurar matriz modelo
        model = np.identity(4, dtype=np.float32)
        
        # Translação
        model[0, 3] = self.position[0] + x
        model[1, 3] = self.position[1] + y
        model[2, 3] = self.position[2] + z
        
        # Enviar matrizes para o shader
        shader.set_mat4("model", model)
        shader.set_mat4("view", view_matrix)
        shader.set_mat4("projection", projection_matrix)
        
        # Configurar textura
        shader.set_bool("useTexture", True)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        shader.set_int("textureSampler", 0)
        
        # Desenhar esfera
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
