import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
class Skybox:
    def __init__(self, textures):
        self.textures = [self.load_texture(t) for t in textures]

    def load_texture(self):
        image = Image.open("./imgs/skybox.png")
        image = image.convert("RGBA")
        width, height = image.size
        texture_data = np.array(list(image.getdata()), np.uint8)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        return texture

    def draw(self):
        glPushMatrix()
        glTranslatef(0, 0, -500)  # Posicione o skybox atrás da cena
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        # Desenhe a caixa aqui (6 faces) aplicando a textura
        glPopMatrix()
