import renderer.scene as sc
import ctypes as ct
import os
import OpenGL.GL as gl
from c_extension import ext
import util


def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):
    
    raysPerPixelLoc = gl.glGetUniformLocation(scene.compute, "raysPerPixel")
    maxBouncesLoc = gl.glGetUniformLocation(scene.compute, "maxBounces")

    gl.glUseProgram(scene.compute)

    gl.glUniform1ui(raysPerPixelLoc, raysPerPixel)
    gl.glUniform1ui(maxBouncesLoc, maxBounces)

    gl.glDispatchCompute(scene.resolution[0], scene.resolution[1], 1)
    gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)


