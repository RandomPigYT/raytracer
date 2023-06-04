import graphics.window
from glfw.GLFW import *
import OpenGL.GL as gl
import graphics.shader as shader
import numpy as np

vertices = np.array([-0.5, -0.5, 0.0, 0.23,
                     0.5, -0.5, 0.0, 0.69,
                     0.0, 0.5, 0.0, 0.420], dtype="float32")


def main():
    glfwInit()

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    window = graphics.window.createWindow(800, 600, "test")

    program = shader.generateShaderProgram(
        "./src/shader_code/vertex.vert", "./src/shader_code/fragment.frag"
    )
    shader.useShader(program)

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices, gl.GL_STATIC_DRAW)

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 16, None)
    gl.glVertexAttribPointer(1, 1, gl.GL_FLOAT, gl.GL_FALSE, 16, None)

    gl.glEnableVertexAttribArray(0)
    gl.glEnableVertexAttribArray(1)

    while not glfwWindowShouldClose(window):
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()
