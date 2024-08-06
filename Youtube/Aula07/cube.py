from OpenGL.GL import *

class Cube:
    def __init__(self):
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        self.build()
        glEndList()

    def build(self):
        vertices = [
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
        ]
        faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5],
        ]
        colors = [
            [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [0.5, 0.5, 0.5], [1, 0.5, 0]
        ]

        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glColor3fv(colors[vertex])
                glVertex3fv(vertices[vertex])
        glEnd()

    def draw(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        glCallList(self.display_list)
        glPopMatrix()
