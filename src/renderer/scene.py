import ctypes as ct
import renderer.canvas as canvas
import renderer.model.loadModel as lm
import OpenGL.GL as gl
import sceneManager as sm
import util
from glfw.GLFW import *
import glm
import numpy as np
import math
import renderer.sendToShader as sendToShader

class Vertex(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 4),
        ("normal", ct.c_float * 4),
        ("textureCoord", ct.c_float * 2),
        ("padding0", ct.c_float * 2),
    ]


class Material(ct.Structure):
    _fields_ = [
        # ("kd", ct.c_float * 4),  # 0   12
        # ("ks", ct.c_float * 4),  # 32    12
        ("albedo", ct.c_float * 4),
        ("emission", ct.c_float * 4),  # 48  12
        ("intensity", ct.c_float * 4),
        ("refractiveIndex", ct.c_float * 4),
        ("roughness", ct.c_float * 2),  # 16  8
        ("metallic", ct.c_float),
        ("reflectance", ct.c_float),  # 24  8
    ]


class Mesh(ct.Structure):
    _fields_ = [
        ("startingVertex", ct.c_uint32),
        ("numTriangles", ct.c_uint32),
        ("materialID", ct.c_uint32),
        ("objectID", ct.c_uint32),
        ("position", 4 * ct.c_float)
    ]


class Object(ct.Structure):
    _fields_ = [("pos", ct.c_float * 3), ("ID", ct.c_uint32)]


class Sphere(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 4),
        ("radius", ct.c_float),
        ("materialID", ct.c_uint32),
        ("padding0", ct.c_float * 2),
    ]


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

        self.direction[0] = math.cos(math.radians(yaw)) * math.cos(
            math.radians(pitch)
        )
        self.direction[1] = math.cos(math.radians(pitch))
        self.direction[2] = math.sin(math.radians(yaw)) * math.cos(
            math.radians(pitch)
        )

        self.direction = glm.normalize(self.direction)


        


class Scene:
    # All the variables defined outside methods have been placed where they have been
    # for arbitrary reasons. Don't read too much into it.
    vertices = (0 * Vertex)()
    meshes = (0 * Mesh)()
    materials = (0 * Material)()
    objects = (0 * Object)()

    spheres = (0 * Sphere)()

    vertSSBO = None
    meshSSBO = None
    materialSSBO = None
    spheresSSBO = None
    
    frameNum = 0

    numBounces = 10
    raysPerPixel = 1

    def __init__(self, name, cameraPosition, yaw, pitch, resolution: tuple):
        if sm.currentScene == None:
            sm.currentScene = self

        self.name = name

        self.resolution = resolution

        self.camera = Camera(cameraPosition, yaw, pitch)

        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]

        self.camera.prevMousePos[0] = 0
        self.camera.prevMousePos[1] = 0

        self.initSSBO()

    # Methods
    loadModel = lm.loadModel
    initCanvas = canvas.initRenderCavas
    resizeTexture = canvas.resizeTexture

    sendVerts = sendToShader.sendVerts
    sendMeshes = sendToShader.sendMeshes
    sendMats = sendToShader.sendMats
    sendSpheresToShader = sendToShader.sendSpheresToShader

    sendUniforms = sendToShader.sendUniforms

    def resetFrame(self):
        self.frameNum = 0

    def createSphere(self, radius, position):
        self.spheres = util.realloc(self.spheres, len(self.spheres) + 1)
        self.materials = util.realloc(self.materials, len(self.materials) + 1)

        self.spheres[len(self.spheres) - 1] = Sphere(
            position=position, radius=radius, materialID=len(self.materials) - 1
        )

        self.sendSpheresToShader()
        self.sendMats()

    def setAsCurrent(self):
        sm.currentScene = self

    def initSSBO(self):
        self.vertSSBO = gl.glGenBuffers(1)
        self.meshSSBO = gl.glGenBuffers(1)
        self.materialSSBO = gl.glGenBuffers(1)
        self.spheresSSBO = gl.glGenBuffers(1)

    def allocateSSBO(self):
        self.sendVerts()
        self.sendMeshes()
        self.sendMats()

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()








