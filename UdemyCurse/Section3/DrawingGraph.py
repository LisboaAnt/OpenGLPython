import math
import numpy as np

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

pygame.init()

screen_width = 800
screen_height = 600
orth_width = 4
orth_height = 1

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Graphs in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,orth_width, 0, orth_height)


def plot_point():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()


def plot_graph():
    glBegin(GL_POINTS)
    px: GL_DOUBLE
    py: GL_DOUBLE
    for px in np.arange(0, 4, 0.0005):
        py = math.exp(-px) * math.cos(2 * math.pi * px)
        glVertex2f(px, py)
    glVertex2f(10, 10)
    glEnd()


def plot_lines():
    for l in points:
        glBegin(GL_LINE_STRIP) ## GL_LINE_LOOP TODAS AS LINHAS FICAM LIGADAS
        for coords in l:
            glVertex2f(coords[0], coords[1])
        glEnd()


done = False
init_ortho()
glPointSize(5)
points = []
line = []
mouse_down = False
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            line = []
            points.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEMOTION and mouse_down: #MOUSEMOTION registrar as coordenadas apenas quando o mouse é movido// MOUSEBUTTONDOWN PARA CLICK
            p = pygame.mouse.get_pos()
            line.append((map_value(0,screen_width, 0, orth_width,p[0]),
                           (map_value(0, screen_height, orth_height, 0, p[1])
                           )))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    plot_graph()
    pygame.display.flip()
    #pygame.time.wait(100)
pygame.quit()
