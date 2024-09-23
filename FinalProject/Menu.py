import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from freetype import Face
import time

class MainMenu:
    def __init__(self, window, width=800, height=600):
        self.window = window

        self.game_pause = False
        self.game_started = False

        self.font_path = "./fonts/Poppins/Poppins-Regular.ttf"
        self.font_size = 48
        self.face = Face(self.font_path)
        self.face.set_char_size(self.font_size * 64)
        self.base_spacing = 3
        self.text_cache = {}

        self.width = width
        self.height = height

        # Inicializar opções do menu
        self.controls = ['Start']
        self.settings = {
            'Back': 99,  # Adiciona a opção "Voltar" com índice 0
            'Up': 273,
            'Down': 274,
            'Left': 276,
        }
        self.current_menu = 'menu'
        self.selected_option = 0
        self.last_key_press_time = 0
        self.key_press_delay = 0.2

    def handle_events(self):
        current_time = time.time()

        if self.game_started:
            glfw.set_window_should_close(self.window, True)
            return

        if current_time - self.last_key_press_time > self.key_press_delay:
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.selected_option = (self.selected_option - 1) % len(self.get_current_menu_options())
                self.last_key_press_time = current_time
            elif glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.selected_option = (self.selected_option + 1) % len(self.get_current_menu_options())
                self.last_key_press_time = current_time
            elif glfw.get_key(self.window, glfw.KEY_ENTER) == glfw.PRESS:
                self.select_option()

    def get_current_menu_options(self):
        if self.current_menu == 'menu':
            return self.controls
        elif self.current_menu == 'settings':
            return list(self.settings.keys())

    def select_option(self):
        options = self.get_current_menu_options()
        selected_key = options[self.selected_option]

        if self.current_menu == 'menu':
            if self.selected_option == 0:  # Start
                glfw.set_window_size(self.window, self.width*2, self.height)
                self.game_started = True
            elif self.selected_option == 1:  # Settings
                self.current_menu = 'settings'
                self.selected_option = -1
        elif self.current_menu == 'settings':
            if selected_key == 'Back':
                self.current_menu = 'menu'
                self.selected_option = -1
            else:
                print("Não implementado")

    def paused(self):
        if glfw.get_key(self.window, glfw.KEY_P) == glfw.PRESS:
            self.game_pause = True

        if glfw.get_key(self.window, glfw.KEY_O) == glfw.PRESS:
            self.game_pause = False

        if self.game_pause:
            self.draw_text(100, 500, "TRON")
            while self.game_pause:
                glfw.poll_events()
                if glfw.get_key(self.window, glfw.KEY_P) == glfw.PRESS:
                    self.game_pause = True
                if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
                    self.game_pause = False
                    print("sair do pause")
                if glfw.get_key(self.window, glfw.KEY_ENTER) == glfw.PRESS:
                    self.game_pause = False
                    print("sair do pause com Enter")



    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.draw_text(100, 500, "TRON")

        options = self.get_current_menu_options()
        for i, option in enumerate(options):
            y = self.height-200 - i * 50
            if i == self.selected_option:
                self.draw_text(100, y, f"{option}/ <<")
            else:
                self.draw_text(100, y, option)

    def draw_text(self, x, y, text):
        glColor3f(0.5, 1, 1)
        for char in text:
            if char == '/':     # não lê / e adiciona 2 espaços
                x += 2 * self.base_spacing
                continue

            if char not in self.text_cache:
                self.face.load_char(char)
                bitmap = self.face.glyph.bitmap
                width, height = bitmap.width, bitmap.rows
                if width == 0 or height == 0:
                    continue

                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)

                texture_data = bytearray(width * height * 4)
                for i in range(height):
                    for j in range(width):
                        index = i * width + j
                        alpha = bitmap.buffer[index]
                        texture_data[index * 4: index * 4 + 3] = [0, 0, 255]
                        texture_data[index * 4 + 3] = alpha

                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
                self.text_cache[char] = (texture_id, width, height)

            texture_id, char_width, char_height = self.text_cache[char]
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1)
            glVertex2f(x, y)
            glTexCoord2f(1, 1)
            glVertex2f(x + char_width, y)
            glTexCoord2f(1, 0)
            glVertex2f(x + char_width, y + char_height)
            glTexCoord2f(0, 0)
            glVertex2f(x, y + char_height)
            glEnd()

            x += char_width + self.base_spacing
