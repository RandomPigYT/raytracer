import core.raytrace as rt
import ctypes as ct
import core.transformedVerts as tv
import c_extension as cext
import core.vertMeshRelation as vmr
import core.initRasterizer as ir
import core.updateBuffers as ub
import core.rasterize as rasterize
import core.model.generateNormals as gn
import OpenGL.GL as gl
import util

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
        ("albedo", ct.c_float * 4),
        ("emission", ct.c_float * 4),
        ("intensity", ct.c_float * 4),
        ("refractiveIndex", ct.c_float * 4),
        ("transmittance", ct.c_float * 4),
        ("roughness", ct.c_float * 2),
        ("metallic", ct.c_float),
        ("reflectance", ct.c_float),
        ("opacity", ct.c_float),
        ("transmissionRoughness", ct.c_float),
        ("textureID", ct.c_int32),
        ("roughnessMapID", ct.c_int32),
        ("metallicMapID", ct.c_int32),
        ("emissiveMapID", ct.c_int32),
        ("normalMapID", ct.c_int32),
        ("opacityMapID", ct.c_int32),
        ("specularMapID", ct.c_int32),
        ("displacementMapID", ct.c_int32),
        ("padding0", ct.c_float * 2),
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
    _fields_ = [
        ("transform", 4 * (4 * ct.c_float)),
        ("ID", ct.c_uint32),
        ("startingMesh", ct.c_uint32),
        ("numMeshes", ct.c_uint32),
        ("padding0", ct.c_int32),
    ]


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

        self.objectNames = []
        self.meshNames = []
        self.matNames = []

        self.meshTransforms = []
        self.objectTransforms = []

        # Texture arrays
        # Format: [<Texture array ID>, <List of texture names>, <Texture handle>]
        self.textures = [(0 * ct.c_uint32)(), [], (0 * ct.c_uint64)()]

        self.vertMeshRelations = (0 * ct.c_uint32)()

        self.bvhs = None
        self.numBvhs = ct.c_uint32()

        self.spheres = (0 * Sphere)()

        self.vertSSBO = None
        self.meshSSBO = None
        self.materialSSBO = None
        self.bvhSSBO = None
        self.spheresSSBO = None
        self.vertMeshRelSSBO = None
        self.texSSBO = None

        self.frameNum = 0

        self.numBounces = 10
        self.raysPerPixel = 1

        self.shaderProgram = None
        self.compute = None

        self.rasterShader = None
        self.meshVBO = []
        self.meshVAO = 0

        self.initRasterizer()

        self.deleteTextureArrays()

        self.setDefaultMaterial()

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

    def setDefaultMaterial(self):
        self.matNames.append("Default material")
        self.materials = util.realloc(self.materials, 1)
        self.materials[0].albedo = (4 * ct.c_float)(
            162.0 / 255.0, 164.0 / 255.0, 165.0 / 255.0, 0.0
        )
        self.materials[0].opacity = 1.0
        self.materials[0].textureID = -1
        self.materials[0].roughnessMapID = -1
        self.materials[0].metallicMapID = -1
        self.materials[0].emissiveMapID = -1
        self.materials[0].normalMapID = -1
        self.materials[0].opacityMapID = -1
        self.materials[0].specularMapID = -1
        self.materials[0].displacementMapID = -1

    def deleteTextureArrays(self):
        gl.glDeleteTextures(
            len(self.textures[0]), ct.cast(self.textures[0], ct.POINTER(ct.c_float))
        )

    getTransformedVerts = tv.transformedVerts
    getVertMeshRelation = vmr.getVertMeshRelation
    initRasterizer = ir.initRasterizer
    updateBuffers = ub.updateBuffers

    renderRasterized = rasterize.rasterize

    generateNormals = gn.generateNormals
