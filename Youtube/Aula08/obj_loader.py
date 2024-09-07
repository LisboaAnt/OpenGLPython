import trimesh
import numpy as np
from OpenGL.GL import *
import os


class ObjLoader:
    def __init__(self, file_path):
        # Verifica se o arquivo existe
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        # Tenta carregar o modelo
        try:
            # Carrega o modelo usando trimesh
            mesh = trimesh.load(file_path, triangulate=True)
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o arquivo OBJ: {e}")

        # Verifica se o mesh foi carregado
        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError("O arquivo OBJ não contém uma malha válida")

        # Usa o mesh carregado
        self.mesh = mesh

        # Extrai vértices, normais e faces
        self.vertices = np.array(self.mesh.vertices, dtype=np.float32)
        self.faces = np.array(self.mesh.faces, dtype=np.uint32)
        self.vertex_normals = np.array(self.mesh.vertex_normals, dtype=np.float32)

        # Cria buffers OpenGL
        self.vertex_buffer = glGenBuffers(1)
        self.normal_buffer = glGenBuffers(1)
        self.index_buffer = glGenBuffers(1)
        self._create_buffers()

    def _create_buffers(self):
        # Cria e vincula o buffer de vértices
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Cria e vincula o buffer de normais
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_normals.nbytes, self.vertex_normals, GL_STATIC_DRAW)

        # Cria e vincula o buffer de índices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)

    def draw(self):
        # Vincula o buffer de vértices e define os ponteiros de atributos
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        # Vincula o buffer de normais e define os ponteiros de atributos
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(1)

        # Vincula o buffer de índices e desenha a malha
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glDrawElements(GL_TRIANGLES, self.faces.size, GL_UNSIGNED_INT, None)

        # Desativa os arrays de atributos de vértices
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
