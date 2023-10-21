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

        # Create vertex-mesh relation texture
        self.sceneRenderer.vertMeshRelTex = gl.glGenTextures(1)

        self.name = name

        self.resolution = resolution

        self.camera = Camera(cameraPosition, yaw, pitch)

        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]

        self.camera.prevMousePos[0] = 0
        self.camera.prevMousePos[1] = 0

        self.initCanvas()
        self.initSSBO()

    # Methods
    loadModel = lm.loadModel
    initCanvas = canvas.initRenderCavas
    resizeTexture = canvas.resizeTexture

    sendVerts = sendToShader.sendVerts
    sendMeshes = sendToShader.sendMeshes
    sendMats = sendToShader.sendMats
    sendBvhs = sendToShader.sendBvhs
    sendSpheresToShader = sendToShader.sendSpheresToShader

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

    def allocateSSBO(self):
        self.sendVerts()
        self.sendMeshes()
        self.sendMats()
        self.sendBvhs()

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()
