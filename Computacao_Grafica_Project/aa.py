import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import cos, sin
import numpy as np

def desenhar_esfera():
    fatias = 40
    pilhas = 40
    raio = 0.5

    for i in range(0, fatias):
        theta1 = i * 2.0 * np.pi / fatias
        theta2 = (i + 1) * 2.0 * np.pi / fatias

        glBegin(GL_TRIANGLE_STRIP)

        for j in range(0, pilhas+1):
            phi = j * np.pi / pilhas
            x = cos(theta1) * sin(phi)
            y = cos(phi)
            z = sin(theta1) * sin(phi)

            nx = x / raio
            ny = y / raio
            nz = z / raio

            glNormal3f(nx, ny, nz)
            glVertex3f(x, y, z)

            x = cos(theta2) * sin(phi)
            z = sin(theta2) * sin(phi)

            nx = x / raio
            nz = z / raio

            glNormal3f(nx, ny, nz)
            glVertex3f(x, y, z)

        glEnd()

def principal():
    if not glfw.init():
        return

    janela = glfw.create_window(640, 480, "Iluminação", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    
    #TESTE AQUI
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    while not glfw.window_should_close(janela):
        largura, altura = glfw.get_framebuffer_size(janela)
        proporcao = largura / float(altura)

        glViewport(0, 0, largura, altura)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50.0, proporcao, 1.0, 10.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        posicao_luz = [2.0, 1.0, 1.0, 0.0]
        cor_luz = [1.0, 0.0, 0.0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, cor_luz)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        

        desenhar_esfera()

        glfw.swap_buffers(janela)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    principal()
