import glfw
from OpenGL.GL import *


# E uma boa pratica criar uma funçio para agrupar as configurações iniciais do OpenGL
def inicio():
   glPointSize(5)        # altera o tamanho dos pontos (por padrio, o tamanho é igual a 1 pixel)
   glLineWidth(3)        # altera a largura dos segmentos de reta (por padrio, a largura é de 1 pixel)

# Funçao que desenha varias primitivas diferentes para exemplificar seu uso
def primitivas():
    glBegin(GL_POINTS) # pontos
    glVertex2f( 1, 1)
    glVertex2f( 4, 1)
    glVertex2f( 4, 4)
    glVertex2f( 1, 4)
    glEnd()
    
    glBegin(GL_LINES) # segmentos de reta (a cada dois pontos, conecte-os em segmentos de reta)
    glVertex2f( 5, 1)
    glVertex2f( 8, 1)
    glVertex2f( 8, 4)
    glVertex2f( 5, 4)
    glEnd()
    
    glBegin(GL_LINE_STRIP) # polilinha aberta (conecta uma sequência de pontos em segmentos de reta)
    glVertex2f( 9, 1)
    glVertex2f(12, 1)
    glVertex2f(12, 4)
    glVertex2f( 9, 4)
    glEnd()
    
    glBegin(GL_LINE_LOOP) # polilinha fechada (conecta uma sequência de pontos em segmentos de reta e o ultimo ponto com o primeiro)
    glVertex2f(13, 1)
    glVertex2f(16, 1)
    glVertex2f(16, 4)
    glVertex2f(13, 4)
    glEnd()
    
    glBegin(GL_QUADS) # quadrilateros (a cada quatro pontos, conecte-os em um quadrilatero)
    glVertex2f( 1, 5)
    glVertex2f( 4, 5)
    glVertex2f( 4, 8)
    glVertex2f( 1, 8)
    glEnd()
    
    glBegin(GL_TRIANGLES) # triangulos (a cada três pontos, conecte-os em triangulos)
    glVertex2f( 5, 5)
    glVertex2f( 8, 5)
    glVertex2f( 5, 8)
    glVertex2f( 5, 8)
    glVertex2f( 8, 5)
    glVertex2f( 8, 8)
    glEnd()
    
    glBegin(GL_TRIANGLE_STRIP) # faixa de triangulos (acada novo ponto é conectado aos dois ultimos formando triangulos)
    glVertex2f( 9, 5)
    glVertex2f( 9, 8)
    glVertex2f(10, 5)
    glVertex2f(10, 8)
    glVertex2f(11, 5)
    glVertex2f(11, 8)
    glVertex2f(12, 5)
    glVertex2f(12, 8)
    glEnd()
    
    glBegin(GL_QUAD_STRIP); # cada dois novos pontos sio conectados aos dois ultimos formando quadrilateros
    glVertex2f(13, 5)
    glVertex2f(13, 8)
    glVertex2f(14, 5)
    glVertex2f(14, 8)
    glVertex2f(15, 5)
    glVertex2f(15, 8)
    glVertex2f(16, 5)
    glVertex2f(16, 8)
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN) # o primeiro ponto é conectado a todos os demais formando triangulos
    glVertex2f(2.5,10.5)
    glVertex2f(  1,  9)
    glVertex2f(  4,  9)
    glVertex2f(  4, 12)
    glVertex2f(  1, 12)
    glVertex2f(  1,  9)
    glEnd()
    
    glBegin(GL_POLYGON) # poli­gono de varios lados (deve ser evitado, pois o poli­gono pode ser incorreto caso seja concavo)
    glVertex2f( 5,10)
    glVertex2f( 6, 9)
    glVertex2f( 7, 9)
    glVertex2f( 8,10)
    glVertex2f( 8,11)
    glVertex2f( 7,12)
    glVertex2f( 6,12)
    glVertex2f( 5,11)
    glEnd()
    
    glBegin(GL_QUADS); # quadrilateros e poli­gonos com a ordem dos vértices incorreta pode levar a esse tipo de erro
    glVertex2f( 9, 9)
    glVertex2f(12, 9)
    glVertex2f( 9,12)
    glVertex2f(12,12)
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN) # GL_POLYGON pode ser substitui­do por GL_TRIANGLE_FAN
    glVertex2f(13,10)
    glVertex2f(14, 9)
    glVertex2f(15, 9)
    glVertex2f(16,10)
    glVertex2f(16,11)
    glVertex2f(15,12)
    glVertex2f(14,12)
    glVertex2f(13,11)
    glEnd()

# Funçao que sera chamada cada vez que o conteudo da janela precisar ser redesenhado
def desenha():
    glClear(GL_COLOR_BUFFER_BIT) # Limpa o conteudo do frame buffer aplicando a cor usada em glClearColor em toda a imagem

    # por padrio, o OpenGL exibe apenas as coisas desenhadas dentro do intervalo -1 e 1 nas coordenadas x e y
    # os comandos abaixo alteram esse comportamento padrio de visualizaçio (sera explicado em mais detalhes futuramente)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,17,0,17,-1,1)    # altera a area de visualizaçio (tudo entre 0 e 17 nas coordenadas x e y sera visualizado)
    
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL ); # alterando para modo de preenchimento (por padrio ja vem ativado)
    glColor3f(1.0, 0.0, 0.0);                    # cor de preenchimento é definida como vermelha  
    primitivas();                                # chamando a funçao que desenha aquele conjunto de primitivas

    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE ); # alterando para modo de linhas (usado para mostrar as arestas dos poli­gonos)
    glColor3f(0.0, 0.0, 0.0);                    # cor das linhas é definida como preta
    primitivas();                                # chamando a funçao das primitivas novamente (boa pratica pra evitar reescrever codigo)


    glFlush() # Mostrar a desenho feito no framebuffer na janela


def main():
    glfw.init()

    window = glfw.create_window(500, 500, "Primitivas", None, None)
    glfw.make_context_current(window)

    glViewport(0, 0, 500, 500)

    while not glfw.window_should_close(window):
        # processamento dos eventos
        glfw.poll_events()

        # renderizações como PyOpenGL
        glClearColor(1,1,1,1) # funçao que define a cor de fundo usada pelo OpenGL para limpar a tela
        glClear(GL_COLOR_BUFFER_BIT)

        inicio()

        desenha()

        # invertendo os buffers (backbuffer e frontbuffer)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()