import core.renderer as renderer
import ctypes as ct


def applyTransformation(vert, mesh):
    temp = (4 * ct.c_float)(*vert.position)
    # For now, this only includes translation
    temp[0] += mesh.position[0]
    temp[1] += mesh.position[1]
    temp[2] += mesh.position[2]

    return temp


def transformedVerts(self):
    v = (len(self.vertices) * renderer.Vertex)()

    for i in self.meshes:
        offset = i.startingVertex
        for j in range(i.numTriangles):
            v[offset + j].position = applyTransformation(self.vertices[offset + j], i)

    return v
