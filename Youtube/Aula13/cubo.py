from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image


class Cubo:
    def __init__(self, inital_position=[0.0, 0.0, 0.0],raio = 0.99999, texture_atlas=None, texture_indices=[0,1,2,3,4,5], lighting = True):
        self.texture_atlas = texture_atlas
        self.texture_indices = texture_indices
        self.raio = raio
        self.position = inital_position
        self.texture_id = None
        self.lighting = lighting


    def draw(self, x, y, z, camera_pos = None):
        if not self.lighting:
            glDisable(GL_LIGHTING)

        vertices = [
            [-self.raio, -self.raio, -self.raio],
            [-self.raio, self.raio, -self.raio],
            [self.raio, self.raio, -self.raio],
            [self.raio, -self.raio, -self.raio],
            [-self.raio, -self.raio, self.raio],
            [-self.raio, self.raio, self.raio],
            [self.raio, self.raio, self.raio],
            [self.raio, -self.raio, self.raio],
        ]
        faces = [
            [3, 0, 1, 2],  # front
            [7, 3, 2, 6],  # dir
            [4, 7, 6, 5],  # tras
            [0, 4, 5, 1],  # esq
            [6, 2, 1, 5],
            [4, 0, 3, 7],  # inf
        ]

        normais = [
            [0, 0, -1],
            [1, 0, 0],
            [0, 0, 1],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0]
        ]


        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)

        if self.texture_atlas:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_atlas.texture_id)

        if camera_pos is not None:
            faces_ordenadas = self.ordenar_faces(faces, vertices, self.position, x, y, z, camera_pos)

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthMask(GL_FALSE)
        else:
            faces_ordenadas = range(len(faces))

        glBegin(GL_QUADS)
        for i in faces_ordenadas:
            glNormal3fv(normais[i])
            if self.texture_atlas:
                uvs = self.texture_atlas.get_uv_coords(self.texture_indices[i])
                for j, vertex in enumerate(faces[i]):
                    glTexCoord2fv(uvs[j])
                    glVertex3fv(vertices[vertex])
            else:
                for vertex in faces[i]:
                    glVertex3fv(vertices[vertex])
        glEnd()

        if camera_pos is not None:
            glDepthMask(GL_TRUE)
            glDisable(GL_BLEND)

        if self.texture_atlas:
            glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        if not self.lighting:
            glEnable(GL_LIGHTING)

    def ordenar_faces(self, faces, vertices,position, x, y, z, camera_pos):
        def distancia_face_para_camera(face):
            centro = [0, 0, 0]
            for vertex_index in face:
                vertex_local = vertices[vertex_index]
                vertex_world = [
                    vertex_local[0] + position[0] + x,
                    vertex_local[1] + position[1] + y,
                    vertex_local[2] + position[2] + z
                ]
                centro[0] += vertex_world[0]
                centro[1] += vertex_world[1]
                centro[2] += vertex_world[2]
            centro = [centro[0] / 4, centro[1] / 4, centro[2] / 4]  # Centro da face no mundo

            # Calcula a distância de Manhattan
            distancia = abs(centro[0] - camera_pos[0]) + abs(centro[1] - camera_pos[1]) + abs(centro[2] - camera_pos[2])

            return distancia

        # Ordena as faces do mais distante para o mais próximo
        return sorted(range(len(faces)), key=lambda i: distancia_face_para_camera(faces[i]), reverse=True)