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


    

    # impl = None
    camPos = (ct.c_float * 3)(0, 0, 3)
    camDir = (ct.c_float * 3)(0, 0, -1.0)

    scene: sc.Scene = sc.Scene("main", camPos, 0, 90, (1920, 1080))

    scene.initCanvas()

    scene.loadModel("models/cube.obj")
    # scene.loadModel("models/CornellBox-Original.obj")
    scene.createSphere(2, (ct.c_float * 4)(5, 2, 0, 0))
    scene.materials[scene.spheres[0].materialID].kd = (ct.c_float * 4)(*(1, 0, 1, 0))

    scene.createSphere(1, (ct.c_float * 4)(3, 5, 2, 0))
    scene.materials[scene.spheres[1].materialID].kd = (ct.c_float * 4)(*(0, 0, 1, 0))

    scene.createSphere(3, (ct.c_float * 4)(2, 0, 2, 0))
    scene.materials[scene.spheres[2].materialID].kd = (ct.c_float * 4)(*(0, 1, 0, 0))

    scene.sendMats()

    render.render(window, scene, impl)
    
    glfwTerminate()


if __name__ == "__main__":
    main()
