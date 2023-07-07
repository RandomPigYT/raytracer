from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr
import sceneManager as sm


def framebufferSizeCallback(window, width, height):
    gl.glViewport(0, 0, width, height)

    gl.glUseProgram(sm.currentScene.compute)
    resolutionLoc = gl.glGetUniformLocation(sm.currentScene.compute, "resolution")
    gl.glUniform2f(resolutionLoc, width, height)



def createWindow(width, height, title, monitor=None):
    window = glfwCreateWindow(width, height, title, monitor, None)

    if not window:
        stderr.write("Failed to create GLFW window\n")
        glfwTerminate()
        return -1

    glfwMakeContextCurrent(window)
    gl.glViewport(0, 0, width, height)

    glfwSetFramebufferSizeCallback(window, framebufferSizeCallback)

    return window
