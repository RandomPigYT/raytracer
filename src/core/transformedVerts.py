import core.renderer as renderer
import ctypes as ct
import glm


def applyTransformation(vert, mesh):
    # temp = (4 * ct.c_float)(*vert.position)

    temp = glm.vec4(*vert.position)
    temp[3] = 1
    temp = glm.mat4(mesh.transform) * temp

    # # For now, this only includes translation
    # temp[0] += mesh.position[0]
    # temp[1] += mesh.position[1]
    # temp[2] += mesh.position[2]

    return (4 * ct.c_float)(*temp)


def transformedVerts(self):
    v = (len(self.vertices) * renderer.Vertex)()

    for i in self.meshes:
        offset = i.startingVertex
        for j in range(i.numTriangles):
            v[offset + j].position = applyTransformation(self.vertices[offset + j], i)

    return v
