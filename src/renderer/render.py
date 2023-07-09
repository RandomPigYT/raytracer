import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import renderer.raytrace as rt
import renderer.model.loadModel as m
import deltatime
import renderer.camera as cam


def render(window, scene):
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
