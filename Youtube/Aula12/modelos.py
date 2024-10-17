from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import pywavefront
import pywavefront.visualization

class Model:
    def __init__(self, obj_path):
        self.scene = pywavefront.Wavefront(obj_path, collect_faces=True)

    def draw(self):
        glPushMatrix()
        glTranslatef(0,2,0)
        pywavefront.visualization.draw(self.scene)
        glPopMatrix()