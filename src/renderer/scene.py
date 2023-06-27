import ctypes as ct
import renderer.canvas as canvas
import renderer.model.loadModel as lm


class Vertex(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 3),
        ("padding0", ct.c_float),
        ("normal", ct.c_float * 3),
        ("padding1", ct.c_float),
        ("textureCoord", ct.c_float * 2),
        ("padding2", 2 * ct.c_float),
    ]


class Material(ct.Structure):
    _fields_ = [
        ("kd", ct.c_float * 3),#0   12
        ("padding0", ct.c_float), #12   4
        ("alpha", ct.c_float * 2),# 16  8
        ("padding1", ct.c_float * 2), # 24  8
        ("ks", ct.c_float * 3), # 32    12
        ("padding1", ct.c_float), # 44  4
        ("emission", ct.c_float * 3), # 48  12
        ("padding3", ct.c_float)    # 60    4
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


class Scene:

    vertices = (0 * Vertex)()
    meshes = (0 * Mesh)()
    materials = (0 * Material)()
    objects = (0 * Object)()


    def __init__(
        self,
        name,
        cameraPos,
        cameraDirection
    ):
        self.name = name

        self.cameraPos = cameraPos
        self.cameraDirection = cameraDirection

    
    # Methods
    loadModel = lm.loadModel
    initCanvas = canvas.initRenderCavas










