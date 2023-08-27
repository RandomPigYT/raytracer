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
import core.renderer as renderer


def sendVerts(self):

    if not len(self.sceneRenderer.vertices):
        return
    # Resize vertices ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.sceneRenderer.vertSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(renderer.Vertex) * len(self.sceneRenderer.vertices),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.sceneRenderer.vertSSBO)

    # Populate vertices ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.sceneRenderer.vertices, ct.sizeof(renderer.Vertex) * len(self.sceneRenderer.vertices))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)



def sendMeshes(self):

    if not len(self.sceneRenderer.meshes):
        return
    # Resize meshes ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.sceneRenderer.meshSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(renderer.Mesh) * len(self.sceneRenderer.meshes),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, self.sceneRenderer.meshSSBO)

    # Populate meshes ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.sceneRenderer.meshes, ct.sizeof(renderer.Mesh) * len(self.sceneRenderer.meshes))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)


def sendMats(self):
    if not len(self.sceneRenderer.materials):
        return

    # Resize materials ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.sceneRenderer.materialSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(renderer.Material) * len(self.sceneRenderer.materials),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.sceneRenderer.materialSSBO)

    # Populate materials ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.sceneRenderer.materials, ct.sizeof(renderer.Material) * len(self.sceneRenderer.materials))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)


def sendSpheresToShader(self):
    
    if not len(self.sceneRenderer.spheres):
        return

    # Resize spheres ssbo
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.sceneRenderer.spheresSSBO)
    gl.glBufferData(
        gl.GL_SHADER_STORAGE_BUFFER,
        ct.sizeof(renderer.Sphere) * len(self.sceneRenderer.spheres),
        None,
        gl.GL_DYNAMIC_READ,
    )
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 4, self.sceneRenderer.spheresSSBO)

    # Populate spheres ssbo
    ptr = ct.cast(
        gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
    )
    ct.memmove(ptr, self.sceneRenderer.spheres, ct.sizeof(renderer.Sphere) * len(self.sceneRenderer.spheres))
    gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

    self.sendUniforms()
    self.sendMats()


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
        glm.vec3(0, 0, 0),
        glm.vec3(self.camera.direction),
        glm.vec3(0, 1, 0)
    )

    camToWorld = gl.glGetUniformLocation(self.sceneRenderer.compute, "camToWorld")
    gl.glUniformMatrix4fv(camToWorld, 1, gl.GL_FALSE, np.ravel(viewMat))

    gl.glUseProgram(self.sceneRenderer.compute)
    resolutionLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "resolution")
    gl.glUniform2f(resolutionLoc, *self.resolution)

    blurStrengthLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "blurStrength")
    gl.glUniform1f(blurStrengthLoc, self.camera.blur)

    fovLoc = gl.glGetUniformLocation(self.sceneRenderer.compute, "fov")
    gl.glUniform1f(fovLoc, self.camera.fov)