import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class TextRenderer:
    def __init__(self, font_name="Arial", font_size=48):
        pygame.font.init()
        self.font = pygame.font.SysFont(font_name, font_size)

    def render_text(self, text, x, y, width=800, height=600):
        # Renderizar o texto em uma superfície do pygame
        text_surface = self.font.render(text, True, (255, 255, 255), (0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        text_width, text_height = text_surface.get_size()

        # Configurar a projeção ortográfica para renderizar em 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)  # Definimos uma tela de 800x600
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Renderizar a textura do texto
        glRasterPos2f(x, y)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        # Restaurar a matriz original
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
