import ctypes as ct
import OpenGL.GL as gl
from glfw.GLFW import *
import glm
import numpy as np


def sendBuffer(ssbo, binding, buffer, count, size):

    # Resize buffer
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, ssbo)
    gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, size * count, None, gl.GL_DYNAMIC_READ)
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, binding, ssbo)

    if not count:
        return

    # Populate the buffer
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, buffer, size * count)
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)


def sendUniforms(self):
    camPosLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "cameraPos")
    camDirLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "cameraDir")

    resolutionLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "resolution")

    gl.glUseProgram(self.sceneRenderer.compute)

    gl.glUniform3f(camPosLoc, *self.camera.position)
    gl.glUniform3f(camDirLoc, *self.camera.direction)

    gl.glUniform2f(resolutionLoc, *(ct.c_float * 2)(*self.resolution))

    # viewMat = glm.lookAt(
    #     self.camera.position,
    #     glm.vec3(self.camera.position) + glm.vec3(self.camera.direction),
    #     glm.vec3(0, 1, 0),
    # )

    viewMat = glm.lookAt(
        glm.vec3(0, 0, 0), glm.vec3(self.camera.direction), glm.vec3(0, 1, 0)
    )

    camToWorld = gl.glGetUniformLocation(self.sceneRenderer.compute, "camToWorld")
    gl.glUniformMatrix4fv(camToWorld, 1, gl.GL_FALSE, np.ravel(viewMat))

    gl.glUseProgram(self.sceneRenderer.compute)
    resolutionLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "resolution")
    gl.glUniform2f(resolutionLoc, *self.resolution)

    blurStrengthLoc = gl.glGetUniformLocation(
        self.sceneRenderer.compute, "blurStrength"
    )
    gl.glUniform1f(blurStrengthLoc, self.camera.blur)

    fovLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "fov")
    gl.glUniform1f(fovLoc, self.camera.fov)
