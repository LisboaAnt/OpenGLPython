from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Iluminacao:
    def __init__(self):
        self.lights = []  # Lista para armazenar as luzes
        self.light_positions = []  # Lista para armazenar as posições das luzes
        self.light_colors = []  # Lista para armazenar as cores das luzes

    def configure_environment(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # Configuração do material da superfície
        material_diffuse = [0.5, 0.5, 0.5, 1.0]  # Cor difusa
        material_specular = [1.0, 1.0, 1.0, 1.0]  # Cor especular (branca)
        shininess = 100.0  # Superfície polida
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

    def create_light(self, position, intensity, distance, color, light_id):
        """Configura a luz e a armazena na lista de luzes."""
        # Armazena os dados da luz em vez de configurar imediatamente
        self.lights.append(light_id)  # Armazena a luz na lista
        self.light_positions.append(position)  # Armazena a posição da luz
        self.light_colors.append((color, intensity, distance))  # Armazena a cor e intensidade da luz

    def move_light(self, light_id, new_position):
        """Atualiza a posição de uma luz existente."""
        index = self.lights.index(light_id)
        self.light_positions[index] = new_position  # Atualiza a posição na lista

    def show_lights(self):
        """Visualiza todas as luzes salvas como esferas na cena."""

        for index, light_id in enumerate(self.lights):
            position = self.light_positions[index]
            color, intensity, distance = self.light_colors[index]

            # Configura a luz para ser exibida
            glLightfv(light_id, GL_POSITION, [position[0], position[1], position[2], 1.0])
            glLightfv(light_id, GL_DIFFUSE, [color[0] * intensity, color[1] * intensity, color[2] * intensity, 1.0])
            glLightfv(light_id, GL_SPECULAR, [color[0], color[1], color[2], 1.0])

            # Define a distância que a luz afeta
            glLightf(light_id, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(light_id, GL_LINEAR_ATTENUATION, 0.0)
            glLightf(light_id, GL_QUADRATIC_ATTENUATION, 1.0 / (distance ** 2))  # Atuação quadrática

            glEnable(light_id)  # Habilita a luz

            """
            # Visualiza a posição da luz como uma esfera
            glPushMatrix()
            glTranslatef(position[0], position[1], position[2])  # Move para a posição da luz
            quadric = gluNewQuadric()
            gluSphere(quadric, 5, 32, 32)  # RAIO, PAREDES
            glPopMatrix()
            """