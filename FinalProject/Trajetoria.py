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
        glColor4f(color[0], color[1], color[2], 0.2)  # Cor do cubo
        z = 0  # Valor fixo para a coordenada Z
        thickness = 20  #  tamanho

        if len(self.points) < 2:
            return  # Não há pontos suficientes para formar uma linha

        # Desenha cubos conectando os pontos
        for i in range(len(self.points) - 1):
            (x1, y1) = self.points[i]
            (x2, y2) = self.points[i + 1]

            glBegin(GL_QUADS)
            # Cálculo dos vértices
            for j in range(-thickness // 2, thickness // 2, thickness):
                for k in range(-thickness // 2, thickness // 2, thickness):
                    glVertex3f(x1 + j, y1 + k, z)
                    glVertex3f(x2 + j, y2 + k, z)
                    glVertex3f(x2 + j, y2 + k, z + thickness)
                    glVertex3f(x1 + j, y1 + k, z + thickness)

            glEnd()

    def check_collision(self, square_x, square_y, square_size):
        half_size = square_size / 2
        for (x, y) in self.points[:-1]:  # Não verificar o ponto atual
            if (square_x - half_size <= x <= square_x + half_size) and (square_y - half_size <= y <= square_y + half_size):
                return True
        return False