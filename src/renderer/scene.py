import ctypes as ct
import renderer.canvas as canvas
import renderer.model.loadModel as lm
import OpenGL.GL as gl
import sceneManager as sm
import util
from glfw.GLFW import *


class Vertex(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 4),
        ("normal", ct.c_float * 4),
        ("textureCoord", ct.c_float * 2),
        ("padding0", ct.c_float * 2)
    ]


class Material(ct.Structure):
    _fields_ = [
        ("kd", ct.c_float * 4),  # 0   12
        ("ks", ct.c_float * 4),  # 32    12
        ("emission", ct.c_float * 4),  # 48  12
        ("intensity", ct.c_float * 4),
        ("alpha", ct.c_float * 2),  # 16  8
        ("padding1", ct.c_float * 2)  # 24  8
    ]


class Mesh(ct.Structure):
    _fields_ = [
        ("startingVertex", ct.c_uint32),
        ("numTriangles", ct.c_uint32),
        ("materialID", ct.c_uint32),
        ("objectID", ct.c_uint32),
    ]


class Object(ct.Structure):
    _fields_ = [("pos", ct.c_float * 3), ("ID", ct.c_uint32)]


class Sphere(ct.Structure):
    _fields_ = [("position", ct.c_float * 4), 
                ("radius", ct.c_float),
                ("materialID", ct.c_uint),
                ("padding0", ct.c_float * 3)]



class Camera:
    position = (ct.c_float * 3)(0, 0, 0)
    direction = (ct.c_float * 3)(0, 0, 0)

    pressedKeys = {GLFW_KEY_W: False, GLFW_KEY_A: False, GLFW_KEY_S: False, GLFW_KEY_D: False}

    prevMousePos = (ct.c_float * 2)(0, 0)


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

    playerSpeed = 1


    def __init__(self, name, cameraPosition, cameraDirection, resolution: tuple):
        if sm.currentScene == None:
            sm.currentScene = self

        self.name = name

        self.cameraPos = cameraPos
        self.cameraDirection = cameraDirection

        self.resolution = resolution

        self.camera = Camera()
        self.camera.direction = (ct.c_float * 3)(*cameraDirection)
        self.camera.position = (ct.c_float * 3)(*cameraPosition)
        
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        width = viewport[2]
        height = viewport[3]

        self.camera.prevMousePos[0] = width / 2
        self.camera.prevMousePos[1] = height / 2

        self.initSSBO()




    # Methods
    loadModel = lm.loadModel
    initCanvas = canvas.initRenderCavas

    
    def createSphere(self, radius, position):

        self.spheres = util.realloc(self.spheres, len(self.spheres) + 1)
        self.materials = util.realloc(self.materials, len(self.materials) + 1)

        self.spheres[len(self.spheres) - 1] = Sphere(position = position, 
                                                        radius = radius, 
                                                        materialID = len(self.materials) - 1)


        self.sendSpheresToShader()


    def setAsCurrent(self):
        sm.currentScene = self

    def initSSBO(self):
        self.vertSSBO = gl.glGenBuffers(1)
        self.meshSSBO = gl.glGenBuffers(1)
        self.materialSSBO = gl.glGenBuffers(1)
        self.spheresSSBO = gl.glGenBuffers(1)
    
    def allocateSSBO(self):

        # Resize vertices ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.vertSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Vertex) * len(self.vertices), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.vertSSBO)
        
        # Populate vertices ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.vertices, ct.sizeof(Vertex) * len(self.vertices))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)
    
        # Resize meshes ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.meshSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Mesh) * len(self.meshes), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, self.meshSSBO)
        
        # Populate meshes ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.meshes, ct.sizeof(Mesh) * len(self.meshes))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

        # Resize materials ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.materialSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Material) * len(self.materials), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.materialSSBO)
        
        # Populate materials ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.materials, ct.sizeof(Material) * len(self.materials))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)
        

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()

    def sendSpheresToShader(self):
        # Resize spheres ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.spheresSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Sphere) * len(self.spheres), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 4, self.spheresSSBO)

        # Populate spheres ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.spheres, ct.sizeof(Sphere) * len(self.spheres))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()
    
    def sendUniforms(self):
        camPosLoc = gl.glGetUniformLocation(self.compute, "cameraPos")
        camDirLoc = gl.glGetUniformLocation(self.compute, "cameraDir")

        resolutionLoc = gl.glGetUniformLocation(self.compute, "resolution")

        gl.glUseProgram(self.compute)

        gl.glUniform3f(camPosLoc, *self.cameraPos)
        gl.glUniform3f(camDirLoc, *self.cameraDirection)

        gl.glUniform2f(resolutionLoc, *(ct.c_float * 2)(*self.resolution))
        

        

    

        

