from glfw.GLFW import *
import OpenGL.GL as gl
import c_extension as cext
import sys
import traceback


def cleanup(t, value, tb):
    glfwTerminate()
    print(*traceback.format_exception(t, value, tb), sep="\n")


def init(contextMajor, contextMinor):
    glfwInit()

    sys.excepthook = cleanup

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    cext.init()
