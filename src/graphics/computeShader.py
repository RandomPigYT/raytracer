from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr
import util


def compileComputeShader(computeShaderPath):
    
    try: 
        computeCode = util.readFile(computeShaderPath)

    except:
        stderr.write("Error while reading file")
        exit(1)
    
    # compile the shader
    compute = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
    gl.glShaderSource(compute, computeCode)
    gl.glCompileShader(compute)
    

    status = gl.glGetShaderiv(compute, gl.GL_COMPILE_STATUS)
    if not status:
        infolog = gl.glGetShaderInfoLog(compute)
        stderr.write(
            "Error: Compute shader compilation failed.\n" + infolog.decode("utf-8")
        )
        glfwTerminate()
        exit(1)

    # link the shader to the program
    program = gl.glCreateProgram()
    gl.glAttachShader(program, compute)
    gl.glLinkProgram(program)


    status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if not status:
        infolog = gl.glGetProgramInfoLog(program)
        stderr.write(
            "Error: Shader program linking failed.\n" + infolog.decode("utf-8")
        )
        glfwTerminate()
        exit(1)
    
    gl.glDeleteShader(compute)
    return program
