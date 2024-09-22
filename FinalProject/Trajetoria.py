import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import numpy as np


class Trajetoria:
    def __init__(self, max_points, interval):
        self.points = []
        self.max_points = max_points
        self.last_time = time.time()
        self.interval = interval

    def add_point(self, x, y):
        current_time = time.time()
        # Adiciona o ponto se o intervalo de tempo entre pontos for respeitado
        if (current_time - self.last_time) > self.interval:
            self.points.append((x, y))
            self.last_time = current_time

        # Remove o ponto mais antigo se exceder o número máximo de pontos
        if len(self.points) > self.max_points:
            self.points.pop(0)

    import numpy as np

    def draw(self, color):
        # Desabilita a iluminação
        glDisable(GL_LIGHTING)

        # Habilita o modo de mistura
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Define a cor com transparência
        glColor4f(color[0], color[1], color[2], 0.8)
        z = 0  # Rastro em relação com a coordenada Z
        height = 40  # Altura do retângulo

        for i in range(len(self.points) - 1):
            (x1, y1) = self.points[i]
            (x2, y2) = self.points[i + 1]

            if i == 0:
                # Desenha um triângulo para o primeiro segmento
                glBegin(GL_TRIANGLES)  # Inicia o desenho de triângulos
                glNormal3f(0.0, 0.0, 1.0)
                glVertex3f(x1, y1, z)  # Vértice inferior esquerdo
                glVertex3f(x2, y2, z)  # Vértice inferior direito
                glVertex3f(x2, y2, z + height)  # Vértice superior
                glEnd()  # Finaliza o desenho do triângulo
            else:
                # Desenha um retângulo para os outros segmentos
                glBegin(GL_QUADS)  # Inicia o desenho de quadriláteros
                glNormal3f(0.0, 0.0, 1.0)  # Normal da superfície
                glVertex3f(x1, y1, z)  # Vértice inferior esquerdo
                glVertex3f(x2, y2, z)  # Vértice inferior direito
                glVertex3f(x2, y2, z + height)  # Vértice superior direito
                glVertex3f(x1, y1, z + height)  # Vértice superior esquerdo
                glEnd()  # Finaliza o desenho do quadrilátero

                glLineWidth(10.0)
                glBegin(GL_LINES)
                glNormal3f(0.0, 0.0, 1.0)
                glVertex3f(x1, y1, height / 2)
                glVertex3f(x2, y2, height / 2)
                glEnd()
                glLineWidth(1.0)

        # Desabilita a mistura e habilita novamente a iluminação
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

    def check_collision(self, square_x, square_y, square_size):
        half_size = square_size / 2
        for (x, y) in self.points[:-1]:  # Não verificar o ponto atual
            if (square_x - half_size <= x <= square_x + half_size) and (square_y - half_size <= y <= square_y + half_size):
                return True
        return False