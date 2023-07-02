#!/usr/bin/python

import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import graphics.computeShader as comp
import numpy as np
import renderer.canvas as canvas
import renderer.raytrace as rt
import renderer.scene as sc
import ctypes as ct
import init
import renderer.model.loadModel as m
import graphics.input as inp





        

def main():
    init.init(4, 5)

    #window = graphics.window.createWindow(1920, 1080, "test", glfwGetPrimaryMonitor())
    window = graphics.window.createWindow(1920, 1080, "test")

    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]

    glfwSetKeyCallback(window, inp.keyCallback)

    # compShaderProgram = comp.compileComputeShader("./src/shader_code/mandelbrot.comp")
    #

    camPos = (ct.c_float * 3)(0, 0, -5)
    camDir = (ct.c_float * 3)(0, 0, 1.0)

    scene: sc.Scene = sc.Scene("main", camPos, camDir)

    scene.initCanvas()

    scene.loadModel("models/cube.obj")

    ssbo = gl.glGenBuffers(1)

    rt.raytrace(scene, 0, 0)

    targetFPS = 60
    frameTime = 1 / targetFPS

    prevTime = glfwGetTime()
    while not glfwWindowShouldClose(window):
        currentTime = glfwGetTime()
        dt = currentTime - prevTime

        while dt < frameTime:
            currentTime = glfwGetTime()
            dt = currentTime - prevTime

        prevTime = currentTime

        shader.useShader(scene.compute)
        gl.glDispatchCompute(width, height, 1)

        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        # gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        shader.useShader(scene.shaderProgram)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, scene.tex)

        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
        # gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, 4)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()
