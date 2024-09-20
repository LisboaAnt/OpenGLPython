from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Iluminacao:
    def configure_lights(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)


        material_diffuse = [0.5, 0.5, 0.5, 1.0]  # Cor difusa
        material_specular = [1.0, 1.0, 1.0, 1.0]  # Cor especular (branca)
        shininess = 100.0  # Superfície polida
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

        # Posição da primeira luz
        light_position1 = [50.0, 10.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position1)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glEnable(GL_LIGHT0)

        # Posição da segunda luz
        light_position2 = [-50.0, -5.0, 2.0, 1.0]
        glLightfv(GL_LIGHT1, GL_POSITION, light_position2)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])  # Azul
        glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glEnable(GL_LIGHT1)

        # Desenha um pequeno cubo na posição da primeira luz para visualização
        glPushMatrix()
        glTranslatef(*light_position1[:3])  # Move para a posição da primeira luz
        glColor3f(1, 0, 0)  # Cor do cubo (vermelho)

        quadric = gluNewQuadric()
        gluSphere(quadric, 20, 32, 32)  # Raio, slices, stacks
        glPopMatrix()

        quadric = gluNewQuadric()
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0, 1])
        gluSphere(quadric, 20, 32, 32)  # Raio, slices, stacks
        glPopMatrix()
