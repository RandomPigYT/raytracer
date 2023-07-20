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

        self.camera = Camera()
        self.camera.position = (ct.c_float * 3)(*cameraPosition)

        self.camera.yaw = yaw
        self.camera.pitch = pitch

        self.camera.direction[0] = math.cos(math.radians(yaw)) * math.cos(
            math.radians(pitch)
        )
        self.camera.direction[1] = math.cos(math.radians(pitch))
        self.camera.direction[2] = math.sin(math.radians(yaw)) * math.cos(
            math.radians(pitch)
        )

        self.camera.direction = glm.normalize(self.camera.direction)

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

    def sendVerts(self):

        if not len(self.vertices):
            return
        # Resize vertices ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.vertSSBO)
        gl.glBufferData(
            gl.GL_SHADER_STORAGE_BUFFER,
            ct.sizeof(Vertex) * len(self.vertices),
            None,
            gl.GL_DYNAMIC_READ,
        )
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.vertSSBO)

        # Populate vertices ssbo
        ptr = ct.cast(
            gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
        )
        ct.memmove(ptr, self.vertices, ct.sizeof(Vertex) * len(self.vertices))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

    def sendMeshes(self):

        if not len(self.meshes):
            return
        # Resize meshes ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.meshSSBO)
        gl.glBufferData(
            gl.GL_SHADER_STORAGE_BUFFER,
            ct.sizeof(Mesh) * len(self.meshes),
            None,
            gl.GL_DYNAMIC_READ,
        )
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, self.meshSSBO)

        # Populate meshes ssbo
        ptr = ct.cast(
            gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
        )
        ct.memmove(ptr, self.meshes, ct.sizeof(Mesh) * len(self.meshes))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

    def sendMats(self):
        if not len(self.materials):
            return

        # Resize materials ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.materialSSBO)
        gl.glBufferData(
            gl.GL_SHADER_STORAGE_BUFFER,
            ct.sizeof(Material) * len(self.materials),
            None,
            gl.GL_DYNAMIC_READ,
        )
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.materialSSBO)

        # Populate materials ssbo
        ptr = ct.cast(
            gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
        )
        ct.memmove(ptr, self.materials, ct.sizeof(Material) * len(self.materials))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

    def sendSpheresToShader(self):
        
        if not len(self.spheres):
            return

        # Resize spheres ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.spheresSSBO)
        gl.glBufferData(
            gl.GL_SHADER_STORAGE_BUFFER,
            ct.sizeof(Sphere) * len(self.spheres),
            None,
            gl.GL_DYNAMIC_READ,
        )
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 4, self.spheresSSBO)

        # Populate spheres ssbo
        ptr = ct.cast(
            gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p
        )
        ct.memmove(ptr, self.spheres, ct.sizeof(Sphere) * len(self.spheres))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()
        self.sendMats()

    def sendUniforms(self):
        camPosLoc = gl.glGetUniformLocation(self.compute, "cameraPos")
        camDirLoc = gl.glGetUniformLocation(self.compute, "cameraDir")

        resolutionLoc = gl.glGetUniformLocation(self.compute, "resolution")

        gl.glUseProgram(self.compute)

        gl.glUniform3f(camPosLoc, *self.camera.position)
        gl.glUniform3f(camDirLoc, *self.camera.direction)

        gl.glUniform2f(resolutionLoc, *(ct.c_float * 2)(*self.resolution))

        # viewMat = glm.lookAt(
        #     self.camera.position,
        #     glm.vec3(self.camera.position) + glm.vec3(self.camera.direction),
        #     glm.vec3(0, 1, 0),
        # )

        viewMat = glm.lookAt(
            glm.vec3(0, 0, 0),
            glm.vec3(self.camera.direction),
            glm.vec3(0, 1, 0)
        )

        camToWorld = gl.glGetUniformLocation(self.compute, "camToWorld")
        gl.glUniformMatrix4fv(camToWorld, 1, gl.GL_FALSE, np.ravel(viewMat))

        gl.glUseProgram(self.compute)
        resolutionLoc = gl.glGetUniformLocation(self.compute, "resolution")
        gl.glUniform2f(resolutionLoc, *self.resolution)

        blurStrengthLoc = gl.glGetUniformLocation(self.compute, "blurStrength")
        gl.glUniform1f(blurStrengthLoc, self.camera.blur)

        fovLoc = gl.glGetUniformLocation(self.compute, "fov")
        gl.glUniform1f(fovLoc, self.camera.fov)



