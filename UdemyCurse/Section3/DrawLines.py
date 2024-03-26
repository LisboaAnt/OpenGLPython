import math
import numpy as np

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

pygame.init()

screen_width = 1000
screen_height = 800
orth_width = 640
orth_height = 480

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Graphs in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,orth_width, 0, orth_height)


def plot_lines():
    for l in points:
        glBegin(GL_LINE_STRIP) ## GL_LINE_LOOP TODAS AS LINHAS FICAM LIGADAS
        for coords in l:
            glVertex2f(coords[0], coords[1])
        glEnd()

#Salavndo as linhas
def save_drawing():
    f = open("drawing.txt", "w")
    f.write(str(len(points)) + "\n")
    for l in points:
        f.write(str(len(l)) + "\n")
        for coords in l:
            f.write(str(coords[0]) + " "+str(coords[1]) + "\n")
    f.close()
    print("Drawing Saved")

def load_drawing():
    f = open("drawing.txt", "r")
    num_of_lines = int(f.readline())
    global points
    global line
    points = []
    for l in range(num_of_lines):
        line = []
        points.append(line)
        num_of_coords = int(f.readline())
        for coord_number in range(num_of_coords):
            px,py = [float(value) for value in next(f).split()]
            line.append((px,py))
            print(str(px) + "," + str(py))


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_drawing()
            elif event.key == pygame.K_l:
                load_drawing()
            elif event.key == pygame.K_SPACE:
                points = []
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
    plot_lines()
    pygame.display.flip()
    #pygame.time.wait(100)
pygame.quit()
