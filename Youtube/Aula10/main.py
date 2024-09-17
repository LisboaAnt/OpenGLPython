import glfw
from OpenGL.GL import *
import numpy as np
import math

# Inicializar a janela GLFW
def init_window(width, height, title):
    if not glfw.init():
        return None
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        return None
    glfw.make_context_current(window)
    return window

# Função para desenhar a linha (curva)
def draw_curve():
    glBegin(GL_LINE_STRIP)
    for i in range(100):
        t = i / 100.0
        x = 0.5 * math.cos(2 * math.pi * t)  # Curva circular para exemplo
        y = 0.5 * math.sin(2 * math.pi * t)
        glVertex2f(x, y)
    glEnd()

# Função para desenhar um quadrado
def draw_square(x, y, size):
    half_size = size / 2
    glBegin(GL_QUADS)
    glVertex2f(x - half_size, y - half_size)
    glVertex2f(x + half_size, y - half_size)
    glVertex2f(x + half_size, y + half_size)
    glVertex2f(x - half_size, y + half_size)
    glEnd()

# Função para mover o quadrado com teclas WASD
def handle_input(window, x, y, speed):
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        y += speed
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        y -= speed
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        x -= speed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        x += speed
    return x, y

# Função para verificar colisão (simples para este exemplo)
def check_collision(square_x, square_y, square_size, curve_points):
    half_size = square_size / 2
    for (cx, cy) in curve_points:
        if (square_x - half_size <= cx <= square_x + half_size) and (square_y - half_size <= cy <= square_y + half_size):
            return True
    return False

# Função principal
def main():
    window = init_window(800, 600, "OpenGL Line and Square Collision")
    if not window:
        return

    # Configuração inicial
    glClearColor(0.0, 0.0, 0.0, 1.0)
    square_x, square_y = 0.0, 0.0  # Posição inicial do quadrado
    square_size = 0.1
    speed = 0.0001

    # Gerar pontos da curva
    curve_points = [(0.5 * math.cos(2 * math.pi * t), 0.5 * math.sin(2 * math.pi * t)) for t in np.linspace(0, 1, 100)]

    # Loop principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Desenhar linha (curva)
        glColor3f(0.0, 1.0, 0.0)
        draw_curve()

        # Desenhar quadrado
        glColor3f(1.0, 0.0, 0.0)
        draw_square(square_x, square_y, square_size)

        # Atualizar posição do quadrado com teclas WASD
        square_x, square_y = handle_input(window, square_x, square_y, speed)

        # Verificar colisão
        if check_collision(square_x, square_y, square_size, curve_points):
            print("Colisão detectada!")

        # Trocar os buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
