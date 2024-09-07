import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image
import numpy as np
import math

# Vertex shader
VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
out vec2 TexCoords;
void main()
{
    gl_Position = vec4(position, 1.0);
    TexCoords = texCoords;
}
"""

# Fragment shader
FRAGMENT_SHADER = """
#version 330 core
in vec2 TexCoords;
out vec4 color;
uniform sampler2D texture1;
void main()
{
    color = texture(texture1, TexCoords);
}
"""

def create_mesh():
    # Cria uma malha paramétrica (grid simples)
    vertices = []
    tex_coords = []
    size = 1.0
    divisions = 50
    for i in range(divisions + 1):
        for j in range(divisions + 1):
            x = -size + 2 * size * i / divisions
            y = -size + 2 * size * j / divisions
            vertices.append([x, y, 0])
            tex_coords.append([i / divisions, j / divisions])

    vertices = np.array(vertices, dtype=np.float32)
    tex_coords = np.array(tex_coords, dtype=np.float32)

    indices = []
    for i in range(divisions):
        for j in range(divisions):
            start = i * (divisions + 1) + j
            indices.extend([start, start + 1, start + divisions + 1])
            indices.extend([start + 1, start + divisions + 2, start + divisions + 1])

    indices = np.array(indices, dtype=np.uint32)
    return vertices, tex_coords, indices

def load_texture(path):
    # Carrega a textura usando Pillow
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture

def main():
    # Inicializa GLFW
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Textura em Malha Paramétrica", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Compila e linka os shaders
    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Cria a malha e carrega a textura
    vertices, tex_coords, indices = create_mesh()
    texture = load_texture("path_to_your_texture.jpg")

    # Criação de VBOs, VAO e EBO
    VAO = glGenVertexArrays(1)
    VBOs = glGenBuffers(2)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBOs[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, VBOs[1])
    glBufferData(GL_ARRAY_BUFFER, tex_coords.nbytes, tex_coords, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 2 * tex_coords.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Configurações de textura
    glUseProgram(shader)
    glUniform1i(glGetUniformLocation(shader, "texture1"), 0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindTexture(GL_TEXTURE_2D, texture)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Limpeza
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(2, VBOs)
    glDeleteBuffers(1, [EBO])
    glfw.terminate()

if __name__ == "__main__":
    main()
