#!/usr/bin/python

import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import renderer.raytrace as rt
import renderer.scene as sc
import ctypes as ct
import init
import renderer.model.loadModel as m
import input as inp
import deltatime
import renderer.camera as cam
import renderer.GUI.initImgui as initImgui
import imgui
import random


import renderer.render as render


def main():
    init.init(4, 5)

    window = graphics.window.createWindow(
        1920, 1080, "raytracer", glfwGetPrimaryMonitor()
    )
    # window = graphics.window.createWindow(1920, 1080, "test")

    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]

    impl = initImgui.init(window)

    io = imgui.get_io()
    io.config_flags |= imgui.CONFIG_NO_MOUSE
    # io.config_flags |= imgui.CONFIG_NAV_NO_CAPTURE_KEYBOARD

    glfwSetKeyCallback(window, inp.keyCallback)
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    glfwSetCursorPosCallback(window, inp.mousePosCallback)


    # glfwSwapInterval(1)

    # impl = None
    camPos = (ct.c_float * 3)(0, 0, 3)
    camDir = (ct.c_float * 3)(0, 0, -1.0)

    scene: sc.Scene = sc.Scene("main", camPos, 0, 90, (1920, 1080))

    # print(*(scene.camera.direction))

    scene.initCanvas()

    scene.loadModel("models/plane.obj")

    scene.materials[scene.meshes[0].materialID].albedo  = (ct.c_float * 4)(*(249 / 255, 170 / 255, 70 / 255, 0))

    scene.loadModel("models/cube.obj")
    # scene.loadModel("models/myCornellBox.obj")
    # scene.loadModel("models/CornellBox-Original.obj")
    scene.createSphere(0.73, (ct.c_float * 4)(0.96, 0.05, 2.37, 0))
    scene.materials[scene.spheres[0].materialID].albedo = (ct.c_float * 4)(*(84 / 255, 255 / 255, 119 / 255, 0))

    scene.createSphere(36.86, (ct.c_float * 4)(4.62, 12.19, 70.37, 0))
    scene.materials[scene.spheres[1].materialID].albedo = (ct.c_float * 4)(*(0, 0, 0, 0))
    scene.materials[scene.spheres[1].materialID].emission = (ct.c_float * 4)(0xf6 / 255, 0xcd / 255, 0x8b / 255, 0)
    scene.materials[scene.spheres[1].materialID].intensity = (ct.c_float * 4)(*(12, 12, 12, 0))

    # scene.createSphere(27.5, (ct.c_float * 4)(2, -28.05, 2, 0))
    # scene.materials[scene.spheres[2].materialID].albedo = (ct.c_float * 4)(*(249 / 255, 170 / 255, 70 / 255, 0))

    scene.createSphere(0.25, (ct.c_float * 4)(2, -0.32, 2, 0))
    scene.materials[scene.spheres[2].materialID].albedo = (ct.c_float * 4)(*(random.random(), random.random(), random.random(), 0))
    scene.sendMats()

    render.render(window, scene, impl)
    
    glfwTerminate()


if __name__ == "__main__":
    main()
