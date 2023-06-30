from glfw.GLFW import *
import OpenGL.GL as gl
import c_extension as cext
import sys


def cleanup():
    glfwTerminate()


def init(contextMajor, contextMinor):
    glfwInit()

    sys.excepthook = cleanup

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    cext.init()
