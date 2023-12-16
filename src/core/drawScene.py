import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import core.raytrace as rt
import core.model.loadModel as m
import deltatime
import core.camera as cam
import imgui
from imgui.integrations.glfw import GlfwRenderer
import core.GUI.guiElements as gElem
import sceneManager as sm

import core.scene as sc
import os


def render(window, scene: sc.Scene, impl: GlfwRenderer):
    while not glfwWindowShouldClose(window):
        deltatime.startTime()

        imgui.new_frame()

        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # rt.raytrace(scene, scene.numBounces, max(scene.raysPerPixel, 1))
        if os.name == "nt":
            scene.sceneRenderer.render()
            gl.glFinish()

        cam.move()

        sm.currentScene.uiManager.render()
        # gElem.elements(window)

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfwPollEvents()
        impl.process_inputs()
        glfwSwapBuffers(window)

        # print(1 / deltatime.deltaTime())
