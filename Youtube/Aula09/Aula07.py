import glfw
from OpenGL.GL import *
import time


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


# Função para desenhar o quadrado
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


# Função para desenhar a linha da trajetória
def draw_trajectory(trajectory):
    glBegin(GL_LINE_STRIP)
    for (x, y) in trajectory:
        glVertex2f(x, y)
    glEnd()


# Função para verificar colisão entre o quadrado e a trajetória (linha)
def check_collision_square_line(square_x, square_y, square_size, trajectory):
    half_size = square_size / 2
    for (x, y) in trajectory:
        # Verifica se qualquer ponto da linha está dentro da área do quadrado
        if (square_x - half_size <= x <= square_x + half_size) and (square_y - half_size <= y <= square_y + half_size):
            return True
    return False


# Função principal
def main():
    window = init_window(800, 600, "OpenGL Square and Line Collision")
    if not window:
        return

    # Configuração inicial
    glClearColor(0.0, 0.0, 0.0, 1.0)
    square_x, square_y = 0.0, 0.0  # Posição inicial do quadrado
    square_size = 0.1
    speed = 0.0001
    max_points = 30  # Limite máximo de pontos na linha
    trajectory = []  # Lista de pontos para a trajetória do quadrado
    last_position = (square_x, square_y)  # Armazena a última posição do quadrado
    last_time = time.time()  # Temporizador para controlar a geração da linha

    # Loop principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Atualizar posição do quadrado com teclas WASD
        new_square_x, new_square_y = handle_input(window, square_x, square_y, speed)

        # Adicionar à trajetória se o quadrado se moveu significativamente a cada 0.1 segundo
        current_time = time.time()
        if (new_square_x, new_square_y) != last_position and (current_time - last_time) > 0.3:
            trajectory.append((new_square_x, new_square_y))
            last_position = (new_square_x, new_square_y)
            last_time = current_time

        # Limitar o tamanho da linha a 30 pontos
        if len(trajectory) > max_points:
            trajectory.pop(0)

        # Desenhar trajetória do quadrado
        glColor3f(0.0, 0.0, 1.0)
        draw_trajectory(trajectory)

        # Desenhar quadrado
        glColor3f(1.0, 0.0, 0.0)
        draw_square(new_square_x, new_square_y, square_size)

        # Verificar colisão do quadrado com a linha que ele gerou
        if check_collision_square_line(new_square_x, new_square_y, square_size, trajectory[:-1]):
            print("Colisão detectada!")

        # Atualizar posição do quadrado
        square_x, square_y = new_square_x, new_square_y

        # Trocar os buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
