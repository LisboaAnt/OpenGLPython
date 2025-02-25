from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class Parede:
    def __init__(self, initial_position=[0.0, 10.0, 0.0], direction=[1.0, 0.0, 0.0], texture_file="grass.jpg", width=100.0, height=100.0):
        self.position = initial_position
        self.direction = np.array(direction)  # Vetor de direção
        self.texture_id = None
        self.reflection_texture = None  # A textura do reflexo será armazenada aqui
        self.width = width  # Largura da parede
        self.height = height  # Altura da parede

        # Criar o framebuffer e a textura de reflexão
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        # Criar textura onde o reflexo será armazenado
        self.reflection_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.reflection_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 800, 600, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Criar renderbuffer para profundidade
        rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, 800, 600)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbo)

        # Associar a textura ao framebuffer
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.reflection_texture, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Erro ao criar framebuffer!")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def draw(self):
        """Desenha uma parede (plano) com textura e rotação."""

        glDisable(GL_LIGHTING)

        # Atualizando os vértices da parede com base no tamanho (width e height)
        vertices = [
            [-self.width / 2, -self.height / 2, 0.0],  # Vértice inferior esquerdo
            [self.width / 2, -self.height / 2, 0.0],  # Vértice inferior direito
            [self.width / 2, self.height / 2, 0.0],  # Vértice superior direito
            [-self.width / 2, self.height / 2, 0.0],  # Vértice superior esquerdo
        ]

        uvs = [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0],
        ]

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-90, 0.0, 1.0, 0.0)


        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)


        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord2fv(uvs[i])
            glVertex3fv(vertices[i])
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glEnable(GL_LIGHTING)

    def set_texture(self, texture_id):
        """Define a textura da parede."""
        self.texture_id = texture_id

    def set_position(self, position):
        """Define a posição da parede."""
        self.position = position

    def set_direction(self, direction):
        """Define a direção da parede (vetor)."""
        self.direction = np.array(direction)


    def render_reflection(self, lista_de_exebicao, cuboAranha, camera_position):
        """Renderiza a reflexão no framebuffer com o efeito de espelho."""

        # Salvar o estado atual da matriz de projeção
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()  # Salvar a matriz de projeção atual
        glLoadIdentity()

        # Configurar a matriz de visualização
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()  # Salvar a matriz de visualização atual
        glLoadIdentity()

        # Configurar o framebuffer de reflexão
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Calcular a posição refletida da câmera
        distance_to_mirror = np.dot(camera_position - self.position, self.direction)
        if distance_to_mirror < 1.0:  # Distância mínima permitida da câmera ao espelho
            camera_position = self.position + self.direction * 1.0
        reflection_position = camera_position - 2 * np.dot(camera_position - self.position, self.direction) * self.direction

        # Definir a visão para o reflexo
        look_at_position = np.array(self.position) + self.direction
        gluLookAt(reflection_position[0], reflection_position[1], reflection_position[2],
                  camera_position[0] + 10, camera_position[1], camera_position[2],
                  0, 1, 0)

        # Definir o plano de recorte (coincide com o plano do espelho)
        clip_plane = np.array([self.direction[0], self.direction[1], self.direction[2],
                               -np.dot(self.direction, self.position)])
        glClipPlane(GL_CLIP_PLANE0, clip_plane)
        glEnable(GL_CLIP_PLANE0)

        # Renderizar a cena refletida
        glCallList(lista_de_exebicao)
        cuboAranha.draw()

        # Desabilitar o plano de recorte após a renderização
        glDisable(GL_CLIP_PLANE0)

        # Restaurar o framebuffer padrão
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Restaurar a matriz de visualização
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()  # Restaurar a matriz de visualização anterior

        # Restaurar a matriz de projeção
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()  # Restaurar a matriz de projeção anterior
        glMatrixMode(GL_MODELVIEW)  # Voltar para a matriz de visualização