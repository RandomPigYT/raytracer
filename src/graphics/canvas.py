from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr
import numpy as np
import util
import graphics.shader as shader
import ctypes

# vertex -> x, y, z, u, v
vertices = [

    -1, 1, 0, 0, 1,   # top-left
    1, 1, 0, 1, 1,   # top-right
    1, -1, 0, 1, 0,  # bottom-right
    -1, -1, 0, 0, 0  # bottom-left

    ]

indices = [

    0, 1, 3,    # upper triangle
    1, 2, 3     # lower triangle

    ]


def initRenderCavas():
    
    floatSize = 4
    int32Size = 4

    vao = gl.glGenVertexArrays(1)
    vbo = gl.glGenBuffers(1)
    ebo = gl.glGenBuffers(1)

    gl.glBindVertexArray(vao)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertices) * floatSize, np.array(vertices, dtype="float32"), gl.GL_STATIC_DRAW)

    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(indices) * int32Size, np.array(indices, dtype="uint32"), gl.GL_STATIC_DRAW)
    
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * floatSize, None)
    gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 5 * floatSize, 3 * floatSize)
    gl.glEnableVertexAttribArray(0)
    gl.glEnableVertexAttribArray(1)


    shaderProgram = shader.generateShaderProgram(
        "./src/shader_code/vertex.vert", 
        "./src/shader_code/fragment.frag"
    )
    
    shader.useShader(shaderProgram)
    
    
    gl.glBindVertexArray(vao)
