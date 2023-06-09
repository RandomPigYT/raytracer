from glfw.GLFW import *
import OpenGL.GL as gl
from sys import stderr
import numpy as np
import util
import graphics.shader as shader
import ctypes
from PIL import Image
import random as rand
import graphics.computeShader as comp

# fmt: off
# vertex -> x, y, z, u, v
vertices = [
    -1, 1, 0, 0, 1,  # top-left
    1, 1, 0, 1, 1,  # top-right
    1, -1, 0, 1, 0,  # bottom-right
    -1, -1, 0, 0, 0,  # bottom-left
]

indices = [0, 1, 3, 
           1, 2, 3]  # upper triangle  # lower triangle
# fmt: on


def initRenderCavas(self):
    floatSize = 4
    int32Size = 4

    # setup buffers
    self.vao = gl.glGenVertexArrays(1)
    self.vbo = gl.glGenBuffers(1)
    self.ebo = gl.glGenBuffers(1)

    gl.glBindVertexArray(self.vao)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
    gl.glBufferData(
        gl.GL_ARRAY_BUFFER,
        len(vertices) * floatSize,
        np.array(vertices, dtype="float32"),
        gl.GL_STATIC_DRAW,
    )

    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
    gl.glBufferData(
        gl.GL_ELEMENT_ARRAY_BUFFER,
        len(indices) * int32Size,
        np.array(indices, dtype="uint32"),
        gl.GL_STATIC_DRAW,
    )

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * floatSize, None)
    gl.glVertexAttribPointer(
        1, 2, gl.GL_FLOAT, gl.GL_FALSE, 5 * floatSize, ctypes.c_void_p(3 * floatSize)
    )
    gl.glEnableVertexAttribArray(0)
    gl.glEnableVertexAttribArray(1)

    gl.glBindVertexArray(self.vao)

    # Shader for quad
    self.shaderProgram = shader.generateShaderProgram(
        "./src/shader_code/vertex.vert", "./src/shader_code/fragment.frag"
    )

    shader.useShader(self.shaderProgram)

    self.tex = gl.glGenTextures(1)
    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)
    # gl.glUniform1i(gl.glGetUniformLocation(shaderProgram, "ourTex"), 0)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)

    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]

    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGBA32F,
        self.resolution[0],
        self.resolution[1],
        0,
        gl.GL_RGBA,
        gl.GL_FLOAT,
        None,
    )
    # gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, 1920, 1080, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, data)

    gl.glBindImageTexture(
        0, self.tex, 0, gl.GL_FALSE, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA32F
    )

    # init compute shader
    self.compute = comp.compileComputeShader("./src/shader_code/raytracer.comp")
    # self.compute = comp.compileComputeShader("./src/shader_code/mandelbrot.comp")


def resizeTexture(self):

    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex)


    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGBA32F,
        self.resolution[0],
        self.resolution[1],
        0,
        gl.GL_RGBA,
        gl.GL_FLOAT,
        None,
    )
