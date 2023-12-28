import ctypes as ct
import core.canvas as canvas
import core.model.loadModel as lm
import OpenGL.GL as gl
import sceneManager as sm
import util
from glfw.GLFW import *
import glm
import numpy as np
import math
import core.sendToShader as sendToShader
import core.renderer as renderer
import core.GUI.uiManager as uiManager
import core.GUI.initGUI as initGUI
import core.save_and_load.sqlWrapper as SQLWrapper


class Camera:
    position = (ct.c_float * 3)(0, 0, 0)
    direction = (ct.c_float * 3)(0, 0, 0)

    # Euler angles in radians
    pitch = 0
    yaw = 0

    pressedKeys = {
        GLFW_KEY_W: False,
        GLFW_KEY_A: False,
        GLFW_KEY_S: False,
        GLFW_KEY_D: False,
        GLFW_KEY_SPACE: False,
        GLFW_KEY_LEFT_SHIFT: False,
    }

    prevMousePos = (ct.c_float * 2)(0, 0)

    playerSpeed = 3
    sensitivity = 0.05

    lockCam = False

    fov = 70
    blur = 1

    def __init__(self, pos, yaw, pitch) -> None:
        self.position = (ct.c_float * 3)(*pos)

        self.yaw = yaw
        self.pitch = pitch

        self.direction[0] = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
        self.direction[1] = math.cos(math.radians(pitch))
        self.direction[2] = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))

        self.direction = glm.normalize(self.direction)


class Scene:
    def __init__(
        self, name, cameraPosition, yaw, pitch, resolution: tuple, renderMode: int
    ):
        if sm.currentScene == None:
            sm.currentScene = self

        self.sceneRenderer = renderer.renderer(self, renderMode)

        self.uiManager = uiManager.UIManager()
        initGUI.initGUI(self)

        self.name = name.lower()

        self.resolution = resolution

        self.camera = Camera(cameraPosition, yaw, pitch)

        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]

        self.camera.prevMousePos[0] = 0
        self.camera.prevMousePos[1] = 0

        self.initCanvas()
        self.initSSBO()

        lm.loadTexture(self.sceneRenderer, "./src/core/model/BLANK.jpg", "", 0, False)

        self.sqlWrapper = SQLWrapper.SQLWrapper(
            "localhost", "root", "1234", "raytracer"
        )

    # Methods
    loadModel = lm.loadModel
    initCanvas = canvas.initRenderCavas
    resizeTexture = canvas.resizeTexture

    def sendVerts(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.vertSSBO,
            0,
            self.sceneRenderer.vertices,
            len(self.sceneRenderer.vertices),
            ct.sizeof(renderer.Vertex),
        )

    def sendMats(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.materialSSBO,
            1,
            self.sceneRenderer.materials,
            len(self.sceneRenderer.materials),
            ct.sizeof(renderer.Material),
        )

    def sendMeshes(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.meshSSBO,
            2,
            self.sceneRenderer.meshes,
            len(self.sceneRenderer.meshes),
            ct.sizeof(renderer.Mesh),
        )

    def sendBvhs(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.bvhSSBO,
            5,
            self.sceneRenderer.bvhs,
            self.sceneRenderer.numBvhs.value,
            ct.sizeof(renderer.Bvh),
        )

    def sendVertMeshRel(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.vertMeshRelSSBO,
            6,
            self.sceneRenderer.vertMeshRelations,
            len(self.sceneRenderer.vertMeshRelations),
            ct.sizeof(ct.c_uint32),
        )

    def sendTextures(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.texSSBO,
            7,
            self.sceneRenderer.textures[2],
            len(self.sceneRenderer.textures[2]),
            ct.sizeof(ct.c_uint64),
        )

    def sendSpheresToShader(self):
        sendToShader.sendBuffer(
            self.sceneRenderer.spheresSSBO,
            4,
            self.sceneRenderer.spheres,
            len(self.sceneRenderer.spheres),
            ct.sizeof(renderer.Sphere),
        )
        self.sendUniforms()
        self.sendMats()

    sendUniforms = sendToShader.sendUniforms

    def resetFrame(self):
        self.sceneRenderer.frameNum = 0

    def createSphere(self, radius, position):
        self.sceneRenderer.spheres = util.realloc(
            self.sceneRenderer.spheres, len(self.sceneRenderer.spheres) + 1
        )
        self.sceneRenderer.materials = util.realloc(
            self.sceneRenderer.materials, len(self.sceneRenderer.materials) + 1
        )

        self.sceneRenderer.spheres[
            len(self.sceneRenderer.spheres) - 1
        ] = renderer.Sphere(
            position=position,
            radius=radius,
            materialID=len(self.sceneRenderer.materials) - 1,
        )

        self.sendSpheresToShader()
        self.sendMats()

    def setAsCurrent(self):
        sm.currentScene = self

    def initSSBO(self):
        self.sceneRenderer.vertSSBO = gl.glGenBuffers(1)
        self.sceneRenderer.meshSSBO = gl.glGenBuffers(1)
        self.sceneRenderer.materialSSBO = gl.glGenBuffers(1)
        self.sceneRenderer.spheresSSBO = gl.glGenBuffers(1)
        self.sceneRenderer.bvhSSBO = gl.glGenBuffers(1)
        self.sceneRenderer.vertMeshRelSSBO = gl.glGenBuffers(1)
        self.sceneRenderer.texSSBO = gl.glGenBuffers(1)

    def allocateSSBO(self):
        self.sendVerts()
        self.sendMeshes()
        self.sendVertMeshRel()
        self.sendMats()
        self.sendBvhs()
        self.sendTextures()
        self.sendSpheresToShader()

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()

    def sendRasterUniforms(self, meshIndex):
        rendererObj = self.sceneRenderer

        modelLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "model")
        viewLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "view")
        projectionLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "projection")
        normalViewLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "normalView")

        cameraPosLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "camPos")
        model = glm.mat4(rendererObj.meshes[meshIndex].transform)

        view = glm.mat4(1)
        # view = glm.translate(view, -glm.vec3(*self.camera.position))
        view = glm.lookAt(
            self.camera.position,
            glm.vec3(*self.camera.position) + glm.vec3(*self.camera.direction),
            glm.vec3(0, 1, 0),
        )

        try:
            aspect = self.resolution[0] / self.resolution[1]

        except ZeroDivisionError:
            aspect = 0

        projection = glm.perspective(
            glm.radians(self.camera.fov),
            aspect,
            0.1,
            100,
        )

        gl.glUniformMatrix4fv(modelLoc, 1, gl.GL_FALSE, glm.value_ptr(model))
        gl.glUniformMatrix4fv(viewLoc, 1, gl.GL_FALSE, glm.value_ptr(view))
        gl.glUniformMatrix4fv(projectionLoc, 1, gl.GL_FALSE, glm.value_ptr(projection))
        # gl.glUniform3fv(cameraPosLoc, 1, glm.value_ptr(glm.vec3(*self.camera.position)))

        normalView = glm.lookAt(
            self.camera.position, glm.vec3(0.0, 0.0, 1.0), glm.vec3(0, 1, 0)
        )

        gl.glUniformMatrix4fv(normalViewLoc, 1, gl.GL_FALSE, glm.value_ptr(normalView))

        resolutionLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "resolution")
        gl.glUniform2f(resolutionLoc, *self.resolution)

        fovLoc = gl.glGetUniformLocation(rendererObj.rasterShader, "fov")
        gl.glUniform1f(fovLoc, glm.radians(self.camera.fov))
