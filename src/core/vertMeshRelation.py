import util
import ctypes as ct


def findMesh(obj, vertIndex) -> ct.c_uint32:
    for i in range(len(obj.meshes)):
        if (
            vertIndex >= obj.meshes[i].startingVertex
            and vertIndex < obj.meshes[i].startingVertex + obj.meshes[i].numTriangles
        ):
            return i


def getVertMeshRelation(self, startVert):
    self.vertMeshRelations = util.realloc(self.vertMeshRelations, len(self.vertices))

    for i in range(startVert, len(self.vertices)):
        self.vertMeshRelations[i] = findMesh(self, i)

