import pygame.key
from pygame.locals import *
from OpenGL.GLU import *
from Cube import *
from LoadMesh import *

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Transformations in Python')
cube = Cube(GL_LINE_LOOP)
mesh = LoadMesh("./Resources/teapot.obj", GL_LINE_LOOP)

eye = [0, 0, 0]


def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 500.0)


def init_camera():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    gluLookAt(eye[0], eye[1], eye[2], 0, 0, 0, 0, 1, 0)  # Pq o gluLookAt(0,5,{0},0,0,0,0,1,0) não mostra nada?
    """eyeX, eyeY, eyeZ: As coordenadas do ponto de onde a câmera está olhando. Isso especifica a posição da câmera no espaço 3D. centerX, centerY, centerZ: Isso especifica o ponto no espaço 3D para onde a câmera está direcionada. upX, upY, upZ: Isso determina a orientação da câmera em relação ao mundo."""
    glEnable(GL_DEPTH_TEST)


def display():  ##NÃO ENTENDI MUITO BEM
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init_camera()
    glPushMatrix()
    mesh.draw()
    glPopMatrix()


done = False
initialise()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            eye[2] += 0.2
        if keys[pygame.K_UP]:
            eye[2] -= 0.2

    display()
    pygame.display.flip()
    pygame.time.wait(0)
pygame.quit()
