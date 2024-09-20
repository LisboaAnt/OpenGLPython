import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

if not glfw.init():
    raise Exception("Falha ao iniciar")

# Habilita o buffer de profundidade
glfw.window_hint(glfw.DEPTH_BITS, 24)

width, height = 800, 600
window = glfw.create_window(width, height, "Aula 3", None, None)
if not window:
    raise Exception("Falha ao criar a janela")


glfw.make_context_current(window)



glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width / height, 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

#Variáveis da câmera
camera_pos = np.array([0.0, 0.0, 3])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw, pitch = -90.0, 0.0  # Ângulos de orientação da câmera

camera_speed = 0.005
keys = {}

#Variáveis Do Mause
first_mouse = True  # Indicador para verificar se é a primeira vez que o mouse é movido
cursor_disabled = False  # Indicador se o cursor está desativado
esc_pressed = False  # Indicador se a tecla ESC está pressionada
sensitivity = 0.1
last_x, last_y = width / 2, height / 2


def camera():
    global camera_pos, camera_front, camera_up
    glLoadIdentity()
    camera_target = camera_pos + camera_front
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])


def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def process_input():
    global camera_pos, camera_front, camera_up, camera_speed, cursor_disabled, esc_pressed, first_mouse
    if keys.get(glfw.KEY_W, False):
        camera_pos += camera_speed * camera_front
    if keys.get(glfw.KEY_S, False):
        camera_pos -= camera_speed * camera_front
    if keys.get(glfw.KEY_A, False):
        camera_pos -= np.cross(camera_front, camera_up) * camera_speed
    if keys.get(glfw.KEY_D, False):
        camera_pos += np.cross(camera_front, camera_up) * camera_speed

    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not esc_pressed:
        cursor_disabled = not cursor_disabled
        mode = glfw.CURSOR_DISABLED if cursor_disabled else glfw.CURSOR_NORMAL
        glfw.set_input_mode(window, glfw.CURSOR, mode)
        esc_pressed = True
        first_mouse = cursor_disabled
        if not cursor_disabled:
            glfw.set_cursor_pos(window, last_x, last_y)
    elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
        esc_pressed = False


def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse, camera_front, cursor_disabled, sensitivity

    # Se o cursor não estiver desativado, não faz nada com o movimento do mouse
    if not cursor_disabled:
        return

    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    # Calcula o deslocamento do mouse em relação à última posição conhecida
    xoffset = xpos - last_x
    yoffset = last_y - ypos

    # Atualiza as últimas coordenadas do mouse
    last_x = xpos
    last_y = ypos

    # Aplica a sensibilidade do mouse aos deslocamentos
    xoffset *= sensitivity
    yoffset *= sensitivity

    # Atualiza os ângulos de orientação da câmera com base no deslocamento do mouse
    yaw += xoffset
    pitch += yoffset

    # Limita o ângulo 'pitch' para não ultrapassar os limites superiores e inferiores
    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

    direction = np.array([
        np.cos(np.radians(yaw)) * np.cos(np.radians(pitch)),
        np.sin(np.radians(pitch)),
        np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))
    ])
    camera_front = direction / np.linalg.norm(direction)




glClearColor(0, 0.2, 0.5, 1)
glfw.set_key_callback(window, key_callback)
glfw.set_cursor_pos_callback(window, mouse_callback)


def create_cube():
    vertices = [
        # Front face
        -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0,
        # Back face
        -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0,
        # Left face
        -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0,
        # Right face
        1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
        # Top face
        -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
        # Bottom face
        -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0,
    ]
    return np.array(vertices, dtype='float32')





def configure_material():
    material_diffuse = [0.5, 0.5, 0.5, 1.0]  # Cor difusa
    material_specular = [1.0, 1.0, 1.0, 1.0]  # Cor especular (branca)
    shininess = 100.0  # Superfície polida
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)


def draw_cube(vertices):
    glBegin(GL_QUADS)
    normals = [
        (0.0, 0.0, 1.0), (0.0, 0.0, -1.0),
        (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)
    ]

    colors = [
        [1.0, 0.0, 0.0, 1.0],  # Vermelho
        [0.0, 1.0, 0.0, 1.0],  # Verde
        [0.0, 0.0, 1.0, 1.0],  # Azul
        [1.0, 1.0, 0.0, 1.0],  # Amarelo
        [1.0, 0.5, 0.0, 1.0],  # Laranja
        [0.5, 0.0, 0.5, 1.0]  # Roxo
    ]

    for i, normal in enumerate(normals):
        glNormal3f(*normal)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, colors[i])  # Aplica a cor do material correspondente à face

        for j in range(4):
            idx = i * 4 + j
            glVertex3f(vertices[idx * 3], vertices[idx * 3 + 1], vertices[idx * 3 + 2])

    glEnd()


def draw_light_cube(vertices):
    glPushMatrix()
    glTranslatef(1.0, 1.0, -2.0)
    glScalef(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    for i in range(0, 24, 3):
        glVertex3f(vertices[i], vertices[i + 1], vertices[i + 2])
    glEnd()
    glPopMatrix()


glEnable(GL_LIGHTING)
glEnable(GL_DEPTH_TEST)


configure_material()

cube_vertices = create_cube()


def configure_lights():
    # Posição da primeira luz
    light_position1 = [10.0, 10.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position1)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHT0)

    # Posição da segunda luz
    light_position2 = [-5.0, 5.0, 2.0, 1.0]
    glLightfv(GL_LIGHT1, GL_POSITION, light_position2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])  # Azul
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHT1)

    # Desenha um pequeno cubo na posição da primeira luz para visualização
    glPushMatrix()
    glTranslatef(*light_position1[:3])  # Move para a posição da primeira luz
    glColor3f(1, 0, 0)  # Cor do cubo (vermelho)

    quadric = gluNewQuadric()
    gluSphere(quadric, 2, 32, 32)  # Raio, slices, stacks
    glPopMatrix()

    # Desenha um pequeno cubo na posição da segunda luz para visualização
    glPushMatrix()
    glTranslatef(*light_position2[:3])  # Move para a posição da segunda luz
    glColor3f(0, 0, 1)  # Cor do cubo (azul)

    quadric = gluNewQuadric()
    gluSphere(quadric, 2, 32, 32)  # Raio, slices, stacks
    glPopMatrix()


# No loop principal, certifique-se de chamar configure_lights() após configurar a câmera.
while not glfw.window_should_close(window):
    glEnable(GL_DEPTH_TEST)
    glfw.poll_events()
    process_input()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    camera()

    configure_lights()  # Configure a luz

    glTranslatef(0.0, 0.0, -5)
    glPushMatrix()
    draw_cube(cube_vertices)
    glPopMatrix()

    glTranslatef(2, 1, 1)
    glPushMatrix()
    draw_cube(cube_vertices)
    glPopMatrix()

    glfw.swap_buffers(window)

glfw.terminate()