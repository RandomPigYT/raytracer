# import core.scene as sc
import ctypes as ct
import OpenGL.GL as gl
import time
import sceneManager as sm
import graphics.shader as shader



def raytrace(scene, maxBounces, raysPerPixel):
    global framNum

    sm.currentScene.sceneRenderer.frameNum += 1

    raysPerPixelLoc = gl.glGetUniformLocation(sm.currentScene.sceneRenderer.compute, "raysPerPixel")
    maxBouncesLoc = gl.glGetUniformLocation(sm.currentScene.sceneRenderer.compute, "maxBounces")
    timeLoc = gl.glGetUniformLocation(sm.currentScene.sceneRenderer.compute, "time")
    frameNumLoc = gl.glGetUniformLocation(sm.currentScene.sceneRenderer.compute, "frameNum")

    gl.glUseProgram(sm.currentScene.sceneRenderer.compute)

    gl.glUniform1ui(raysPerPixelLoc, raysPerPixel)
    gl.glUniform1ui(maxBouncesLoc, maxBounces)

    gl.glUniform1ui(timeLoc, int(time.time() * 10000))
    gl.glUniform1ui(frameNumLoc, sm.currentScene.sceneRenderer.frameNum)

    gl.glDispatchCompute(48, 45, 1)
    gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

    shader.useShader(sm.currentScene.sceneRenderer.shaderProgram)

    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, sm.currentScene.sceneRenderer.tex)

    gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
    # gl.glFinish()
