from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image


class Cilindro:
    def __init__(self, inital_position=[0.0, 0.0, 0.0], altura=1.0, raio=0.5,
                 texture_atlas=None, texture_indices=[0, 1, 2], lighting=True,
                 cores_faces=None, rotation=None, slices=32, stacks=32):
        self.texture_atlas = texture_atlas
        self.texture_indices = texture_indices  # [base_inferior, lateral, base_superior]
        self.altura = altura
        self.raio = raio
        self.position = inital_position
        self.texture_id = None
        self.lighting = lighting
        self.cores_faces = cores_faces if cores_faces else [[1.0, 1.0, 1.0, 1.0] for _ in range(3)]
        self.rotation = rotation
        self.slices = slices  # número de divisões ao redor do cilindro
        self.stacks = stacks  # número de divisões ao longo da altura
        self.quadric = gluNewQuadric()

        # Configura o quadric para gerar coordenadas de textura
        if self.texture_atlas:
            gluQuadricTexture(self.quadric, GL_TRUE)

        gluQuadricNormals(self.quadric, GLU_SMOOTH)

    def draw(self, x, y, z, camera_pos=None):
        if not self.lighting:
            glDisable(GL_LIGHTING)

        glPushMatrix()
        glTranslatef(self.position[0] + x, self.position[1] + y, self.position[2] + z)

        if self.rotation is not None:
            glRotatef(self.rotation[0], 1, 0, 0)
            glRotatef(self.rotation[1], 0, 1, 0)
            glRotatef(self.rotation[2], 0, 0, 1)

        # Desenha o cilindro em três partes: base inferior, lateral e base superior
        for i in range(3):
            if self.texture_atlas:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture_atlas.texture_id)
                if i < len(self.texture_indices):
                    uvs = self.texture_atlas.get_uv_coords(self.texture_indices[i])
            else:
                cor = self.cores_faces[i]
                glMaterialfv(GL_FRONT, GL_DIFFUSE, cor)
                glMaterialfv(GL_FRONT, GL_SPECULAR, cor)
                glMaterialfv(GL_FRONT, GL_AMBIENT, cor)
                glMaterialfv(GL_FRONT, GL_SHININESS, 10)

            """
            if i == 0:  # Base inferior
                glPushMatrix()
                glTranslatef(0, -self.altura / 2, 0)
                glRotatef(180, 1, 0, 0)
                gluDisk(self.quadric, 0, self.raio, self.slices, 1)
                glPopMatrix()
            """
            if i == 1:  # Lateral
                glPushMatrix()
                glTranslatef(0, -self.altura / 2, 0)
                gluCylinder(self.quadric, self.raio, self.raio, self.altura, self.slices, self.stacks)
                glPopMatrix()
            """
            else:  # Base superior
                glPushMatrix()
                glTranslatef(0, -self.altura / 2, self.altura)
                gluDisk(self.quadric, 0, self.raio, self.slices, 1)
                glPopMatrix()
            """

            if self.texture_atlas:
                glDisable(GL_TEXTURE_2D)

        glPopMatrix()

        if not self.lighting:
            glEnable(GL_LIGHTING)