import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from pyglm import glm
from camera import Camera
from cubo import Cubo

def desenhar_eixos():
    glLineWidth(2)

    glBegin(GL_LINES)
    # Eixo X (vermelho)
    glColor3f(1, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(10, 0, 0)

    # Eixo Y (verde)
    glColor3f(0, 1, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(0, 10, 0)

    # Eixo Z (azul)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -10)
    glVertex3f(0, 0, 10)
    glEnd()

    # Ticks nos eixos
    glLineWidth(1)
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for i in range(-10, 11):
        if i == 0:
            continue
        # Eixo X
        glVertex3f(i, -0.1, 0)
        glVertex3f(i,  0.1, 0)
        # Eixo Y
        glVertex3f(-0.1, i, 0)
        glVertex3f( 0.1, i, 0)
        # Eixo Z
        glVertex3f(0, -0.1, i)
        glVertex3f(0,  0.1, i)
    glEnd()


cubo = Cubo(inital_position=[0, 0, 0], altura=0.01, largura=2.0, profundidade=2.0, cores_faces=[
    [0.64, 0.70, 0.73, 1.00],
    [0.64, 0.70, 0.73, 1.00],
    [0.64, 0.70, 0.73, 1.00],
    [0.64, 0.70, 0.73, 1.00],
    [5.64, 0.70, 0.73, 1.00],
    [0.64, 0.70, 0.73, 1.00], ])

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Desenho 3D", None, None)
    if not window:
        glfw.terminate()
        return

    camera = Camera(800, 800)
    glfw.set_key_callback(window, camera.key_callback)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)

    glfw.make_context_current(window)
    glViewport(0, 0, 800, 800)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        camera.process_input(window)

        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Projeção em perspectiva
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/800, 0.1, 100.0)

        # Câmera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.update_camera()

        desenhar_eixos()
        cubo.draw(0,0,0)
        
        glPushMatrix()
        glTranslatef(5,3,-5)
        glRotatef(-45, 0, 1, 0)
        glRotatef(90, 1, 0, 0)
        glScalef(4, 1, 3)
        cubo.draw(0,0,0)


        glPopMatrix()

        glFlush()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
