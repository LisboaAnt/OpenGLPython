import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Colisao:
    def __init__(self):
        self.objetos_colisao = {}  # Dicionário para armazenar os objetos e suas posições
        self.mostra_colisao = False
        self.colisao = True

    def adicionar_objeto(self, obj_id, posicao, tamanho):
        """ Adiciona um objeto ao dicionário de colisão, centralizando a posição """
        centro = np.array(posicao) - np.array(tamanho) / 2
        self.objetos_colisao[obj_id] = {"posicao": centro, "tamanho": tamanho}

    def atualizar_posicao(self, obj_id, nova_posicao):
        """ Atualiza a posição de um objeto no dicionário """
        if obj_id in self.objetos_colisao:
            tamanho = self.objetos_colisao[obj_id]["tamanho"]
            centro = np.array(nova_posicao) - np.array(tamanho) / 2
            self.objetos_colisao[obj_id]["posicao"] = centro

    def pode_mover(self, obj_id, nova_posicao):
        """ Verifica se o objeto pode se mover sem colidir com outro """
        if obj_id not in self.objetos_colisao:
            return False

        tamanho_atual = self.objetos_colisao[obj_id]["tamanho"]
        centro_novo = np.array(nova_posicao) - np.array(tamanho_atual) / 2

        for outro_id, info in self.objetos_colisao.items():
            if outro_id == obj_id:
                continue
            if self._colisao_3d(centro_novo, tamanho_atual, info["posicao"], info["tamanho"]):
                return False

        return True

    def _colisao_3d(self, pos1, tam1, pos2, tam2):
        """ Verifica colisão entre dois objetos 3D """
        return (pos1[0] < pos2[0] + tam2[0] and pos1[0] + tam1[0] > pos2[0] and
                pos1[1] < pos2[1] + tam2[1] and pos1[1] + tam1[1] > pos2[1] and
                pos1[2] < pos2[2] + tam2[2] and pos1[2] + tam1[2] > pos2[2])

    def desenhar_linha_espessa(self, p1, p2, largura):
        """Desenha uma linha espessa entre p1 e p2 com largura constante."""
        p1 = np.array(p1)
        p2 = np.array(p2)
        direcao = p2 - p1
        perpendicular = np.array([-direcao[1], direcao[0], 0])
        if np.linalg.norm(perpendicular) == 0:
            perpendicular = np.array([1, 0, 0])
        perpendicular = perpendicular / np.linalg.norm(perpendicular) * largura / 2

        v1 = p1 + perpendicular
        v2 = p1 - perpendicular
        v3 = p2 + perpendicular
        v4 = p2 - perpendicular

        glDisable(GL_LIGHTING)

        glBegin(GL_QUADS)
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v4)
        glVertex3fv(v3)
        glEnd()

        glEnable(GL_LIGHTING)

    def desenhar_colisao(self):
        """ Desenha as caixas de colisão """
        for info in self.objetos_colisao.values():
            pos = info["posicao"]
            tam = info["tamanho"]
            x, y, z = pos
            w, h, d = tam

            # Define os 8 vértices centralizados
            vertices = [
                (x, y, z), (x + w, y, z),
                (x, y + h, z), (x + w, y + h, z),
                (x, y, z + d), (x + w, y, z + d),
                (x, y + h, z + d), (x + w, y + h, z + d)
            ]

            arestas = [
                (0, 1), (1, 3), (3, 2), (2, 0),
                (4, 5), (5, 7), (7, 6), (6, 4),
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]

            glColor3f(1, 0, 0)
            largura_linha = 0.1

            for edge in arestas:
                self.desenhar_linha_espessa(vertices[edge[0]], vertices[edge[1]], largura_linha)
        glColor3f(1, 1, 1)  # Resetar a cor