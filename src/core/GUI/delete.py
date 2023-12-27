import sceneManager as sm
import ctypes as ct
import util

def deleteMaterial(index):
    pass


def deleteVerts(meshIndex):
    r = sm.currentScene.sceneRenderer

    startingVert = r.meshes[meshIndex].startingVertex
    numVerts = r.meshes[meshIndex].numTriangles

    try:
        import core.renderer as renderer
        dst = ct.cast(
            ct.byref(r.vertices[startingVert]), ct.POINTER(renderer.Vertex)
        )
        src = ct.cast(
            ct.byref(r.vertices[startingVert + numVerts]), ct.POINTER(renderer.Vertex)
        )
        ct.memmove(dst, src, len(r.vertices[startingVert + numVerts:]) * ct.sizeof(renderer.Vertex))
        del renderer
        
        r.vertices = util.realloc(r.vertices, len(r.vertices) - numVerts)

    except IndexError:
        r.vertices = util.realloc(r.vertices, 0)


    for i in range(meshIndex + 1, len(r.meshes)):
        r.meshes[i].startingVertex -= numVerts

    

def deleteObject(index):
    r = sm.currentScene.sceneRenderer
    startingMesh = r.objects[index].startingMesh
    numMeshes = r.objects[index].numMeshes

    for i in range(startingMesh, startingMesh + numMeshes):
        deleteVerts(i)

    try:
        import core.renderer as renderer
        dst = ct.cast(
            ct.byref(r.meshes[startingMesh]), ct.POINTER(renderer.Mesh)
        )
        src = ct.cast(
            ct.byref(r.meshes[startingMesh + numMeshes]), ct.POINTER(renderer.Mesh)
        )
        ct.memmove(dst, src, len(r.meshes[startingMesh + numMeshes:]) * ct.sizeof(renderer.Mesh))
        del renderer

        r.meshes = util.realloc(r.meshes, len(r.meshes) - numMeshes)
    
    except IndexError:
        r.meshes = util.realloc(r.meshes, 0)


    r.meshNames = r.meshNames[:startingMesh] + r.meshNames[startingMesh + numMeshes:]
    r.meshTransforms = r.meshTransforms[:startingMesh] + r.meshTransforms[startingMesh + numMeshes:]
    r.meshVBO = r.meshVBO[:startingMesh] + r.meshVBO[startingMesh + numMeshes:]

    for i in range(index + 1, len(r.objects)):
        r.objects[i].startingMesh -= numMeshes

    try:
        import core.renderer as renderer
        dst = ct.cast(
            ct.byref(r.objects[index]), ct.POINTER(renderer.Object)
        )
        src = ct.cast(
            ct.byref(r.objects[index + 1]), ct.POINTER(renderer.Object)
        )
        ct.memmove(dst, src, len(r.objects[index + 1:]) * ct.sizeof(renderer.Object))
        del renderer

        r.objects = util.realloc(r.objects, len(r.objects) - 1)
    
    except IndexError:
        r.objects = util.realloc(r.objects, 0)

    r.objectNames = r.objectNames[:index] + r.objectNames[index + 1:]
    r.objectTransforms = r.objectTransforms[:index] + r.objectTransforms[index + 1:]

    r.updateBvh()
    r.getVertMeshRelation(0)
    r.updateBuffers(0)
    sm.currentScene.allocateSSBO()