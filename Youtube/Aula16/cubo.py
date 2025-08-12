from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import ctypes


class Cubo:
    def __init__(self, inital_position=[0.0, 0.0, 0.0], altura=1.0, largura=1.0, profundidade=1.0,
                 texture_atlas=None, texture_indices=[0,1,2,3,4,5], lighting=True, cores_faces=None, rotation=None):
        self.texture_atlas = texture_atlas
        self.texture_indices = texture_indices
        self.altura = altura
        self.largura = largura
        self.profundidade = profundidade
        self.position = inital_position
        self.lighting = lighting
        self.rotation = rotation if rotation else [0.0, 0.0, 0.0]
        
        # Cor padrão se não for especificada
        cor_padrao = [0.0, 0.184, 0.365, 1.0]  # RGBA(0, 47, 93, 255) normalizado
        self.cores_faces = cores_faces if cores_faces else [cor_padrao for _ in range(6)]
        
        # Configuração dos vértices e VBOs
        self.setup_mesh()
        
    def setup_mesh(self):
        # Metade das dimensões para centralizar o cubo
        hx = self.largura / 2
        hy = self.altura / 2
        hz = self.profundidade / 2
        
        # Vértices do cubo (posição, normal, texcoord)
        vertices = [
            # Frente (Z+)
            -hx, -hy,  hz,  0.0,  0.0,  1.0,  0.0, 0.0,  # 0
             hx, -hy,  hz,  0.0,  0.0,  1.0,  1.0, 0.0,  # 1
             hx,  hy,  hz,  0.0,  0.0,  1.0,  1.0, 1.0,  # 2
            -hx,  hy,  hz,  0.0,  0.0,  1.0,  0.0, 1.0,  # 3
            
            # Trás (Z-)
             hx, -hy, -hz,  0.0,  0.0, -1.0,  0.0, 0.0,  # 4
            -hx, -hy, -hz,  0.0,  0.0, -1.0,  1.0, 0.0,  # 5
            -hx,  hy, -hz,  0.0,  0.0, -1.0,  1.0, 1.0,  # 6
             hx,  hy, -hz,  0.0,  0.0, -1.0,  0.0, 1.0,  # 7
            
            # Cima (Y+)
            -hx,  hy,  hz,  0.0,  1.0,  0.0,  0.0, 0.0,  # 8
             hx,  hy,  hz,  0.0,  1.0,  0.0,  1.0, 0.0,  # 9
             hx,  hy, -hz,  0.0,  1.0,  0.0,  1.0, 1.0,  # 10
            -hx,  hy, -hz,  0.0,  1.0,  0.0,  0.0, 1.0,  # 11
            
            # Baixo (Y-)
            -hx, -hy, -hz,  0.0, -1.0,  0.0,  0.0, 0.0,  # 12
             hx, -hy, -hz,  0.0, -1.0,  0.0,  1.0, 0.0,  # 13
             hx, -hy,  hz,  0.0, -1.0,  0.0,  1.0, 1.0,  # 14
            -hx, -hy,  hz,  0.0, -1.0,  0.0,  0.0, 1.0,  # 15
            
            # Direita (X+)
             hx, -hy,  hz,  1.0,  0.0,  0.0,  0.0, 0.0,  # 16
             hx, -hy, -hz,  1.0,  0.0,  0.0,  1.0, 0.0,  # 17
             hx,  hy, -hz,  1.0,  0.0,  0.0,  1.0, 1.0,  # 18
             hx,  hy,  hz,  1.0,  0.0,  0.0,  0.0, 1.0,  # 19
            
            # Esquerda (X-)
            -hx, -hy, -hz, -1.0,  0.0,  0.0,  0.0, 0.0,  # 20
            -hx, -hy,  hz, -1.0,  0.0,  0.0,  1.0, 0.0,  # 21
            -hx,  hy,  hz, -1.0,  0.0,  0.0,  1.0, 1.0,  # 22
            -hx,  hy, -hz, -1.0,  0.0,  0.0,  0.0, 1.0   # 23
        ]
        
        # Índices para desenhar o cubo com triângulos
        indices = [
            0, 1, 2, 2, 3, 0,       # Frente
            4, 5, 6, 6, 7, 4,       # Trás
            8, 9, 10, 10, 11, 8,    # Cima
            12, 13, 14, 14, 15, 12, # Baixo
            16, 17, 18, 18, 19, 16, # Direita
            20, 21, 22, 22, 23, 20  # Esquerda
        ]
        
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
    
    def draw(self, x, y, z, shader, view_matrix, projection_matrix, camera_pos=None):
        shader.use()
        
        # Configurar matriz modelo
        model = np.identity(4, dtype=np.float32)
        
        # Translação
        translation = np.identity(4, dtype=np.float32)
        translation[0, 3] = self.position[0] + x
        translation[1, 3] = self.position[1] + y
        translation[2, 3] = self.position[2] + z
        
        # Rotação
        if self.rotation is not None:
            # Rotação X
            rotation_x = np.identity(4, dtype=np.float32)
            angle_x = np.radians(self.rotation[0])
            rotation_x[1, 1] = np.cos(angle_x)
            rotation_x[1, 2] = -np.sin(angle_x)
            rotation_x[2, 1] = np.sin(angle_x)
            rotation_x[2, 2] = np.cos(angle_x)
            
            # Rotação Y
            rotation_y = np.identity(4, dtype=np.float32)
            angle_y = np.radians(self.rotation[1])
            rotation_y[0, 0] = np.cos(angle_y)
            rotation_y[0, 2] = np.sin(angle_y)
            rotation_y[2, 0] = -np.sin(angle_y)
            rotation_y[2, 2] = np.cos(angle_y)
            
            # Rotação Z
            rotation_z = np.identity(4, dtype=np.float32)
            angle_z = np.radians(self.rotation[2])
            rotation_z[0, 0] = np.cos(angle_z)
            rotation_z[0, 1] = -np.sin(angle_z)
            rotation_z[1, 0] = np.sin(angle_z)
            rotation_z[1, 1] = np.cos(angle_z)
            
            # Combinar rotações
            rotation = np.dot(rotation_z, np.dot(rotation_y, rotation_x))
            model = np.dot(translation, rotation)
        else:
            model = translation
        
        # Enviar matrizes para o shader
        shader.set_mat4("model", model)
        shader.set_mat4("view", view_matrix)
        shader.set_mat4("projection", projection_matrix)
        
        # Configurar iluminação
        shader.set_bool("useLighting", self.lighting)
        
        # Desenhar cada face do cubo
        glBindVertexArray(self.VAO)
        
        for i in range(6):
            # Configurar textura ou cor
            if self.texture_atlas and i < len(self.texture_indices):
                shader.set_bool("useTexture", True)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, self.texture_atlas.texture_id)
                shader.set_int("textureSampler", 0)
                
                # Atualizar coordenadas de textura se necessário
                if hasattr(self.texture_atlas, 'get_uv_coords'):
                    uvs = self.texture_atlas.get_uv_coords(self.texture_indices[i])
                    # Aqui você precisaria atualizar as coordenadas de textura no VBO
            else:
                shader.set_bool("useTexture", False)
                cor = self.cores_faces[i]
                shader.set_vec3("materialDiffuse", cor[0], cor[1], cor[2])
            
            # Desenhar face
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(i * 6 * 4))
        
        glBindVertexArray(0)
    
    def ordenar_faces(self, faces, vertices, position, x, y, z, camera_pos):
        def distancia_face_para_camera(face):
            # Calcula o centro da face
            centro_face = np.zeros(3)
            for vertice_idx in face:
                centro_face += np.array(vertices[vertice_idx])
            centro_face /= len(face)
            
            # Adiciona a posição do cubo
            centro_face += np.array([position[0] + x, position[1] + y, position[2] + z])
            
            # Calcula a distância até a câmera
            return np.linalg.norm(centro_face - np.array(camera_pos))
        
        # Ordena as faces pela distância à câmera (do mais distante para o mais próximo)
        return sorted(faces, key=distancia_face_para_camera, reverse=True)