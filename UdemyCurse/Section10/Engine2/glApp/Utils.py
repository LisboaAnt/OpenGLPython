from OpenGL.GL import *
import numpy as np


def format_vertices(coordinates, triangles):
    all_triangles = []
    for t in range(0, len(triangles), 3):
        all_triangles.append(coordinates[triangles[t]])
        all_triangles.append(coordinates[triangles[t + 1]])
        all_triangles.append(coordinates[triangles[t + 2]])
    return np.array(all_triangles, np.float32)

def format_colors(colors, triangles):
    """Expande a lista de cores para ter um valor por vértice expandido.

    - Se houver menos cores do que índices de vértices, usa-se módulo para repetir a paleta.
    - Se as cores estiverem alinhadas por índice de coordenada, o mapeamento segue os índices de 'triangles'.
    """
    all_colors = []
    if len(colors) == 0:
        return np.zeros((len(triangles), 3), np.float32)
    for t in range(0, len(triangles), 3):
        all_colors.append(colors[triangles[t] % len(colors)])
        all_colors.append(colors[triangles[t + 1] % len(colors)])
        all_colors.append(colors[triangles[t + 2] % len(colors)])
    return np.array(all_colors, np.float32)

def compile_shader(shader_type, shader_source):
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error_message = "\n" + error_message.decode("utf-8")
        raise Exception(error_message)
    return shader_id

def create_program(vertex_shader_code, fragment_shader_code):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not link_success:
        info = glGetShaderInfoLog(program_id)
        raise RuntimeError(info)
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id