import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np

class Mesh1:
    def __init__(self, start_pos, end_pos, normal, total_polygons, texture_file='ground.jpg'):
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.texture_id = None

        if texture_file:
            self.texture_id = self.load_texture(texture_file)

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
                    x0, y1   # Superior esquerdo
                ])

                # Adiciona a normal
                self.normals.extend(normal * 4)  # A mesma normal para todos os vértices

                # Adiciona as coordenadas UV (mapeamento de textura normalizado para uma única textura)
                u0 = i / polygons_x
                v0 = j / polygons_y
                u1 = (i + 1) / polygons_x
                v1 = (j + 1) / polygons_y

                self.uvs.extend([
                    u0, v0,  # Inferior esquerdo
                    u1, v0,  # Inferior direito
                    u1, v1,  # Superior direito
                    u0, v1   # Superior esquerdo
                ])

        # Converte listas para arrays de float32
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.normals = np.array(self.normals, dtype=np.float32)
        self.uvs = np.array(self.uvs, dtype=np.float32)

        # Habilita estados de array
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def load_texture(self, texture_file):
        # Carregar a textura usando PIL
        image = Image.open(texture_file)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(image.getdata()), np.uint8)

        # Gerar e carregar a textura
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return texture_id

    def draw(self):
        color = [1, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, color)
        glMaterialfv(GL_FRONT, GL_AMBIENT, color)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        # Ativar textura
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # Define os ponteiros para os arrays de vértices, normais e coordenadas UV
        glVertexPointer(2, GL_FLOAT, 0, self.vertices)
        glNormalPointer(GL_FLOAT, 0, self.normals)
        glTexCoordPointer(2, GL_FLOAT, 0, self.uvs)

        # Desenha a malha
        glDrawArrays(GL_QUADS, 0, len(self.vertices) // 2)

        # Desativar textura
        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
