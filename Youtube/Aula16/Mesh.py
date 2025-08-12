import glfw
from OpenGL.GL import *
import numpy as np
import ctypes

class Mesh:
    def __init__(self, start_pos, end_pos, normal, total_polygons, texture_atlas=None, texture_index=0):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.normal = normal
        self.total_polygons = total_polygons
        self.texture_atlas = texture_atlas
        self.texture_index = texture_index
        
        # Configuração dos vértices e VBOs
        self.setup_mesh()
        
    def setup_mesh(self):
        # Calcular dimensões
        width = self.end_pos[0] - self.start_pos[0]
        height = self.end_pos[1] - self.start_pos[1]
        
        # Calcular tamanho de cada célula
        cell_width = width / self.total_polygons
        cell_height = height / self.total_polygons
        
        # Criar vértices e índices
        vertices = []
        indices = []
        
        # Obter coordenadas UV se houver textura
        uvs = None
        if self.texture_atlas:
            uvs = self.texture_atlas.get_uv_coords(self.texture_index)
        
        # Gerar malha de vértices
        for i in range(self.total_polygons + 1):
            for j in range(self.total_polygons + 1):
                # Posição
                x = self.start_pos[0] + j * cell_width
                y = self.start_pos[1] + i * cell_height
                z = 0.0  # Assumindo que a malha está no plano XY
                
                # Normal
                nx, ny, nz = self.normal
                
                # Coordenadas de textura
                if uvs:
                    # Mapear coordenadas de textura proporcionalmente à posição na malha
                    u = (j / self.total_polygons) * (uvs[1][0] - uvs[0][0]) + uvs[0][0]
                    v = (i / self.total_polygons) * (uvs[2][1] - uvs[0][1]) + uvs[0][1]
                else:
                    u = j / self.total_polygons
                    v = i / self.total_polygons
                
                # Adicionar vértice
                vertices.extend([x, y, z, nx, ny, nz, u, v])
        
        # Gerar índices para triângulos
        for i in range(self.total_polygons):
            for j in range(self.total_polygons):
                # Calcular índices dos vértices para o quad atual
                top_left = i * (self.total_polygons + 1) + j
                top_right = top_left + 1
                bottom_left = (i + 1) * (self.total_polygons + 1) + j
                bottom_right = bottom_left + 1
                
                # Primeiro triângulo (top_left, bottom_left, bottom_right)
                indices.extend([top_left, bottom_left, bottom_right])
                
                # Segundo triângulo (top_left, bottom_right, top_right)
                indices.extend([top_left, bottom_right, top_right])
        
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        
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
    
    def draw(self, shader, view_matrix, projection_matrix):
        shader.use()
        
        # Configurar matriz modelo (identidade - sem transformações)
        model = np.identity(4, dtype=np.float32)
        
        # Enviar matrizes para o shader
        shader.set_mat4("model", model)
        shader.set_mat4("view", view_matrix)
        shader.set_mat4("projection", projection_matrix)
        
        # Configurar textura
        if self.texture_atlas:
            shader.set_bool("useTexture", True)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_atlas.texture_id)
            shader.set_int("textureSampler", 0)
        else:
            shader.set_bool("useTexture", False)
            shader.set_vec3("materialDiffuse", 0.7, 0.7, 0.7)  # Cor cinza claro
        
        # Desenhar malha
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)