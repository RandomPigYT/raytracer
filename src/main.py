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

#   program = shader.generateShaderProgram(
#       "./src/shader_code/vertex.vert", "./src/shader_code/fragment.frag"
#   )

#   computeProgram = comp.compileComputeShader("./src/shader_code/compute.comp")
#   shader.useShader(computeProgram)
#   gl.glDispatchCompute(5, 5, 1)

#   shader.useShader(program)

#   vbo = gl.glGenBuffers(1)
#   gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
#   gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices, gl.GL_STATIC_DRAW)

#   vao = gl.glGenVertexArrays(1)
#   gl.glBindVertexArray(vao)

#   gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 16, None)
#   gl.glVertexAttribPointer(1, 1, gl.GL_FLOAT, gl.GL_FALSE, 16, None)

#   gl.glEnableVertexAttribArray(0)
#   gl.glEnableVertexAttribArray(1)
#   

#   print(glfwGetWindowSize(window))

    canvas.initRenderCavas()
    while not glfwWindowShouldClose(window):
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
    
        #gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, 0)
        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, 4)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()
