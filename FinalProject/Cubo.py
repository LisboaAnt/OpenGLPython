from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

class Cubo:
    def __init__(self, tamanho=1.0, textura_path="./imgs/skybox/skyboxF.png"):
        self.tamanho = tamanho
        self.textura_id = None
        if textura_path:
            self.textura_id = self.load_texture(textura_path)  # Carrega a textura se o caminho for fornecido
        self.posicao = [500.0, 500.0, 0.0]

    def load_texture(self, path):
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # Inverte a imagem verticalmente
        img_data = img.convert("RGBA").tobytes()  # Converte a imagem para bytes

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        # Define parâmetros da textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

    def desenhar(self):
        glEnable(GL_TEXTURE_2D)  # Ativa o uso de texturas
        glBindTexture(GL_TEXTURE_2D, self.textura_id)  # Aplica a textura

        self.desenhar_cubo(self.tamanho)

        glDisable(GL_TEXTURE_2D)  # Desativa o uso de texturas

    def transladar(self, x, y, z):
        self.posicao = [x, y, z]

    def desenhar_cubo(self, lado):
        vertices = [
            [-1, -1, -1],  # Vértice 0
            [1, -1, -1],  # Vértice 1
            [1, 1, -1],  # Vértice 2
            [-1, 1, -1],  # Vértice 3
            [-1, -1, 1],  # Vértice 4
            [1, -1, 1],  # Vértice 5
            [1, 1, 1],  # Vértice 6
            [-1, 1, 1]  # Vértice 7
        ]

        # Normais para cada face
        normais = [
            [0, 0, -1],  # Normal da face frontal (eixo Z negativo)
            [1, 0, 0],  # Normal da face direita (eixo X positivo)
            [0, 0, 1],  # Normal da face traseira (eixo Z positivo)
            [-1, 0, 0],  # Normal da face esquerda (eixo X negativo)
            [0, 1, 0],  # Normal da face superior (eixo Y positivo)
            [0, -1, 0]  # Normal da face inferior (eixo Y negativo)
        ]

        faces = [
            [0, 1, 2, 3],  # Face frontal
            [1, 5, 6, 2],  # Face direita
            [5, 4, 7, 6],  # Face traseira
            [4, 0, 3, 7],  # Face esquerda
            [3, 2, 6, 7],  # Face superior
            [4, 5, 1, 0]  # Face inferior
        ]

        for i, face in enumerate(faces):
            glBegin(GL_QUADS)
            glNormal3fv(normais[i])  # Define a normal da face atual
            for vertice_index in face:
                # Define coordenadas de textura para centralizar a textura em cada face
                if i == 0:  # Face frontal
                    glTexCoord2f(vertices[vertice_index][0] + 1, vertices[vertice_index][1] + 1)
                elif i == 1:  # Face direita
                    glTexCoord2f(vertices[vertice_index][2] + 1, vertices[vertice_index][1] + 1)
                elif i == 2:  # Face traseira
                    glTexCoord2f(vertices[vertice_index][0] + 1, vertices[vertice_index][1] + 1)
                elif i == 3:  # Face esquerda
                    glTexCoord2f(vertices[vertice_index][2] + 1, vertices[vertice_index][1] + 1)
                elif i == 4:  # Face superior
                    glTexCoord2f(vertices[vertice_index][0] + 1, vertices[vertice_index][2] + 1)
                elif i == 5:  # Face inferior
                    glTexCoord2f(vertices[vertice_index][0] + 1, vertices[vertice_index][2] + 1)

                glVertex3f(
                    self.posicao[0] + vertices[vertice_index][0] * lado / 2,
                    self.posicao[1] + vertices[vertice_index][1] * lado / 2,
                    self.posicao[2] + vertices[vertice_index][2] * lado / 2
                )
            glEnd()
