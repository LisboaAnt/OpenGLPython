import glfw
from OpenGL.GL import *
import math
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

class Quadrado:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = 0.0  # Ângulo de rotação em graus
        self.rotation_speed = 0.05  # Velocidade de rotação

    def draw(self):
        half_size = self.size / 2
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glRotatef(self.angle, 0, 0, 1)  # Rotacionar em torno do centro do quadrado
        glBegin(GL_QUADS)
        glVertex2f(-half_size, -half_size)
        glVertex2f(half_size, -half_size)
        glVertex2f(half_size, half_size)
        glVertex2f(-half_size, half_size)
        glEnd()
        glPopMatrix()

    def move(self, window):
        # Girar o quadrado com as teclas A e D
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.angle += self.rotation_speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.angle -= self.rotation_speed

        # Mover para frente ou para trás com as teclas W e S
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y += self.speed * math.sin(math.radians(self.angle))
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.x -= self.speed * math.cos(math.radians(self.angle))
            self.y -= self.speed * math.sin(math.radians(self.angle))

    # Calcula a posição da parte de trás do quadrado
    def get_back_position(self):
        half_size = self.size / 1.5
        back_x = self.x - half_size * math.cos(math.radians(self.angle))
        back_y = self.y - half_size * math.sin(math.radians(self.angle))
        return back_x, back_y

class Trajetoria:
    def __init__(self, max_points, interval):
        self.points = []
        self.max_points = max_points
        self.last_time = time.time()
        self.interval = interval

    def add_point(self, x, y):
        current_time = time.time()
        # Adiciona o ponto se o intervalo de tempo entre pontos for respeitado
        if (current_time - self.last_time) > self.interval:
            self.points.append((x, y))
            self.last_time = current_time

        # Remove o ponto mais antigo se exceder o número máximo de pontos
        if len(self.points) > self.max_points:
            self.points.pop(0)

    def draw(self):
        glBegin(GL_LINE_STRIP)
        for (x, y) in self.points:
            glVertex2f(x, y)
        glEnd()

    def check_collision(self, square_x, square_y, square_size):
        half_size = square_size / 2
        for (x, y) in self.points[:-1]:  # Não verificar o ponto atual
            if (square_x - half_size <= x <= square_x + half_size) and (square_y - half_size <= y <= square_y + half_size):
                return True
        return False

# Função principal
def main():
    window = init_window(800, 600, "OpenGL Square and Line Collision")
    if not window:
        return

    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Inicializar o quadrado e a trajetória
    quadrado = Quadrado(0.0, 0.0, 0.1, 0.0001)
    trajetoria = Trajetoria(max_points=30, interval=0.1)

    # Loop principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Mover e desenhar o quadrado
        quadrado.move(window)
        glColor3f(1.0, 0.0, 0.0)
        quadrado.draw()

        # Adicionar o ponto da parte de trás do quadrado na trajetória
        back_x, back_y = quadrado.get_back_position()
        trajetoria.add_point(back_x, back_y)

        # Desenhar a trajetória
        glColor3f(0.0, 0.0, 1.0)
        trajetoria.draw()

        # Verificar colisão do quadrado com a trajetória
        if trajetoria.check_collision(quadrado.x, quadrado.y, quadrado.size):
            print("Colisão detectada!")

        # Trocar os buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
