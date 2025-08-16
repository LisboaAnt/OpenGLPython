from OpenGL.GL import *
from .Mesh import *
import numpy as np
import pygame
import random
from .Utils import *
from .Transformation import *


class LoadMesh(Mesh):
    def __init__(self, filename, program_id, draw_type=GL_TRIANGLES, location=pygame.Vector3(0, 0, 0),
                rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                scale=pygame.Vector3(1, 1, 1),
                move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                move_translation=pygame.Vector3(0, 0, 0),
                move_scale=pygame.Vector3(1, 1, 1),
                ):
        coordinates, triangles, uvs, uvs_ind, normals, normals_ind = self.load_drawing(filename)
        vertices = format_vertices(coordinates, triangles)
        vertex_normals = format_vertices(normals, normals_ind)
        vertex_uvs = format_vertices(uvs, uvs_ind)
        colors = []
        for i in range(len(vertices)):
            colors.append(random.random())
            colors.append(random.random())
            colors.append(random.random())
        super().__init__(program_id, vertices, vertex_normals, vertex_uvs, colors, draw_type, location, rotation, scale, 
                        move_rotation=move_rotation, 
                        move_translation=move_translation, 
                        move_scale=move_scale,
                        vertex_normals=vertex_normals,
                        vertex_uvs=vertex_uvs)

    def load_drawing(self, filename):
        vertices = []
        triangles = []
        normals = []
        normals_ind = []
        uvs = []
        uvs_ind = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))

                if line[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line[3:].split()]
                    normals.append((vx, vy, vz))

                if line[:2] == "vt":
                    vx, vy = [float(value) for value in line[3:].split()]
                    uvs.append((vx, vy))

                if line[:2] == "f ":
                    t1, t2, t3 = [value for value in line[2:].split()]
                    triangles.append([int(value) for value in t1.split('/')][0]-1)
                    triangles.append([int(value) for value in t2.split('/')][0]-1)
                    triangles.append([int(value) for value in t3.split('/')][0]-1)
                    
                    uvs_ind.append([int(value) for value in t1.split('/')][1]-1)
                    uvs_ind.append([int(value) for value in t2.split('/')][1]-1)
                    uvs_ind.append([int(value) for value in t3.split('/')][1]-1)

                    
                    normals_ind.append([int(value) for value in t1.split('/')][2]-1)
                    normals_ind.append([int(value) for value in t2.split('/')][2]-1)
                    normals_ind.append([int(value) for value in t3.split('/')][2]-1)
                line = fp.readline()
        return vertices, triangles, uvs, uvs_ind, normals, normals_ind

