import core.scene as sc
import ctypes as ct
import util
import tinyobjloader as tol
from sys import stderr
import c_extension as cext
import core.renderer as renderer

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
    reader = tol.ObjReader()
    status = reader.ParseFromFile(filename)

    if not status:
        stderr.write("Failed to load " + filename)
        return False

    attribs = reader.GetAttrib()
    shapes = reader.GetShapes()

    v = (len(attribs.vertices) * ct.c_float)(*attribs.vertices)
    vn = (len(attribs.normals) * ct.c_float)(*attribs.normals)
    vt = (len(attribs.texcoords) * ct.c_float)(*attribs.texcoords)

    vertOffset = len(self.sceneRenderer.vertices)
    meshOffset = len(self.sceneRenderer.meshes)

    self.sceneRenderer.vertices = util.realloc(self.sceneRenderer.vertices, len(self.sceneRenderer.vertices) + numFaces(shapes))
    self.sceneRenderer.meshes = util.realloc(self.sceneRenderer.meshes, len(self.sceneRenderer.meshes) + len(shapes))
    self.sceneRenderer.materials = util.realloc(self.sceneRenderer.materials, len(self.sceneRenderer.materials) + len(shapes))

    # generate mesh data
    startingVertCount = 0
    for i in range(len(shapes)):
        self.sceneRenderer.meshes[i + meshOffset].startingVertex = startingVertCount + vertOffset
        self.sceneRenderer.meshes[i + meshOffset].numTriangles = len(shapes[i].mesh.indices)

        self.sceneRenderer.meshes[i + meshOffset].materialID = i + meshOffset

        startingVertCount += self.sceneRenderer.meshes[i + meshOffset].numTriangles

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

    a = ct.c_uint32()
    bvhs = cext.ext.constructBvh(
            ct.byref(a),
            ct.cast(self.sceneRenderer.vertices, ct.POINTER(renderer.Vertex)),
            len(self.sceneRenderer.vertices)
    )
    os.system("cls")
   #print(a.value)
   #print(len(self.sceneRenderer.vertices) / 3)

    for i in range(a.value):
        print(bvhs[i].hitIndex, bvhs[i].missIndex, bvhs[i].numTris, sep=' ')

    cext.ext.freeBvh(bvhs)

    self.allocateSSBO()
    self.sendVerts()
    self.sendMeshes()
    self.sendMats()

    return True
