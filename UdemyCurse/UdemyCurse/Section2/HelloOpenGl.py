import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,640,0,480)
def initialise():
    window = glfw.create_window(screen_width, screen_height, "OpenGL in Python", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create window")
    glfw.make_context_current(window)
    glfw.set_window_pos(window, 200, 200)

    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor4f(*drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)

    # modelview
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -5)
    glLoadIdentity()
    glViewport(0, 0, screen_width, screen_height)
    glEnable(GL_DEPTH_TEST)
    glTranslatef(0, 0, -2)

    glfw.swap_interval(1)  # Limita a taxa de quadros


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1, 10, 0, 1)
    glPushMatrix()
    glPopMatrix()
    glfw.swap_buffers(window)


glfw.init()
initialise()
window = glfw.get_current_context()

while not glfw.window_should_close(window):
    glfw.poll_events()
    display()

glfw.terminate()
