import glfw
from OpenGL.GL import *

# Função de inicialização do GLFW
def init():
    if not glfw.init():
        return False
    return True

# Função para criar a janela
def create_window():
    window = glfw.create_window(800, 600, "Hello, World!", None, None)
    if not window:
        glfw.terminate()
        return None
    glfw.make_context_current(window)
    return window

# Função de renderização
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa o buffer de cor e profundidade
    glfw.set_window_title(window, "Hello, World!")  # Redefine o título da janela como "Hello, World!"
    glfw.swap_buffers(window)  # Troca os buffers

# Função principal
def main():
    if not init():
        return
    global window
    window = create_window()
    if not window:
        return
    while not glfw.window_should_close(window):
        display()  # Renderiza a cena
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()  # Chama a função principal
