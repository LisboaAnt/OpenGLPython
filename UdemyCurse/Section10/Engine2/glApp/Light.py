import pygame

from .Transformation import *
from .Uniform import *

class Light:
    def __init__(self, program_id, position =  pygame.Vector3(0, 0, 0),  light_number = 0):
        self.transformation = identity_matrix()
        self.program_id = program_id
        self.position = position
        self.light_number = light_number
        self.light_variable = "light_pos[" + str(light_number) + "]"


    def update(self):
        light_pos = Uniform("vec3", self.position)
        light_pos.find_variable(self.program_id, self.light_variable)
        light_pos.load()

