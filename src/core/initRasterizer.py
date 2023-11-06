import graphics.shader as shader
import core.renderer as renderer
import OpenGL.GL as gl
import ctypes as ct


def initRasterizer(self: renderer.renderer):
    self.rasterShader = shader.generateShaderProgram(
        "./src/shader_code/rasterizer.vert", "./src/shader_code/rasterizer.frag"
    )

    self.meshVAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(self.meshVAO)
    
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, ct.sizeof(renderer.Vertex))


