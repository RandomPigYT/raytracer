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
import input as inp
import deltatime
import renderer.camera as cam




        

def main():
    init.init(4, 5)

    window = graphics.window.createWindow(1920, 1080, "test", glfwGetPrimaryMonitor())
    # window = graphics.window.createWindow(1920, 1080, "test")

    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]


    glfwSetKeyCallback(window, inp.keyCallback)
    # glfwSetMouseButtonCallback(window, inp.mouseButtonCallback)
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    glfwSetCursorPosCallback(window, inp.mousePosCallback)

    # compShaderProgram = comp.compileComputeShader("./src/shader_code/mandelbrot.comp")
    #

    camPos = (ct.c_float * 3)(0, 0, 3)
    camDir = (ct.c_float * 3)(0, 0, -1.0)

    scene: sc.Scene = sc.Scene("main", camPos, 0, 90, (1920, 1080))

    scene.initCanvas()

    # scene.loadModel("models/cube.obj")
    # scene.loadModel("models/CornellBox-Original.obj")
    scene.createSphere(2, (ct.c_float * 4)(5, 2, 0, 0))
    scene.materials[scene.spheres[0].materialID].kd = (ct.c_float * 4)(*(1, 0, 1, 0))

    scene.createSphere(1, (ct.c_float * 4)(3, 5, 2, 0))
    scene.materials[scene.spheres[1].materialID].kd = (ct.c_float * 4)(*(0, 0, 1, 0))

    scene.createSphere(3, (ct.c_float * 4)(2, 0, 2, 0))
    scene.materials[scene.spheres[2].materialID].kd = (ct.c_float * 4)(*(0, 1, 0, 0))


    scene.sendMats()

    scene.playerSpeed = 10

    

    while not glfwWindowShouldClose(window):

        deltatime.startTime()


        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]


        # gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        rt.raytrace(scene, 1, 30)
        cam.move()

        shader.useShader(scene.shaderProgram)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, scene.tex)

        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)

        glfwSwapBuffers(window)
        glfwPollEvents()

        # print(1 / deltatime.deltaTime())

    glfwTerminate()


if __name__ == "__main__":
    main()
