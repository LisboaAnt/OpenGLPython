import glfw
from OpenGL.GL import *

def draw_triangle():
    glBegin(GL_TRIANGLES)  
    # Vértice 1 (inferior esquerdo) - cor vermelha
    glColor3f(1, 0, 0)#R,G,B
    glVertex2f(-0.5, -0.5)  

    # Vértice 2 (inferior direito) - cor verde
    glColor3f(0, 1, 0)
    glVertex2f(0.5, -0.5) #x,y 

    # Vértice 3 (superior) - cor azul
    glColor3f(0, 0, 1)
    glVertex2f(0., 0.5)  

    glEnd()

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

        draw_triangle()  # Chamando a função para desenhar o triângulo

        # invertendo os buffers (backbuffer e frontbuffer)
        glfw.swap_buffers(window)
    glfw.terminate()
    
if __name__ == "__main__":
    main()
