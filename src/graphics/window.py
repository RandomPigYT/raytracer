from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr


def framebufferSizeCallback(window, width, height):
    gl.glViewport(0, 0, width, height)


def createWindow(width, height, title):
    window = glfwCreateWindow(width, height, title, None, None)

    if not window:
        stderr.write("Failed to create GLFW window\n")
        glfwTerminate()
        retrun - 1

    glfwMakeContextCurrent(window)
    gl.glViewport(0, 0, width, height)

    glfwSetFramebufferSizeCallback(window, framebufferSizeCallback)

    return window
