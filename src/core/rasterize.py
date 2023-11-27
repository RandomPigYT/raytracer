import OpenGL.GL as gl
import graphics.shader as shader
import ctypes as ct
import sceneManager as sm


def rasterize(self, voidColour):
    gl.glClearColor(*voidColour)

    shader.useShader(self.rasterShader)
    gl.glBindVertexArray(self.meshVAO)

    import core.renderer as renderer

    for i in range(len(self.meshVBO)):

        sm.currentScene.sendRasterUniforms(i)

        bindingindex = 0
        gl.glBindVertexBuffer(
            bindingindex, self.meshVBO[i], 0, ct.sizeof(renderer.Vertex)
        )

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.meshes[i].numTriangles)
    del renderer

    gl.glBindVertexArray(0)
    shader.useShader(0)
