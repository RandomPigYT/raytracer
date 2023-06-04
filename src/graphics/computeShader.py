from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr


def compileComputeShader(computeShaderPath):

    computeShaderFile = read(computeShaderPath, "r")

    computeShaderCode = computeShaderFile.read()

    computeShaderFile.close()



    pass
