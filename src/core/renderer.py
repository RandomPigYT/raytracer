import core.raytrace as rt
import ctypes as ct
import core.transformedVerts as tv
import c_extension as cext
import core.vertMeshRelation as vmr
import core.initRasterizer as ir
import core.updateBuffers as ub
import core.rasterize as rasterize
import core.model.generateNormals as gn

RAYTRACE = 0
RASTERIZE = 1


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
        ("transform", 4 * (4 * ct.c_float)),
    ]


class Object(ct.Structure):
    _fields_ = [("pos", ct.c_float * 3), ("ID", ct.c_uint32)]


class Bvh(ct.Structure):
    _fields_ = [
        ("corner1", 4 * ct.c_float),
        ("corner2", 4 * ct.c_float),
        ("hitIndex", ct.c_int32),
        ("missIndex", ct.c_int32),
        ("numTris", ct.c_uint32),
        ("triIndices", 4 * ct.c_uint32),
        ("padding0", ct.c_int32),
    ]


class Sphere(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 4),
        ("radius", ct.c_float),
        ("materialID", ct.c_uint32),
        ("padding0", ct.c_float * 2),
    ]


class Transform(ct.Structure):
    position = [0, 0, 0]
    rotation = [0, 0, 0]
    scale = [1, 1, 1]


class renderer:
    # vertices = (0 * Vertex)()
    # meshes = (0 * Mesh)()
    # materials = (0 * Material)()
    # objects = (0 * Object)()

    # meshTransforms = []

    # vertMeshRelations = (0 * ct.c_uint32)()
    # vertMeshRelTex = None

    # bvhs = None
    # numBvhs = ct.c_uint32()

    # spheres = (0 * Sphere)()

    # vertSSBO = None
    # meshSSBO = None
    # materialSSBO = None
    # bvhSSBO = None
    # spheresSSBO = None
    # vertMeshRelSSBO = None

    # frameNum = 0

    # numBounces = 10
    # raysPerPixel = 1

    # shaderProgram = None
    # compute = None

    # rasterShader = None
    # meshVBO = []
    # meshVAO = 0

    # mode:
    # 0 -> raytrace
    # 1 -> rasterize
    def __init__(self, scene, mode: int):
        self.mode = mode
        self.scene = scene

        self.vertices = (0 * Vertex)()
        self.meshes = (0 * Mesh)()
        self.materials = (0 * Material)()
        self.objects = (0 * Object)()

        self.meshTransforms = []

        self.vertMeshRelations = (0 * ct.c_uint32)()
        self.vertMeshRelTex = None

        self.bvhs = None
        self.numBvhs = ct.c_uint32()

        self.spheres = (0 * Sphere)()

        self.vertSSBO = None
        self.meshSSBO = None
        self.materialSSBO = None
        self.bvhSSBO = None
        self.spheresSSBO = None
        self.vertMeshRelSSBO = None

        self.frameNum = 0

        self.numBounces = 10
        self.raysPerPixel = 1

        self.shaderProgram = None
        self.compute = None

        self.rasterShader = None
        self.meshVBO = []
        self.meshVAO = 0

        self.initRasterizer()

    def render(self, voidColour=(0.663, 0.965, 0.969, 1)):
        if self.mode == RAYTRACE:
            rt.raytrace(self.scene, self.numBounces, self.raysPerPixel)

        elif self.mode == RASTERIZE:
            self.renderRasterized(voidColour)

    def switchMode(self, mode):
        self.mode = mode

    def updateBvh(self):
        transformedVerts = self.getTransformedVerts()

        if self.bvhs != None:
            cext.ext.freeBvh(self.bvhs)

        self.bvhs = cext.ext.constructBvh(
            ct.byref(self.numBvhs),
            ct.cast(transformedVerts, ct.POINTER(Vertex)),
            len(transformedVerts),
        )

    getTransformedVerts = tv.transformedVerts
    getVertMeshRelation = vmr.getVertMeshRelation
    initRasterizer = ir.initRasterizer
    updateBuffers = ub.updateBuffers

    renderRasterized = rasterize.rasterize

    generateNormals = gn.generateNormals
