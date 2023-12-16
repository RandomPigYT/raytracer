import ctypes as ct
import util
import tinyobjloader as tol
from sys import stderr
import c_extension as cext
import core.renderer as renderer
import OpenGL.GL as gl
import glm
import time
import os


class face(ct.Structure):
    _fields_ = [
        ("v_index", ct.c_int32),
        ("vt_index", ct.c_int32),
        ("vn_index", ct.c_int32),
    ]


def numFaces(shapes):
    count = 0
    for i in shapes:
        count += len(i.mesh.indices)

    return count


def loadModel(self, filename):
    oldLen = len(self.sceneRenderer.vertices)
    oldMeshLen = len(self.sceneRenderer.meshes)

    reader = tol.ObjReader()
    status = reader.ParseFromFile(filename)

    if not status:
        stderr.write("Failed to load " + filename)
        return False

    attribs = reader.GetAttrib()
    shapes = reader.GetShapes()
    materials = reader.GetMaterials()

    print(len(materials))

    v = (len(attribs.vertices) * ct.c_float)(*attribs.vertices)
    vn = (len(attribs.normals) * ct.c_float)(*attribs.normals)
    vt = (len(attribs.texcoords) * ct.c_float)(*attribs.texcoords)

    vertOffset = len(self.sceneRenderer.vertices)
    meshOffset = len(self.sceneRenderer.meshes)

    self.sceneRenderer.vertices = util.realloc(
        self.sceneRenderer.vertices, len(self.sceneRenderer.vertices) + numFaces(shapes)
    )
    self.sceneRenderer.meshes = util.realloc(
        self.sceneRenderer.meshes, len(self.sceneRenderer.meshes) + len(shapes)
    )
    self.sceneRenderer.materials = util.realloc(
        self.sceneRenderer.materials, len(self.sceneRenderer.materials) + len(shapes)
    )
    self.sceneRenderer.objects = util.realloc(
        self.sceneRenderer.objects, len(self.sceneRenderer.objects) + 1
    )

    # generate mesh data
    startingVertCount = 0
    for i in range(len(shapes)):
        self.sceneRenderer.meshes[i + meshOffset].startingVertex = (
            startingVertCount + vertOffset
        )
        self.sceneRenderer.meshes[i + meshOffset].numTriangles = len(
            shapes[i].mesh.indices
        )

        self.sceneRenderer.meshes[i + meshOffset].materialID = i + meshOffset

        startingVertCount += self.sceneRenderer.meshes[i + meshOffset].numTriangles

        self.sceneRenderer.meshes[
            i + meshOffset
        ].transform = util.mat4ToFloatArray4Array4(glm.mat4(1))

        self.sceneRenderer.meshTransforms.append(renderer.Transform())

        # Generate the VBOs for the newly added meshes
        self.sceneRenderer.meshVBO.append(gl.glGenBuffers(1))

    # generate vertices
    for shape in shapes:
        temp = (len(shape.mesh.indices) * face)(
            *[
                face(
                    v_index=i.vertex_index,
                    vt_index=i.texcoord_index,
                    vn_index=i.normal_index,
                )
                for i in shape.mesh.indices
            ]
        )

        cext.ext.generateVerts(
            ct.byref(ct.cast(self.sceneRenderer.vertices, ct.POINTER(renderer.Vertex))),
            v,
            vn,
            vt,
            temp,
            len(temp),
            vertOffset,
        )

        vertOffset += len(temp)

    self.sceneRenderer.generateNormals(oldLen)
    self.sceneRenderer.updateBvh()
    self.sceneRenderer.getVertMeshRelation(oldLen)

    self.sceneRenderer.updateBuffers(oldMeshLen)

    self.sendVertMeshRel()

    self.allocateSSBO()

    return True
