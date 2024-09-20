class Iluminacao:
    def __init__(self):
        # Configura a iluminação
        glEnable(GL_LIGHTING)  # Ativa o modelo de iluminação
        glEnable(GL_LIGHT0)  # Ativa a luz 0

        # Define as propriedades da luz
        luz_ambiente = [0.2, 0.2, 0.2, 1.0]  # Luz ambiente
        luz_difusa = [1.0, 1.0, 1.0, 1.0]  # Luz difusa
        luz_especular = [1.0, 1.0, 1.0, 1.0]  # Luz especular
        posicao_luz = [0.0, 0.0, 0.0, 1.0]  # Posição da luz

        # Aplica as propriedades da luz
        glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
        glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)

    def desenhar(self):
        # Desenha um círculo amarelo na posição (0, 0, 0)
        glPushMatrix()
        glColor3f(1.0, 1.0, 0.0)  # Amarelo
        glTranslatef(0.0, 0.0, 0.0)  # Translada para a posição (0, 0, 0)

        # Desenha o círculo
        num_segments = 100  # Número de segmentos do círculo
        radius = 1.0  # Raio do círculo
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)  # Centro do círculo
        for i in range(num_segments + 1):
            angle = 2 * math.pi * i / num_segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0.0)  # Ponto na borda do círculo
        glEnd()

        glPopMatrix()
