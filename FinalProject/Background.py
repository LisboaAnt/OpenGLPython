import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class TronBackground:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.create_background()
        self.size = 100

    def create_background(self):
        # Configurações iniciais
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        glLineWidth(1.0)  # Espessura das linhas

    def draw_background(self):
        glDisable(GL_LIGHTING)
        glLineWidth(1)

        # Tamanho de cada quadrado
        tamanho = int(self.grid_size*1.5)  # Tamanho de cada quadrado

        # Tamanho da malha em termos de quadrados
        self.grid_count = (self.width // tamanho, self.height // tamanho)

        # Desenhar linhas
        glBegin(GL_LINES)
        glColor3f(0, 0.5, 0.5)  # Cor azul brilhante

        # Desenhar linhas verticais
        for i in range(-self.width // 2, self.width // 2 + tamanho, tamanho):
            glVertex2f(i, -self.height // 2)
            glVertex2f(i, self.height // 2)

        # Desenhar linhas horizontais
        for i in range(-self.height // 2, self.height // 2 + tamanho, tamanho):
            glVertex2f(-self.width // 2, i)
            glVertex2f(self.width // 2, i)
        glEnd()

        glEnable(GL_LIGHTING)
        glNormal3fv([0, 0, 1])
        posicaoz = -10  # Z em -10
        tamanho = 400
        # Desenhar a malha de quadrados
        for x in range(-self.width // 2, self.width // 2, tamanho):
            for y in range(-self.height // 2, self.height // 2, tamanho):
                glBegin(GL_QUADS)
                self.configurar_material(color=[1, 1, 1])  # Configurar material
                glVertex3f(x, y, posicaoz)  # Inferior esquerdo
                glVertex3f(x + tamanho, y, posicaoz)  # Inferior direito
                glVertex3f(x + tamanho, y + tamanho, posicaoz)  # Superior direito
                glVertex3f(x, y + tamanho, posicaoz)  # Superior esquerdo
                glEnd()


    def configurar_material(self, color, alpha=0.6):
        # Define a cor do material (RGBA) com transparência
        ambient = [color[0] * 0.2, color[1] * 0.2, color[2] * 0.2, alpha]  # Cor ambiente
        diffuse = [color[0], color[1], color[2], alpha]  # Cor difusa
        specular = [color[0] * 2.0, color[1] * 2.0, color[2] * 2.0, 1.0]  # Aumenta a cor especular
        shininess = [1.0]  # Brilho do material mais alto para reflexão intensa

        # Configura os materiais
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, shininess)




    def desenhar_retangulo(self, posicaox, posicaoy, posicaoz, tamanhx, tamanhy, color, normal):
        # Define os vértices da face frontal do retângulo
        vertices = np.array([
            [0, 0, 0],  # Inferior esquerdo
            [tamanhx, 0, 0],  # Inferior direito
            [tamanhx, 0, tamanhy],  # Superior direito
            [0, 0, tamanhy]  # Superior esquerdo
        ], dtype='float32')

        # Transladar a face
        vertices += np.array([posicaox, posicaoy, posicaoz])

        # Define a normal
        glNormal3fv(normal)

        # Desenhar a face
        glBegin(GL_QUADS)
        self.configurar_material(color)  # Configura o material
        for vertex in vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])  # Adiciona o vértice
        glEnd()

    def desenhar_retangulo2(self, posicaox, posicaoy, posicaoz, tamanhx, tamanhy, color, normal):
        self.configurar_material(color)  # Configura o material
        # Define os vértices da face frontal do retângulo
        vertices = np.array([
            [0, 0, 0],  # Inferior esquerdo
            [0, tamanhx, 0],  # Inferior direito
            [0, tamanhx, tamanhy],  # Superior direito
            [0, 0, tamanhy]  # Superior esquerdo
        ], dtype='float32')

        # Transladar a face
        vertices += np.array([posicaox, posicaoy, posicaoz])

        # Define a normal
        glNormal3fv(normal)

        # Desenhar a face
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])  # Adiciona o vértice
        glEnd()

    def desenhar_grade_retangulos(self, posicaox, posicaoy, posicaoz, tamanhx, tamanhy, num_divisoes_x, color, normal):
        largura_menor = tamanhx / num_divisoes_x  # Tamanho dos retângulos menores
        altura_menor = tamanhy  # Mantém a altura constante

        for i in range(num_divisoes_x):
            # Calcular a posição de cada retângulo menor
            x = posicaox + i * largura_menor
            self.desenhar_retangulo(x, posicaoy, posicaoz, largura_menor, altura_menor, color, normal)

    def desenhar_grade_retangulos2(self, posicaox, posicaoy, posicaoz, tamanhx, tamanhy, num_divisoes_x, color, normal):
        largura_menor = tamanhx / num_divisoes_x  # Tamanho dos retângulos menores
        altura_menor = tamanhy  # Mantém a altura constante

        for i in range(num_divisoes_x):
            # Calcular a posição de cada retângulo menor
            y = posicaoy + i * largura_menor
            self.desenhar_retangulo2(posicaox, y, posicaoz, largura_menor, altura_menor, color, normal)

    def draw(self):

        self.draw_background()

        # Grades em diferentes posições Z
        self.desenhar_grade_retangulos(-2500, 2500, 0, 5000, 150, 10, [1.0, 1.0, 1.0], [0.0, -1.0, 0.0])  # Frente
        self.desenhar_grade_retangulos(-2500, -2500, 0, 5000, 150, 10, [1.0, 1.0, 1.0], [0.0, 1.0, 0.0])  # Atrás

        # Retângulos laterais
        self.desenhar_grade_retangulos2(-2500, -2500, 0, 5000, 150, 10, [1.0, 1.0, 1.0],
                                        [1.0, 0.0, 0.0])  # Lado esquerdo
        self.desenhar_grade_retangulos2(2500, -2500, 0, 5000, 150, 10, [1.0, 1.0, 1.0],
                                        [-1.0, 0.0, 0.0])  # Lado direito

