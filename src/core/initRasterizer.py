import graphics.shader as shader
import OpenGL.GL as gl
import ctypes as ct


def initRasterizer(self):
    self.rasterShader = shader.generateShaderProgram(
        "./src/shader_code/rasterizer.vert", "./src/shader_code/rasterizer.frag"
    )

    self.meshVAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(self.meshVAO)

    # Hopefully this will prevent any circular import errors
    import core.renderer as renderer

    # gl.glVertexAttribPointer(
    #     0, 4, gl.GL_FLOAT, gl.GL_FALSE, ct.sizeof(renderer.Vertex), None
    # )
    # gl.glVertexAttribPointer(
    #     1,
    #     4,
    #     gl.GL_FLOAT,
    #     gl.GL_FALSE,
    #     ct.sizeof(renderer.Vertex),
    #     ct.c_void_p(renderer.Vertex.normal.offset)
    # )
    # gl.glVertexAttribPointer(
    #     2,
    #     2,
    #     gl.GL_FLOAT,
    #     gl.GL_FALSE,
    #     ct.sizeof(renderer.Vertex),
    #     ct.c_void_p(renderer.Vertex.textureCoord.offset)
    # )

    bindingindex = 0

    gl.glVertexAttribFormat(0, 4, gl.GL_FLOAT, gl.GL_FALSE, 0)
    gl.glVertexAttribBinding(0, bindingindex)
    gl.glVertexAttribFormat(
        1, 4, gl.GL_FLOAT, gl.GL_FALSE, renderer.Vertex.normal.offset
    )
    gl.glVertexAttribBinding(1, bindingindex)
    gl.glVertexAttribFormat(
        2, 2, gl.GL_FLOAT, gl.GL_FALSE, renderer.Vertex.textureCoord.offset
    )
    gl.glVertexAttribBinding(2, bindingindex)

    del renderer

    gl.glEnableVertexAttribArray(0)
    gl.glEnableVertexAttribArray(1)
    gl.glEnableVertexAttribArray(2)

    gl.glBindVertexArray(0)
