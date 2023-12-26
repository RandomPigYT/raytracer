import imgui
import sceneManager as sm
import ctypes as ct
import glm
import util

def materials():
    pass

def meshes(object):
    pass

# type: 
# 0: mesh
# 1: object
def drawTransforms(index, elementType, objIndex):
    transformList = None
    elementList = None
    if elementType == 0:
        transformList = sm.currentScene.sceneRenderer.meshTransforms
        elementList = sm.currentScene.sceneRenderer.meshes

    else:
        transformList = sm.currentScene.sceneRenderer.objectTransforms
        elementList = sm.currentScene.sceneRenderer.objects

    prevPos = glm.vec3([*transformList[index].position])
    prevRot = glm.vec3([*transformList[index].rotation])
    prevScale = glm.vec3([*transformList[index].scale])

    shouldUpdateBvh = False
        
    status, pos = imgui.drag_float3(
        "Position##" + str(index) + "##" + str(elementType),
        *transformList[index].position,
        0.01,
        format="%.2f",
    )
    if status:
        transformList[index].position = pos
        shouldUpdateBvh = True

    status, rot = imgui.drag_float3(
        "Rotation##" + str(index) + "##" + str(elementType),
        *transformList[index].rotation,
        0.01,
        format="%.2f",
    )
    if status:
        transformList[index].rotation = rot
        shouldUpdateBvh = True

    status, scale = imgui.drag_float3(
        "Scale##" + str(index) + "##" + str(elementType),
        *transformList[index].scale,
        0.01,
        format="%.2f",
    )
    if status:
        transformList[index].scale = scale
        shouldUpdateBvh = True

    objectTransformList = sm.currentScene.sceneRenderer.objectTransforms   

    objectTransform = glm.rotate(glm.mat4(1), objectTransformList[objIndex].rotation[0], glm.vec3(1, 0, 0))
    objectTransform = glm.rotate(objectTransform, objectTransformList[objIndex].rotation[1], glm.vec3(0, 1, 0))
    objectTransform = glm.rotate(objectTransform, objectTransformList[objIndex].rotation[2], glm.vec3(0, 0, 1))
    objectTransform = glm.scale(objectTransform, glm.vec3(*objectTransformList[objIndex].scale))

    invObjTrans = glm.inverse(objectTransform)

    objTranslate = glm.translate(glm.mat4(1), glm.vec3(*objectTransformList[objIndex].position))

    objectTransform = objTranslate * objectTransform

    if elementType == 1 and shouldUpdateBvh:
        elementList[index].transform = util.mat4ToFloatArray4Array4(objectTransform)

        for i in range(elementList[index].startingMesh, elementList[index].startingMesh + elementList[index].numMeshes):

            meshTransform = glm.translate(glm.mat4(1), sm.currentScene.sceneRenderer.meshTransforms[i].position)

            meshTransform = glm.rotate(meshTransform, sm.currentScene.sceneRenderer.meshTransforms[i].rotation[0], (1, 0, 0))
            meshTransform = glm.rotate(meshTransform, sm.currentScene.sceneRenderer.meshTransforms[i].rotation[1], (0, 1, 0))
            meshTransform = glm.rotate(meshTransform, sm.currentScene.sceneRenderer.meshTransforms[i].rotation[2], (0, 0, 1))

            meshTransform = glm.scale(meshTransform, sm.currentScene.sceneRenderer.meshTransforms[i].scale)

            sm.currentScene.sceneRenderer.meshes[i].transform = util.mat4ToFloatArray4Array4(
                objectTransform * glm.mat4(meshTransform)
            )


    
    if elementType == 0 and shouldUpdateBvh:
        dp = glm.vec3(pos) - prevPos
        dr = glm.vec3(rot) - prevRot
        ds = glm.vec3(scale) - prevScale

        dp = invObjTrans * dp
        ds = invObjTrans * ds

        pos = glm.vec3(pos) + dp
        scale = glm.vec3(scale) + ds

        meshTransform = objectTransform
        
        meshTransform = glm.translate(meshTransform, pos)
        # meshTransform = glm.rotate(meshTransform, prevRot, )
        meshTransform = glm.rotate(meshTransform, dr[0], glm.normalize(invObjTrans * glm.vec3(1, 0, 0)))
        meshTransform = glm.rotate(meshTransform, dr[1], glm.normalize(invObjTrans * glm.vec3(0, 1, 0)))
        meshTransform = glm.rotate(meshTransform, dr[2], glm.normlize(invObjTrans * glm.vec3(0, 0, 1)))

        meshTransform = glm.rotate(meshTransform, prevRot[0], glm.vec3(1, 0, 0))
        meshTransform = glm.rotate(meshTransform, prevRot[1], glm.vec3(0, 1, 0))
        meshTransform = glm.rotate(meshTransform, prevRot[2], glm.vec3(0, 0, 1))

        meshTransform = glm.scale(meshTransform, scale)

        elementList[index].transform = util.mat4ToFloatArray4Array4(meshTransform)
    
    sm.currentScene.resetFrame()
    if shouldUpdateBvh and sm.currentScene.sceneRenderer.mode == 0:
        sm.currentScene.sceneRenderer.updateBvh()
        sm.currentScene.sendBvhs()

        





        



def objects():

    imgui.begin("Models")
    
    for i in range(len(sm.currentScene.sceneRenderer.objects)):
        if imgui.tree_node(sm.currentScene.sceneRenderer.objectNames[i]):
            imgui.text("Model Transforms")
            drawTransforms(i, 1, i)
            imgui.tree_pop()


    imgui.end()

def drawUI():
    objects()

    sm.currentScene.allocateSSBO()