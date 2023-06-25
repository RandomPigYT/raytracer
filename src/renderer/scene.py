import ctypes as ct


class Vertex(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 3),
        ("padding0", ct.c_float),
        ("normal", ct.c_float * 3),
        ("padding1", ct.c_float),
        ("textureCoord", ct.c_float * 3),
        ("padding2", ct.c_float),
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
        ("startingVertex", ct.c_uint64),
        ("numTriangles", ct.c_uint64),
        ("materialID", ct.c_uint64),
        ("objectID", ct.c_uint64),
    ]


class Object(ct.Structure):
    _fields_ = [("pos", ct.c_float * 3), ("ID", ct.c_uint32)]


class Scene:
    def __init__(
        self,
        name,
        cameraPos,
        cameraDirection,
        vertices,
        materials,
        meshes,
        objects,
        objectNames,
        shaderProgram,
        computeProgram,
        quadVAO,
        quadVBO,
        quadEBO,
        quadTexture,
        ssbo
    ):
        self.name = name

        self.shaderProgram = shaderProgram
        self.computeProgram = computeProgram

        self.ssbo = ssbo

        self.quadVAO = quadVAO
        self.quadVBO = quadVBO
        self.quadEBO = quadEBO

        self.quadTexture = quadTexture

        self.cameraPos = cameraPos
        self.cameraDirection = cameraDirection

        self.vertices = vertices
        self.materials = materials
        self.meshes = meshes
        self.objects = objects
        self.objectNames = objectNames
