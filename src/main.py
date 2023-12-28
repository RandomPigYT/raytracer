#!/usr/bin/python

import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import core.scene as sc
import ctypes as ct
import init
import input as inp
import core.GUI.initImgui as initImgui
import imgui
import random
import core.save_and_load.save as save


import core.drawScene as drawScene


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
    io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
    io.config_flags |= imgui.CONFIG_NAV_NO_CAPTURE_KEYBOARD

    glfwSetKeyCallback(window, inp.keyCallback)
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    glfwSetCursorPosCallback(window, inp.mousePosCallback)

    gl.glEnable(gl.GL_DEPTH_TEST)

    camPos = (ct.c_float * 3)(0, 0, 3)
    camDir = (ct.c_float * 3)(0, 0, -1.0)

    scene: sc.Scene = sc.Scene("testScene", camPos, 0, 90, (1920, 1080), 1)
    # save.save()

    drawScene.render(window, scene, impl)

    glfwTerminate()


if __name__ == "__main__":
    main()
