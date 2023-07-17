import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import renderer.raytrace as rt
import renderer.model.loadModel as m
import deltatime
import renderer.camera as cam
import imgui
from imgui.integrations.glfw import GlfwRenderer
import renderer.GUI.guiElements as gElem
import sceneManager as sm



def render(window, scene, impl: GlfwRenderer):



    while not glfwWindowShouldClose(window):
        deltatime.startTime()


        imgui.new_frame()

        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]


        
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        rt.raytrace(scene, 10, 50)
        cam.move()

        shader.useShader(scene.shaderProgram)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, scene.tex)

        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)

        gElem.elements(window)

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfwPollEvents()
        impl.process_inputs()
        glfwSwapBuffers(window)

        # print(1 / deltatime.deltaTime())
