import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from freetype import Face

class MainMenu:
    def __init__(self, window, width=800, height=600):
        self.window = window
        self.game_started = False
        self.font_path = "./fonts/Poppins/Poppins-Regular.ttf"  # Fonte não negrito
        self.font_size = 48
        self.face = Face(self.font_path)
        self.face.set_char_size(self.font_size * 64)
        self.text_cache = {}
        self.width = width
        self.height = height
        self.base_spacing = 3  # Espaçamento base entre caracteres

    def handle_events(self):
        if glfw.get_key(self.window, glfw.KEY_ENTER) == glfw.PRESS:
            self.game_started = True
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Desenhe o texto e os botões do menu
        self.draw_text(200, 300, "Press//ENTER//to//Start")
        self.draw_text(200, 250, "Press//ESC//to//Quit")

    def draw_text(self, x, y, text):
        glColor3f(0, 0, 1)  # Cor do texto (azul)
        for char in text:
            if char == '/':
                # Ajustar o espaçamento para o caractere '/' sem desenhá-lo
                x += 2 * self.base_spacing
                continue

            if char not in self.text_cache:
                self.face.load_char(char)
                bitmap = self.face.glyph.bitmap
                width, height = bitmap.width, bitmap.rows
                if width == 0 or height == 0:
                    continue  # Pular caracteres com dimensões zero

                # Criar textura com alta qualidade
                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)

                # Preencher o buffer da textura com dados de bitmap
                texture_data = bytearray(width * height * 4)
                for i in range(height):
                    for j in range(width):
                        index = i * width + j
                        alpha = bitmap.buffer[index]
                        texture_data[index * 4 + 0] = 0  # Red
                        texture_data[index * 4 + 1] = 0  # Green
                        texture_data[index * 4 + 2] = 255  # Blue
                        texture_data[index * 4 + 3] = alpha  # Alpha

                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
                self.text_cache[char] = (texture_id, width, height)

            texture_id, char_width, char_height = self.text_cache[char]
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1)  # Invertido em Y para corrigir a orientação
            glVertex2f(x, y)
            glTexCoord2f(1, 1)
            glVertex2f(x + char_width, y)
            glTexCoord2f(1, 0)
            glVertex2f(x + char_width, y + char_height)
            glTexCoord2f(0, 0)
            glVertex2f(x, y + char_height)
            glEnd()

            # Ajustar o espaçamento para o próximo caractere
            x += char_width + self.base_spacing