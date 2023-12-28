import core.scene as sc
import ctypes as ct
import OpenGL.GL as gl
import time
import sceneManager as sm
import graphics.shader as shader
import math


def raytrace(scene, maxBounces, raysPerPixel, voidColour):
    global framNum

    if len(sm.currentScene.sceneRenderer.meshes) == 0:
        gl.glClearColor(*voidColour)
        return

    scene.sceneRenderer.frameNum += 1

    raysPerPixelLoc = gl.glGetUniformLocation(
        scene.sceneRenderer.compute, "raysPerPixel"
    )
    maxBouncesLoc = gl.glGetUniformLocation(scene.sceneRenderer.compute, "maxBounces")
    timeLoc = gl.glGetUniformLocation(scene.sceneRenderer.compute, "time")
    frameNumLoc = gl.glGetUniformLocation(scene.sceneRenderer.compute, "frameNum")

    gl.glUseProgram(scene.sceneRenderer.compute)

    gl.glUniform1ui(raysPerPixelLoc, raysPerPixel)
    gl.glUniform1ui(maxBouncesLoc, maxBounces)

    gl.glUniform1ui(timeLoc, int(time.time() * 10000))
    gl.glUniform1ui(frameNumLoc, scene.sceneRenderer.frameNum)

    gl.glActiveTexture(gl.GL_TEXTURE1)

    gl.glDispatchCompute(48, 45, 1)
    gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

    gl.glBindVertexArray(sm.currentScene.sceneRenderer.vao)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, sm.currentScene.sceneRenderer.vbo)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, sm.currentScene.sceneRenderer.ebo)

    gl.glBindTexture(gl.GL_TEXTURE_1D, 0)

    shader.useShader(scene.sceneRenderer.shaderProgram)

    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, scene.sceneRenderer.tex)

    gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
    # gl.glFinish()

    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
