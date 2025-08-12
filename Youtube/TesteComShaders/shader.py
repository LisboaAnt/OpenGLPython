import OpenGL.GL.shaders as shaders
from OpenGL.GL import *
import numpy as np

class Shader:
    def __init__(self, vertex_path, fragment_path):
        self.program = self.create_shader(vertex_path, fragment_path)

    def create_shader(self, vertex_path, fragment_path):
        with open(vertex_path, 'r') as file:
            vertex_shader_source = file.read()

        with open(fragment_path, 'r') as file:
            fragment_shader_source = file.read()

        shader_program = shaders.compileProgram(
            shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        )

        return shader_program

    def use(self):
        glUseProgram(self.program)

    def set_int(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def set_float(self, name, value):
        glUniform1f(glGetUniformLocation(self.program, name), value)

    def set_vec3(self, name, x, y, z):
        glUniform3f(glGetUniformLocation(self.program, name), x, y, z)

    def set_mat4(self, name, matrix):
        loc = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, matrix)
