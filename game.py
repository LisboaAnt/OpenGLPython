










from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math

width, height = 800, 600 # Largura e altura da janela de exibição


def draw_floor(size=1000, divisions=20):
    """
    Desenha um chão (plano) na origem no eixo XZ.
    
    :param size: Tamanho total do chão (largura e comprimento).
    :param divisions: Número de divisões da grade no chão.
    """
    half_size = size / 2.0
    step = size / divisions
    
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)  # Cor do chão (cinza)
    
    # Desenha um grande quadrado como o chão
    glVertex3f(-half_size, 0, -half_size)
    glVertex3f(half_size, 0, -half_size)
    glVertex3f(half_size, 0, half_size)
    glVertex3f(-half_size, 0, half_size)
    
    glEnd()
    
    # Opcional: desenha uma grade no chão para visualização
    glColor3f(1, 1, 1)  # Cor da grade (um cinza mais claro)
    glBegin(GL_LINES)
    
    # Linhas paralelas ao eixo X
    for i in range(divisions + 1):
        glVertex3f(-half_size + i * step, 0, -half_size)
        glVertex3f(-half_size + i * step, 0, half_size)
    
    # Linhas paralelas ao eixo Z
    for i in range(divisions + 1):
        glVertex3f(-half_size, 0, -half_size + i * step)
        glVertex3f(half_size, 0, -half_size + i * step)
    
    glEnd()
    



class OBJLoader:
    def __init__(self, filename):
        self.moto_position = [width / 2, height / 2]; 
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.load_obj(filename)

    def load_obj(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # linha de vértice
                    self._parse_vertex(line)
                elif line.startswith('vt '):  # linha de coordenada de textura
                    self._parse_texcoord(line)
                elif line.startswith('vn '):  # linha de normal
                    self._parse_normal(line)
                elif line.startswith('f '):  # linha de face
                    self._parse_face(line)

    def _parse_vertex(self, line):
        parts = line.split()
        vertex = (float(parts[1]), float(parts[2]), float(parts[3]))
        self.vertices.append(vertex)

    def _parse_texcoord(self, line):
        parts = line.split()
        texcoord = (float(parts[1]), float(parts[2]))
        self.texcoords.append(texcoord)

    def _parse_normal(self, line):
        parts = line.split()
        normal = (float(parts[1]), float(parts[2]), float(parts[3]))
        self.normals.append(normal)

    def _parse_face(self, line):
        parts = line.split()
        face = []
        for part in parts[1:]:
            indices = part.split('/')
            vertex_idx = int(indices[0]) - 1  # Índice do vértice
            texcoord_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None  # Índice da coordenada de textura
            normal_idx = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None  # Índice da normal
            face.append((vertex_idx, texcoord_idx, normal_idx))
        self.faces.append(face)

    def get_data(self):
        return self.vertices, self.texcoords, self.normals, self.faces


zoom_factor = 30.0  # Distância inicial da câmera
fov = 90.0      # Campo de visão inicial

def init_gl(vertices, faces):
    glEnable(GL_DEPTH_TEST)

    # Convertendo a lista de vértices para um numpy array
    vertices_array = np.array(vertices, dtype='float32')

    # Gerar um buffer de vértices
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices_array.nbytes, vertices_array, GL_STATIC_DRAW)

    # Preparar os dados das faces
    indices = []
    for face in faces:
        for vertex_idx, texcoord_idx, normal_idx in face:
            indices.append(vertex_idx)
    indices_array = np.array(indices, dtype='uint32')

    # Gerar um buffer de índices (para as faces)
    ibo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_array.nbytes, indices_array, GL_STATIC_DRAW)

    return vbo, ibo



speed = 10.0 # Velocidade da moto
camera_distance = -200# Distância da câmera em relação à moto
moto_position = [60.0, 60.0, 60.0]  # Posição inicial da moto
rotate_angle = 0.0  # Ângulo de rotação da moto

def display():
    global moto_position, rotate_angle, camera_distance
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Atualizar a posição da câmera para acompanhar a moto
    gluPerspective(90, width / height, 0.1, 1000)
    
    camera_x = moto_position[0] + camera_distance * math.sin(math.radians(rotate_angle))  # Ajusta conforme a rotação
    camera_z = moto_position[2] + camera_distance * math.cos(math.radians(rotate_angle)) # Ajusta conforme a rotação e o zoom
    
    # Atualiza a função gluLookAt para seguir a moto
    gluLookAt(
        camera_x , 150, camera_z,  # Posição da câmera
        moto_position[0], moto_position[1], moto_position[2],  # Olhar para a moto
        0, 1, 0  # O eixo 'y' é o "cima" global
    )
    
    draw_floor()

    # Mover a moto antes de desenhar
    glPushMatrix()
    glTranslatef(moto_position[0], moto_position[1], moto_position[2])
    glRotatef(rotate_angle, 0.0, 1.0, 0.0)  # Aplica a rotação ao longo do eixo Y
    
    # Desenhar a moto
    glEnableClientState(GL_VERTEX_ARRAY)
    glRotatef(90, 0.0, 1.0, 0.0) 
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
    glColor3f(1, 0, 0)
    glDrawElements(GL_TRIANGLES, len(faces) * 3, GL_UNSIGNED_INT, None)
    glColor3f(1, 1, 1)
     
      
    glDisableClientState(GL_VERTEX_ARRAY)
    
    glPopMatrix()

    glutSwapBuffers()

def timer(value):
    global moto_position

    # Adicione movimento à moto (exemplo: mover ao longo do eixo X)
    # moto_position[0] -= 20  # Incremento no eixo X

    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)





def reshape(w, h):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    
    
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global zoom_factor, fov, moto_position, rotate_angle
    
    # if key == b'-':
    #     zoom_factor += 20.0
    # elif key == b'=':
    #     zoom_factor -= 20.0
    # elif key == b'[':
    #     fov += 50.0
    #     print(fov)
    # elif key == b']':
    #     fov -= 50.0
    if key == b'w':
        moto_position[2] +=  math.cos(math.radians(rotate_angle)) * speed
        moto_position[0] +=  math.sin(math.radians(rotate_angle)) * speed
    elif key == b's':
        moto_position[2] -=  math.cos(math.radians(rotate_angle)) * speed
        moto_position[0] -=  math.sin(math.radians(rotate_angle)) * speed
    elif key == b'a':
        rotate_angle += 5.0
        
    elif key == b'd':
        rotate_angle -= 5.0
        
        
    rotate_angle = rotate_angle % 360
    
    glutPostRedisplay()

def main():
    global vbo, ibo, faces

    # Carregar o modelo .obj
    obj_loader = OBJLoader('akira_moto.obj')
    vertices, texcoords, normals, faces = obj_loader.get_data()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("Render .obj com PyOpenGL - Zoom")

    # Inicializar OpenGL com os dados carregados
    vbo, ibo = init_gl(vertices, faces)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)
    

    glutMainLoop()


if __name__ == "__main__":
    main()
