import core.scene as sc
import ctypes as ct
import util
import tinyobjloader as tol
from sys import stderr
import c_extension as cext


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

    vertOffset = len(self.vertices)
    meshOffset = len(self.meshes)

    self.vertices = util.realloc(self.vertices, len(self.vertices) + numFaces(shapes))
    self.meshes = util.realloc(self.meshes, len(self.meshes) + len(shapes))
    self.materials = util.realloc(self.materials, len(self.materials) + len(shapes))

    # generate mesh data
    startingVertCount = 0
    for i in range(len(shapes)):
        self.meshes[i + meshOffset].startingVertex = startingVertCount + vertOffset
        self.meshes[i + meshOffset].numTriangles = len(shapes[i].mesh.indices)

        self.meshes[i + meshOffset].materialID = i + meshOffset

        startingVertCount += self.meshes[i + meshOffset].numTriangles

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
            ct.byref(ct.cast(self.vertices, ct.POINTER(sc.Vertex))),
            v,
            vn,
            vt,
            temp,
            len(temp),
            vertOffset,
        )

        vertOffset += len(temp)


    self.allocateSSBO()
    self.sendVerts()
    self.sendMeshes()
    self.sendMats()

    return True
