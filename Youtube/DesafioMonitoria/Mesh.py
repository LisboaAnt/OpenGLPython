import glfw
from OpenGL.GL import *
import numpy as np

class Mesh:
    def __init__(self, start_pos, end_pos, normal, total_polygons, texture_atlas=None, texture_index=0):
        self.vertices = []
        self.normals = []
        self.texture_coords = []
        self.texture_atlas = texture_atlas
        self.texture_index = texture_index

        # Calcular a configuração da malha
        polygons_x = int(np.sqrt(total_polygons))  # Número de polígonos na direção X
        polygons_y = int(np.ceil(total_polygons / polygons_x))  # Número de polígonos na direção Y

        # Deslocamento entre os pontos de início e fim
        delta_x = (end_pos[0] - start_pos[0]) / polygons_x
        delta_y = (end_pos[1] - start_pos[1]) / polygons_y

        # Se tiver textura, pega as coordenadas UV base
        if self.texture_atlas:
            uvs = self.texture_atlas.get_uv_coords(self.texture_index)
            u_min, v_min = uvs[0]  # Coordenadas do canto inferior esquerdo
            u_max, v_max = uvs[2]  # Coordenadas do canto superior direito

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

                # Adiciona coordenadas de textura proporcionais à posição no mesh
                if self.texture_atlas:
                    # Calcula as coordenadas UV proporcionalmente à posição no mesh
                    u0 = u_min + (u_max - u_min) * (i / polygons_x)
                    u1 = u_min + (u_max - u_min) * ((i + 1) / polygons_x)
                    v0 = v_min + (v_max - v_min) * (j / polygons_y)
                    v1 = v_min + (v_max - v_min) * ((j + 1) / polygons_y)
                    
                    self.texture_coords.extend([
                        u0, v0,  # Inferior esquerdo
                        u1, v0,  # Inferior direito
                        u1, v1,  # Superior direito
                        u0, v1   # Superior esquerdo
                    ])

        # Converte listas para arrays de float32
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.normals = np.array(self.normals, dtype=np.float32)
        if self.texture_atlas:
            self.texture_coords = np.array(self.texture_coords, dtype=np.float32)

        # Habilita estados de array
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        if self.texture_atlas:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def draw(self):
        glPushMatrix()
        glTranslatef(0, -1.5, 0)
        glRotatef(90, 1, 0, 0)

        if self.texture_atlas:
            color = [0.95, 0.84, 0.68, 1.00]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glMaterialfv(GL_FRONT, GL_SPECULAR, color)
            glMaterialfv(GL_FRONT, GL_AMBIENT, color)
            glMaterialfv(GL_FRONT, GL_SHININESS, 100)

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_atlas.texture_id)
            glTexCoordPointer(2, GL_FLOAT, 0, self.texture_coords)
        else:
            color = [1, 1, 1, 1.0]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glMaterialfv(GL_FRONT, GL_SPECULAR, color)
            glMaterialfv(GL_FRONT, GL_AMBIENT, color)
            glMaterialfv(GL_FRONT, GL_SHININESS, 100)

        # Define os ponteiros para os arrays de vértices e normais
        glVertexPointer(2, GL_FLOAT, 0, self.vertices)
        glNormalPointer(GL_FLOAT, 0, self.normals)

        # Desenha a malha
        glDrawArrays(GL_QUADS, 0, len(self.vertices) // 2)

        if self.texture_atlas:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()