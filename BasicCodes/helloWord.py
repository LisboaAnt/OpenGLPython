import glfw
from OpenGL.GL import *

def main():
    glfw.init()

    window = glfw.create_window(800, 600, "Hello World", None, None)
    glfw.make_context_current(window)

    glViewport(0, 0, 800, 600)

    while not glfw.window_should_close(window):
        # processamento dos eventos
        glfw.poll_events()

        # renderizações como PyOpenGL
        glClearColor(0.2, 0.3, 0.3, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(1, 0, 0)  # habilitando a cor vermelha
        glBegin(GL_TRIANGLES)  # definindo a primitiva GL_TRIANGLES (triângulo)
        glVertex2f(-0.5, -0.5)  # coordenada do vértice inferior esquerdo
        glVertex2f(0.5, -0.5)  # coordenada do vértice inferior direito
        glVertex2f(0., 0.5)  # coordenada do vértice superior
        glEnd()

        # invertendo os buffers (backbuffer e frontbuffer)
        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()