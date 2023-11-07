import OpenGL.GL as gl
import ctypes as ct
import numpy as np


def updateBuffers(self, start):
    for i in range(start, len(self.meshes)):
        offset = self.meshes[i].startingVertex

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.meshVBO[i])
        import core.renderer as renderer

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self.meshes[i].numTriangles * ct.sizeof(renderer.Vertex),
            ct.byref(self.vertices[offset]),
            gl.GL_DYNAMIC_DRAW,
        )
        del renderer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
