import glfw
from OpenGL.GL import *
import numpy as np

class Mesh:
    def __init__(self, start_pos, end_pos, normal, total_polygons):
        self.vertices = []
        self.normals = []

        # Calcular a configuração da malha
        polygons_x = int(np.sqrt(total_polygons))  # Número de polígonos na direção X
        polygons_y = int(np.ceil(total_polygons / polygons_x))  # Número de polígonos na direção Y

        # Deslocamento entre os pontos de início e fim
        delta_x = (end_pos[0] - start_pos[0]) / polygons_x
        delta_y = (end_pos[1] - start_pos[1]) / polygons_y

        for i in range(polygons_x):
            for j in range(polygons_y):
                # Verifica se ainda há polígonos para adicionar
                if len(self.vertices) // 8 >= total_polygons:  # 4 vértices por quadrado
                    break

                # Calculando os vértices do quadrado
                x0 = start_pos[0] + i * delta_x
                y0 = start_pos[1] + j * delta_y
                x1 = x0 + delta_x
                y1 = y0 + delta_y

                # Adiciona os vértices
                self.vertices.extend([
                    x0, y0,  # Inferior esquerdo
                    x1, y0,  # Inferior direito
                    x1, y1,  # Superior direito
                    x0, y1  # Superior esquerdo
                ])

                # Adiciona a normal
                self.normals.extend(normal * 4)  # A mesma normal para todos os vértices

        # Converte listas para arrays de float32
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.normals = np.array(self.normals, dtype=np.float32)

        # Habilita estados de array
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

    def draw(self):
        color = [1, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, color)
        glMaterialfv(GL_FRONT, GL_AMBIENT, color)
        glMaterialfv(GL_FRONT, GL_SHININESS, 100)

        # Define os ponteiros para os arrays de vértices e normais
        glVertexPointer(2, GL_FLOAT, 0, self.vertices)
        glNormalPointer(GL_FLOAT, 0, self.normals)

        # Desenha a malha
        glDrawArrays(GL_QUADS, 0, len(self.vertices) // 2)