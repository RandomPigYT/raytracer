import OpenGL.GL as gl
import graphics.shader as shader
import ctypes as ct
import sceneManager as sm
import glm


def clampVec3(x, l, u):
    x[0] = min(x[0], u)
    x[0] = max(x[0], l)

    x[1] = min(x[1], u)
    x[1] = max(x[1], l)

    x[2] = min(x[2], u)
    x[2] = max(x[2], l)

    return x


def toneMap(x):
    x = glm.vec3(x[:-1])
    a = 2.51
    b = 0.03
    c = 2.43
    d = 0.59
    e = 0.14

    return glm.vec4(
        *clampVec3((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0), 1.0
    )


def gammaCorrect(x, gamma):
    invGamma = 1 / gamma
    return glm.vec4(*(glm.vec3(x) ** glm.vec3(invGamma)), 1.0)


def rasterize(self, voidColour):
    gl.glClearColor(*gammaCorrect(toneMap(voidColour), 2.2))

    if not len(self.meshes):
        return

    shader.useShader(self.rasterShader)
    gl.glBindVertexArray(self.meshVAO)

    import core.renderer as renderer

    for i in range(len(self.meshVBO)):
        sm.currentScene.sendRasterUniforms(i)

        bindingindex = 0
        gl.glBindVertexBuffer(
            bindingindex, self.meshVBO[i], 0, ct.sizeof(renderer.Vertex)
        )

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.meshes[i].numTriangles)
    del renderer

    gl.glBindVertexArray(0)
    shader.useShader(0)
