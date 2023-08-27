import core.scene as sc
import ctypes as ct
import os
import OpenGL.GL as gl
from c_extension import ext
import util
import time
import sceneManager as sm
import graphics.shader as shader



def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):
    global framNum

    sm.currentScene.frameNum += 1

    raysPerPixelLoc = gl.glGetUniformLocation(scene.compute, "raysPerPixel")
    maxBouncesLoc = gl.glGetUniformLocation(scene.compute, "maxBounces")
    timeLoc = gl.glGetUniformLocation(scene.compute, "time")
    frameNumLoc = gl.glGetUniformLocation(scene.compute, "frameNum")

    gl.glUseProgram(scene.compute)

    gl.glUniform1ui(raysPerPixelLoc, raysPerPixel)
    gl.glUniform1ui(maxBouncesLoc, maxBounces)

    gl.glUniform1ui(timeLoc, int(time.time() * 10000))
    gl.glUniform1ui(frameNumLoc, sm.currentScene.frameNum)

    gl.glDispatchCompute(48, 45, 1)
    gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

    shader.useShader(scene.shaderProgram)

    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, scene.tex)

    gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
    # gl.glFinish()
