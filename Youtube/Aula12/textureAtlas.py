from OpenGL.GL import *
import numpy as np
from PIL import Image


class TextureAtlas:
    def __init__(self, texture_file, atlas_size):
        self.texture_file = texture_file
        self.atlas_size = atlas_size
        self.texture_id = self.load_texture()

    def load_texture(self):
        image = Image.open(self.texture_file)
        image = image.convert('RGBA')
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        img_data = np.array(list(image.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  # Filtro de aumento (GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_NEAREST_MIPMAP_NEAREST)  # Filtro de redução com mipmaps
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 4)
        # Carrega a textura e gera os mipmaps
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id

    def get_uv_coords(self, index):
        cols, rows = self.atlas_size
        col = index % cols
        row = index // cols

        u0 = col / cols
        v0 = 1 - (row + 1) / rows
        u1 = (col + 1) / cols
        v1 = 1 - row / rows

        return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
