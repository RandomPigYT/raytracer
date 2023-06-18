from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr
import util


def useShader(ID):
    gl.glUseProgram(ID)


def generateShaderProgram(vertexPath, fragmentPath):
    try:
        vertexCode = util.readFile(vertexPath)
        fragmentCode = util.readFile(fragmentPath)

    except:
        stderr.write("Error: Shader file not successfully read\n")

    # Compile shaders
    vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertex, vertexCode)
    gl.glCompileShader(vertex)

    status = gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS)
    if not status:
        infolog = gl.glGetShaderInfoLog(vertex)
        stderr.write(
            "Error: Vertex shader compilation failed.\n" + infolog.decode("utf-8")
        )
        glfwTerminate()
        exit(1)

    fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragment, fragmentCode)
    gl.glCompileShader(fragment)

    status = gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS)
    if not status:
        infolog = gl.glGetShaderInfoLog(fragment)
        stderr.write(
            "Error: Fragment shader compilation failed.\n" + infolog.decode("utf-8")
        )
        glfwTerminate()
        exit(1)

    # shader program
    ID = gl.glCreateProgram()
    gl.glAttachShader(ID, vertex)
    gl.glAttachShader(ID, fragment)
    gl.glLinkProgram(ID)

    # status = None
    # gl.glGetProgramiv(id, gl.GL_LINK_STATUS, status)
    # if not status:
    #     infolog = None
    #     gl.glGetProgramInfoLog(ID, 512, None, infolog)

    #     stderr.write("Error: Shader program linking failed.\n" + infolog)

    gl.glDeleteShader(vertex)
    gl.glDeleteShader(fragment)

    return ID
