from OpenGL.GL import *
import glm
import glfw

# Constants
FPS = 30
FLAT = 1
GOURAUD = 2

# Global variables
janelaLargura = 500  # window width in pixels
janelaAltura = 500  # window height in pixels
cameraPosition = glm.vec3(20, -10, 20)  # camera position
lightPosition = glm.vec3(5, 5, 5)  # light position
lightSpin = True  # indicates if the light spins around the surface
lightRotation = glm.rotate(glm.mat4(1.0), 0.01, glm.vec3(0, 0, 1))  # rotation matrix for light
lightAmbient = glm.vec3(0.1)  # ambient light property
lightDiffuse = glm.vec3(1.0)  # diffuse light property
lightSpecular = glm.vec3(1.0)  # specular light property
surfaceSize = 20.0  # size of the surface
surfaceDivisions = 10  # number of subdivisions of the surface
surfaceAmbient = glm.vec3(0.1)  # ambient property of the surface material
surfaceDiffuse = glm.vec3(0, 1, 1)  # diffuse property of the surface material
surfaceSpecular = glm.vec3(0.5)  # specular property of the surface material
surfaceShine = 128  # specular property of the surface material
shadingType = FLAT  # shading type


# Initialization function
def inicio():
    glClearColor(0, 0, 0, 1)
    glPointSize(5)
    glLineWidth(1)  # change line width to 1 pixel
    glEnable(GL_DEPTH_TEST)  # enable depth testing


# Function to convert glm.mat4 to list<float>
def mat2list(M):
    return [list(M[i]) for i in range(4)]


# Function to handle window resizing
def alteraJanela(largura, altura):
    global janelaLargura, janelaAltura
    janelaLargura = largura
    janelaAltura = altura
    glViewport(0, 0, largura, altura)  # allocate the entire area of the window for drawing


# Function to handle keyboard input
def teclado(window, key, scancode, action, mods):
    global surfaceDivisions, shadingType, lightSpin
    if action == glfw.PRESS:
        if key == glfw.KEY_D:
            surfaceDivisions -= 1  # decrease surface subdivisions
        elif key == glfw.KEY_UP:
            surfaceDivisions += 1  # increase surface subdivisions
        elif key == glfw.KEY_F:
            shadingType = FLAT  # set shading to FLAT
        elif key == glfw.KEY_G:
            shadingType = GOURAUD  # set shading to GOURAUD
        elif key == glfw.KEY_SPACE:
            lightSpin = not lightSpin  # toggle light spin


# Timer function for updating and redrawing
def timer():
    global lightPosition

    if lightSpin:  # if light spinning is enabled
        lightPosition = glm.vec3(lightRotation * glm.vec4(lightPosition, 1.0))  # apply rotation to light position

    glfw.post_empty_event()  # trigger a redraw
    glfw.set_time(0)  # reset timer for next frame


# Phong shading calculation
def shading(point, normal):
    # Ambient reflection
    shadeAmbient = lightAmbient * surfaceAmbient

    # Diffuse reflection
    l = glm.normalize(lightPosition - point)
    n = glm.normalize(normal)
    shadeDiffuse = lightDiffuse * surfaceDiffuse * glm.max(0.0, glm.dot(l, n))

    # Specular reflection
    v = glm.normalize(cameraPosition - point)
    r = 2 * glm.dot(n, l) * n - l
    shadeSpecular = lightSpecular * surfaceSpecular * glm.max(0, glm.dot(v, r) ** surfaceShine)

    # Phong illumination model
    shade = shadeAmbient + shadeDiffuse + shadeSpecular

    return shade


# Draw flat shaded surface
def drawFlat():
    delta = surfaceSize / surfaceDivisions  # distance between vertices
    glBegin(GL_TRIANGLES)
    for i in range(surfaceDivisions):
        for j in range(surfaceDivisions):
            p1 = glm.vec3(-surfaceSize / 2 + i * delta, -surfaceSize / 2 + j * delta, 0)
            p2 = glm.vec3(-surfaceSize / 2 + (i + 1) * delta, -surfaceSize / 2 + j * delta, 0)
            p3 = glm.vec3(-surfaceSize / 2 + (i + 1) * delta, -surfaceSize / 2 + (j + 1) * delta, 0)
            p4 = glm.vec3(-surfaceSize / 2 + i * delta, -surfaceSize / 2 + (j + 1) * delta, 0)
            normal = glm.vec3(0, 0, 1)  # normal for flat shading

            # Draw triangles
            for triangle in [(p1, p2, p3), (p1, p3, p4)]:
                pc = (1.0 / 3.0) * (triangle[0] + triangle[1] + triangle[2])
                cor = shading(pc, normal)
                glColor3f(cor.r, cor.g, cor.b)
                for vertex in triangle:
                    glVertex3f(vertex.x, vertex.y, vertex.z)
    glEnd()


# Draw Gouraud shaded surface
def drawGouraud():
    delta = surfaceSize / surfaceDivisions  # distance between vertices
    glBegin(GL_TRIANGLES)
    for i in range(surfaceDivisions):
        for j in range(surfaceDivisions):
            p1 = glm.vec3(-surfaceSize / 2 + i * delta, -surfaceSize / 2 + j * delta, 0)
            p2 = glm.vec3(-surfaceSize / 2 + (i + 1) * delta, -surfaceSize / 2 + j * delta, 0)
            p3 = glm.vec3(-surfaceSize / 2 + (i + 1) * delta, -surfaceSize / 2 + (j + 1) * delta, 0)
            p4 = glm.vec3(-surfaceSize / 2 + i * delta, -surfaceSize / 2 + (j + 1) * delta, 0)
            normal = glm.vec3(0, 0, 1)  # normal for Gouraud shading

            # Calculate shading for each vertex
            cor1 = shading(p1, normal)
            cor2 = shading(p2, normal)
            cor3 = shading(p3, normal)
            cor4 = shading(p4, normal)

            # Draw triangles with vertex colors
            for triangle in [(p1, p2, p3), (p1, p3, p4)]:
                glColor3f(cor1.r, cor1.g, cor1.b)
                glVertex3f(p1.x, p1.y, p1.z)
                glColor3f(cor2.r, cor2.g, cor2.b)
                glVertex3f(p2.x, p2.y, p2.z)
                glColor3f(cor3.r, cor3.g, cor3.b)
                glVertex3f(p3.x, p3.y, p3.z)

                glColor3f(cor1.r, cor1.g, cor1.b)
                glVertex3f(p1.x, p1.y, p1.z)
                glColor3f(cor3.r, cor3.g, cor3.b)
                glVertex3f(p3.x, p3.y, p3.z)
                glColor3f(cor4.r, cor4.g, cor4.b)
                glVertex3f(p4.x, p4.y, p4.z)
    glEnd()


# Function used to redraw the content of the frame buffer
def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear frame buffer and depth buffer

    # Set projection
    glMatrixMode(GL_PROJECTION)
    aspectRatio = janelaLargura / janelaAltura
    matrizProjecao = glm.perspective(glm.radians(45.0), aspectRatio, 0.1, 100.0)
    glLoadMatrixf(mat2list(matrizProjecao))

    # Set modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glm.lookAt(cameraPosition, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    # Draw surface based on shading type
    if shadingType == FLAT:
        drawFlat()
    else:
        drawGouraud()

    glfw.swap_buffers(window)  # swap the front and back buffers


# Main function to initialize GLFW and run the application
if __name__ == "__main__":
    if not glfw.init():
        raise Exception("GLFW can't be initialized!")

    window = glfw.create_window(janelaLargura, janelaAltura, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created!")

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, alteraJanela)  # set window size callback
    glfw.set_key_callback(window, teclado)  # set key callback

    inicio()

    # Main loop
    while not glfw.window_should_close(window):
        timer()
        desenha()  # Draw the content
        glfw.poll_events()  # process events

    glfw.terminate()  # clean up and close the window
