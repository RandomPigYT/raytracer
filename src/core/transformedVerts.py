import core.renderer as renderer
import ctypes as ct
import glm


def applyTransformation(vert, mesh):
    temp = glm.vec4(*vert.position)
    temp[3] = 1
    temp = glm.mat4(mesh.transform) * temp

    return (4 * ct.c_float)(*temp)


def transformedVerts(self):
    v = (len(self.vertices) * renderer.Vertex)()

    for i in self.meshes:
        offset = i.startingVertex
        for j in range(i.numTriangles):
            v[offset + j].position = applyTransformation(self.vertices[offset + j], i)

    return v
