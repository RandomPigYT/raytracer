import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import graphics.computeShader as comp
import numpy as np
import graphics.canvas as canvas



def main():
    glfwInit()

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 5)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    window = graphics.window.createWindow(1920, 1080, "test", glfwGetPrimaryMonitor())


    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]


    compShaderProgram = comp.compileComputeShader("./src/shader_code/compute.comp")

    tex, shaderProgram = canvas.initRenderCavas()

    pixels: np.array = gl.glReadPixels(0, 0, width, height, gl.GL_RGBA, gl.GL_FLOAT)
    

    
    
    while not glfwWindowShouldClose(window):




        shader.useShader(compShaderProgram)
        gl.glDispatchCompute(width, height, 1)
    
        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)


        #gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        shader.useShader(shaderProgram)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
    
    
        #gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, 0)
        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, 4)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()
