from OpenGL.GL import *

class Cube:
    def __init__(self, x_centro, y_centro, z_centro, lado, r, g, b, intensidade):
        self.x_centro = x_centro
        self.y_centro = y_centro
        self.z_centro = z_centro
        self.lado = lado
        self.r = r
        self.g = g
        self.b = b
        self.intensidade = intensidade

    def draw(self):
        # Habilita a iluminação e define as propriedades do material
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Configura a posição da fonte de luz
        light_position = [self.x_centro, self.y_centro, self.z_centro, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        # Configura a luz ambiente difusa em todas as direções com a cor especificada e intensidade
        glLightfv(GL_LIGHT0, GL_AMBIENT, [self.r * self.intensidade, self.g * self.intensidade, self.b * self.intensidade, 1.0])

        # Configura os coeficientes de atenuação para limitar o alcance da luz
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)

        # Desenha o cubo
        vertices = [
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ]

        faces = [
            [0, 1, 2, 3],  # Face frontal
            [1, 5, 6, 2],  # Face direita
            [5, 4, 7, 6],  # Face traseira
            [4, 0, 3, 7],  # Face esquerda
            [3, 2, 6, 7],  # Face superior
            [4, 5, 1, 0]   # Face inferior
        ]

        for face in faces:
            glBegin(GL_QUADS)
            for vertice_index in face:
                glVertex3f(
                    self.x_centro + vertices[vertice_index][0] * self.lado / 2,
                    self.y_centro + vertices[vertice_index][1] * self.lado / 2,
                    self.z_centro + vertices[vertice_index][2] * self.lado / 2
                )
            glEnd()
