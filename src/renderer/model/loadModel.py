import renderer.scene as sc
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

    offset = len(self.vertices)

    self.vertices = util.realloc(self.vertices, len(self.vertices) + numFaces(shapes))

    # I'm compromising memory usage for speed

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
            offset,
        )

        offset += len(temp)

    #   for i in shape.mesh.indices:

    #       self.vertices[currentIndex + offset].position = (3 * ct.c_float)(attribs.vertices[i.vertex_index * 3],
    #                                                               attribs.vertices[(i.vertex_index * 3) + 1],
    #                                                               attribs.vertices[(i.vertex_index * 3) + 2])

    #       if i.texcoord_index >= 0:
    #           self.vertices[currentIndex + offset].textureCoord = (2 * ct.c_float)(attribs.texcoords[i.texcoord_index * 2],
    #                                                                       attribs.texcoords[(i.texcoord_index * 2) + 1])

    #       if i.normal_index >= 0:
    #           self.vertices[currentIndex + offset].normal = (3 * ct.c_float)(attribs.normals[i.normal_index * 3],
    #                                                                 attribs.normals[(i.normal_index * 3) + 1],
    #                                                                 attribs.normals[(i.normal_index * 3) + 2])

    #       currentIndex += 1

    for i in range(0, len(self.vertices), 3):
        print(*self.vertices[i].position)
        print(*self.vertices[i + 1].position)
        print(*self.vertices[i + 2].position)
        print()

    return True
