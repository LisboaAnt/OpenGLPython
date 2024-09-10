import pywavefront
import pywavefront.visualization
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Carregar o arquivo .obj
scene1 = pywavefront.Wavefront('load_obj/LightCyclePlayer.obj', collect_faces=True)
scene2 = pywavefront.Wavefront('load_obj/LightCycleIA.obj', collect_faces=True)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 800, 600)
    
    # Configuração de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)  # Projeção perspectiva
    
    # Posicionar a câmera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10.0, 5.0, 10.0,  # posição da câmera (ajustada para melhor visualização)
              0, 0, 0,   # ponto onde a câmera está olhando
              0, 1, 0)   # eixo 'up'

    # Renderizar o objeto
    glScalef(1, 1, 1)  # Ajustar escala, se necessário
    pywavefront.visualization.draw(scene1)
    
    glTranslatef(5, 0, 0)  # Ajustar posição
    pywavefront.visualization.draw(scene2)

    glutSwapBuffers()

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Configurar a luz
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])  # Posição da luz
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])   # Luz difusa
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])  # Luz especular

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Renderizando OBJ com Materiais")
    glutDisplayFunc(render)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
