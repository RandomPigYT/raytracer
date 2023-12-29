import imgui
import sceneManager as sm
import ctypes as ct
import glm
import util
import math
import core.GUI.delete as delete
import core.GUI.enterText as enterText


def createMaterial(selfIndex, name):
    name, done, cancel = enterText.enterName("Material Name", name)

    # sm.currentScene.uiManager.jobs[selfIndex].renderArgs[1] = name
    for i in range(len(sm.currentScene.uiManager.jobs)):
        if sm.currentScene.uiManager.jobs[i].id == selfIndex:
            sm.currentScene.uiManager.jobs[i].renderArgs[1] = name

    if done:
        # if name in sm.currentScene.sceneRenderer.matNames:
        #     name += "(" + str(sm.currentScene.sceneRenderer.matNames.count(name)) + ")"

        sm.currentScene.sceneRenderer.matNames.append(name + '_' + str(len(sm.currentScene.sceneRenderer.matNames)))

        newMatIndex = len(sm.currentScene.sceneRenderer.materials)
        sm.currentScene.sceneRenderer.materials = util.realloc(
            sm.currentScene.sceneRenderer.materials,
            len(sm.currentScene.sceneRenderer.materials) + 1,
        )
        matArray = sm.currentScene.sceneRenderer.materials  # To reduce verbosity
        matArray[newMatIndex].albedo = (4 * ct.c_float)(
            162.0 / 255.0, 164.0 / 255.0, 165.0 / 255.0, 0.0
        )
        matArray[newMatIndex].opacity = 1.0
        matArray[newMatIndex].textureID = -1
        matArray[newMatIndex].roughnessMapID = -1
        matArray[newMatIndex].metallicMapID = -1
        matArray[newMatIndex].emissiveMapID = -1
        matArray[newMatIndex].normalMapID = -1
        matArray[newMatIndex].opacityMapID = -1
        matArray[newMatIndex].specularMapID = -1
        matArray[newMatIndex].displacementMapID = -1

    if cancel:
        return True

    return done


def textureCombo(valuePtr: ct.POINTER(ct.c_int32), label, num):
    selected = valuePtr.contents.value if valuePtr.contents.value != 0 else -1
    with imgui.begin_combo(
        label + "##" + str(num),
        sm.currentScene.sceneRenderer.textures[1][selected]
        if selected != -1
        else "Select Texture",
    ) as combo:
        if combo.opened:
            for i, tex in enumerate(sm.currentScene.sceneRenderer.textures[1][1:]):
                isSelected = i + 1 == selected
                if imgui.selectable(tex, isSelected)[0]:
                    valuePtr.contents.value = i + 1

                if isSelected:
                    imgui.set_item_default_focus()

            isSelected = -1 == selected
            if imgui.selectable("No Texture", isSelected)[0]:
                valuePtr.contents.value = -1


def drawMaterialControls(materialID, num):
    status, albedo = imgui.color_edit3(
        "albedo##" + str(num),
        *sm.currentScene.sceneRenderer.materials[materialID].albedo,
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].albedo = (*albedo, 1)

    status, emission = imgui.drag_float3(
        "emission##" + str(num),
        *sm.currentScene.sceneRenderer.materials[materialID].emission[:-1],
        0.01,
        format="%0.2f",
        min_value=0,
        max_value=math.inf,
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].emission = (*emission, 1)

    status, op = imgui.drag_float(
        "opacity##" + str(num),
        sm.currentScene.sceneRenderer.materials[materialID].opacity,
        0.001,
        format="%0.3f",
        min_value=0,
        max_value=1,
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].opacity = op

    status, ref = imgui.drag_float3(
        "refractive index##" + str(num),
        *(sm.currentScene.sceneRenderer.materials[materialID].refractiveIndex[:-1]),
        0.001,
        format="%0.3f",
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].refractiveIndex = ref

    status, roughness = imgui.drag_float(
        "roughness##" + str(num),
        sm.currentScene.sceneRenderer.materials[materialID].roughness[0],
        0.001,
        format="%0.3f",
        min_value=0,
        max_value=1,
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].roughness[0] = roughness

    status, metallic = imgui.drag_float(
        "metallic##" + str(num),
        sm.currentScene.sceneRenderer.materials[materialID].metallic,
        0.001,
        format="%0.3f",
        min_value=0,
        max_value=1,
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].metallic = metallic

    status, reflectance = imgui.drag_float(
        "reflectance##" + str(num),
        sm.currentScene.sceneRenderer.materials[materialID].reflectance,
        0.001,
        format="%0.3f",
        min_value=0,
        max_value=1,
    )
    if status:
        sm.currentScene.sceneRenderer.materials[materialID].reflectance = reflectance

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].textureID
    )
    textureCombo(ct.pointer(tempTexID), "Texture", num)
    sm.currentScene.sceneRenderer.materials[materialID].textureID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].roughnessMapID
    )
    textureCombo(ct.pointer(tempTexID), "Roughness Map", num)
    sm.currentScene.sceneRenderer.materials[materialID].roughnessMapID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].metallicMapID
    )
    textureCombo(ct.pointer(tempTexID), "Metallic Map", num)
    sm.currentScene.sceneRenderer.materials[materialID].metallicMapID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].emissiveMapID
    )
    textureCombo(ct.pointer(tempTexID), "Emissive Map", num)
    sm.currentScene.sceneRenderer.materials[materialID].emissiveMapID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].normalMapID
    )
    textureCombo(ct.pointer(tempTexID), "Normal Map", num)
    sm.currentScene.sceneRenderer.materials[materialID].normalMapID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].opacityMapID
    )
    textureCombo(ct.pointer(tempTexID), "Opacity Map", num)
    sm.currentScene.sceneRenderer.materials[materialID].opacityMapID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].specularMapID
    )
    textureCombo(ct.pointer(tempTexID), "Specular Map", num)
    sm.currentScene.sceneRenderer.materials[materialID].specularMapID = tempTexID.value

    tempTexID = ct.c_int32(
        sm.currentScene.sceneRenderer.materials[materialID].displacementMapID
    )
    textureCombo(ct.pointer(tempTexID), "Displacement Map", num)
    sm.currentScene.sceneRenderer.materials[
        materialID
    ].displacementMapID = tempTexID.value


def materials():
    imgui.begin("Materials")

    for i in range(1, len(sm.currentScene.sceneRenderer.materials)):
        if imgui.tree_node(sm.currentScene.sceneRenderer.matNames[i]):
            drawMaterialControls(i, i)
            imgui.tree_pop()
        if imgui.begin_popup_context_item("Edit Materials##" + str(i)).opened:
            if imgui.button("Delete Material##" + str(i)):
                delete.deleteMaterial(i)
                imgui.end_popup()
                imgui.end()
                return
            imgui.end_popup()

    cleanupNewMat = lambda selfIndex: sm.currentScene.uiManager.removeJob(selfIndex)

    if imgui.button("Create Material"):
        sm.currentScene.uiManager.addJob(
            createMaterial,
            [sm.currentScene.uiManager.globalJobID, ""],
            cleanupNewMat,
            [sm.currentScene.uiManager.globalJobID],
            True,
            False,
        )

    sm.currentScene.allocateSSBO()
    sm.currentScene.resetFrame()
    imgui.end()


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

    objectTransform = glm.rotate(
        glm.mat4(1), objectTransformList[objIndex].rotation[0], glm.vec3(1, 0, 0)
    )
    objectTransform = glm.rotate(
        objectTransform, objectTransformList[objIndex].rotation[1], glm.vec3(0, 1, 0)
    )
    objectTransform = glm.rotate(
        objectTransform, objectTransformList[objIndex].rotation[2], glm.vec3(0, 0, 1)
    )
    objectTransform = glm.scale(
        objectTransform, glm.vec3(*objectTransformList[objIndex].scale)
    )

    invObjTrans = glm.inverse(objectTransform)

    objTranslate = glm.translate(
        glm.mat4(1), glm.vec3(*objectTransformList[objIndex].position)
    )

    objectTransform = objTranslate * objectTransform

    if elementType == 1 and shouldUpdateBvh:
        elementList[index].transform = util.mat4ToFloatArray4Array4(objectTransform)

        for i in range(
            elementList[index].startingMesh,
            elementList[index].startingMesh + elementList[index].numMeshes,
        ):
            meshTransform = glm.translate(
                glm.mat4(1), sm.currentScene.sceneRenderer.meshTransforms[i].position
            )

            meshTransform = glm.rotate(
                meshTransform,
                sm.currentScene.sceneRenderer.meshTransforms[i].rotation[0],
                (1, 0, 0),
            )
            meshTransform = glm.rotate(
                meshTransform,
                sm.currentScene.sceneRenderer.meshTransforms[i].rotation[1],
                (0, 1, 0),
            )
            meshTransform = glm.rotate(
                meshTransform,
                sm.currentScene.sceneRenderer.meshTransforms[i].rotation[2],
                (0, 0, 1),
            )

            meshTransform = glm.scale(
                meshTransform, sm.currentScene.sceneRenderer.meshTransforms[i].scale
            )

            sm.currentScene.sceneRenderer.meshes[
                i
            ].transform = util.mat4ToFloatArray4Array4(
                objectTransform * glm.mat4(meshTransform)
            )

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

            showMeshes, _ = imgui.collapsing_header("Meshes")
            if showMeshes:
                for j in range(
                    sm.currentScene.sceneRenderer.objects[i].startingMesh,
                    sm.currentScene.sceneRenderer.objects[i].startingMesh
                    + sm.currentScene.sceneRenderer.objects[i].numMeshes,
                ):
                    selected = sm.currentScene.sceneRenderer.meshes[j].materialID
                    if imgui.tree_node(sm.currentScene.sceneRenderer.meshNames[j]):
                        with imgui.begin_combo(
                            "Material##%d##%d" % (i, j),
                            sm.currentScene.sceneRenderer.matNames[
                                sm.currentScene.sceneRenderer.meshes[j].materialID
                            ],
                        ) as combo:
                            if combo.opened:
                                for k, mat in enumerate(
                                    sm.currentScene.sceneRenderer.matNames
                                ):
                                    isSelected = k == selected
                                    if imgui.selectable(mat, isSelected)[0]:
                                        sm.currentScene.sceneRenderer.meshes[
                                            j
                                        ].materialID = k

                                    if isSelected:
                                        imgui.set_item_default_focus()

                        imgui.tree_pop()
            imgui.tree_pop()

        if imgui.begin_popup_context_item("Edit Models##" + str(i)).opened:
            if imgui.button("Delete Model##" + str(i)):
                delete.deleteObject(i)
                imgui.end_popup()
                imgui.end()
                return
            imgui.end_popup()

    imgui.end()


def drawUI():
    objects()
    materials()

    sm.currentScene.allocateSSBO()
