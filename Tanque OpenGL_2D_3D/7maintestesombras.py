import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

def desenhar_esfera(x_centro, y_centro, z_centro, raio, altura_pixels):
    fatias = 40
    pilhas = 40

    for i in range(fatias):
        theta1 = i * 2.0 * np.pi / fatias
        theta2 = (i + 1) * 2.0 * np.pi / fatias

        glBegin(GL_TRIANGLE_STRIP)

        for j in range(pilhas+1):
            phi = j * np.pi / pilhas
            x = x_centro + raio * np.cos(theta1) * np.sin(phi)
            y = y_centro + raio * np.cos(phi) * altura_pixels  # Ajuste para desenhar em pixels de altura
            z = z_centro + raio * np.sin(theta1) * np.sin(phi)

            nx = x / raio
            ny = y / raio
            nz = z / raio

            glNormal3f(nx, ny, nz)
            glVertex3f(x, y, z)

            x = x_centro + raio * np.cos(theta2) * np.sin(phi)
            z = z_centro + raio * np.sin(theta2) * np.sin(phi)

            nx = x / raio
            nz = z / raio

            glNormal3f(nx, ny, nz)
            glVertex3f(x, y, z)

        glEnd()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Esfera OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = 800 / 600
        glOrtho(-1 * aspect_ratio, 1 * aspect_ratio, -1, 1, -1, 1)  # Define a projeção ortográfica

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        desenhar_esfera(0, 0, 0, 0.5, 10)  # Desenha uma esfera com centro (0, 0, 0), raio 0.5 e altura de 10 pixels

        glfw.swap_buffers(window)

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    glfw.terminate()

if __name__ == "__main__":
    main()
