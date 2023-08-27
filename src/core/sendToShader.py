import ctypes as ct
import core.canvas as canvas
import core.model.loadModel as lm
import OpenGL.GL as gl
import sceneManager as sm
import util
from glfw.GLFW import *
import glm
import numpy as np
import math
import core.scene as sc


def sendVerts(self):

    if not len(self.vertices):
        return
    # Resize vertices ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.vertSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(sc.Vertex) * len(self.vertices),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.vertSSBO)

    # Populate vertices ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.vertices, ct.sizeof(sc.Vertex) * len(self.vertices))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)



def sendMeshes(self):

    if not len(self.meshes):
        return
    # Resize meshes ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.meshSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(sc.Mesh) * len(self.meshes),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, self.meshSSBO)

    # Populate meshes ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.meshes, ct.sizeof(sc.Mesh) * len(self.meshes))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)


def sendMats(self):
    if not len(self.materials):
        return

    # Resize materials ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.materialSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(sc.Material) * len(self.materials),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.materialSSBO)

    # Populate materials ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.materials, ct.sizeof(sc.Material) * len(self.materials))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)


def sendSpheresToShader(self):
    
    if not len(self.spheres):
        return

    # Resize spheres ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.spheresSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(sc.Sphere) * len(self.spheres),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 4, self.spheresSSBO)

    # Populate spheres ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.spheres, ct.sizeof(sc.Sphere) * len(self.spheres))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

    self.sendUniforms()
    self.sendMats()


def sendUniforms(self):
    camPosLoc = gl.glGetUniformLocation(self.compute, "cameraPos")
    camDirLoc = gl.glGetUniformLocation(self.compute, "cameraDir")

    resolutionLoc = gl.glGetUniformLocation(self.compute, "resolution")

    gl.glUseProgram(self.compute)

    gl.glUniform3f(camPosLoc, *self.camera.position)
    gl.glUniform3f(camDirLoc, *self.camera.direction)

    gl.glUniform2f(resolutionLoc, *(ct.c_float * 2)(*self.resolution))

    # viewMat = glm.lookAt(
    #     self.camera.position,
    #     glm.vec3(self.camera.position) + glm.vec3(self.camera.direction),
    #     glm.vec3(0, 1, 0),
    # )

    viewMat = glm.lookAt(
        glm.vec3(0, 0, 0),
        glm.vec3(self.camera.direction),
        glm.vec3(0, 1, 0)
    )

    camToWorld = gl.glGetUniformLocation(self.compute, "camToWorld")
    gl.glUniformMatrix4fv(camToWorld, 1, gl.GL_FALSE, np.ravel(viewMat))

    gl.glUseProgram(self.compute)
    resolutionLoc = gl.glGetUniformLocation(self.compute, "resolution")
    gl.glUniform2f(resolutionLoc, *self.resolution)

    blurStrengthLoc = gl.glGetUniformLocation(self.compute, "blurStrength")
    gl.glUniform1f(blurStrengthLoc, self.camera.blur)

    fovLoc = gl.glGetUniformLocation(self.compute, "fov")
    gl.glUniform1f(fovLoc, self.camera.fov)