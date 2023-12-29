import sceneManager as sm
import imgui
import os
import core.GUI.drawDirTree as ddt
import time
import threading
import core.GUI.manage_scenes.newScene as newScene
import core.GUI.modelLoadUI as modelLoadUI

prevUiIndex = None


def loadModel(selfIndex, pathInp):
    global prevUiIndex

    if prevUiIndex != selfIndex and prevUiIndex != None:
        return True

    prevUiIndex = selfIndex
    imgui.begin("Select file")

    result = False

    changed, pathInp = imgui.input_text(
        "Select Directory", value=pathInp, buffer_length=400
    )

    condition = lambda ext: ext.lower() == ".obj"

    try:
        os.listdir(os.path.expanduser(pathInp))
        result = ddt.drawDirTree(
            os.path.expanduser(pathInp), condition, sm.currentScene.loadModel
        )

    except FileNotFoundError:
        pass

    if imgui.button("Cancel"):
        result = True

    imgui.end()

    if changed:
        for i in range(len(sm.currentScene.uiManager.jobs)):
            if sm.currentScene.uiManager.jobs[i].id == selfIndex:
                sm.currentScene.uiManager.jobs[i].renderArgs[1] = pathInp

    return result


def loadModelCleanup(selfIndex):
    global prevUiIndex
    sm.currentScene.uiManager.removeJob(selfIndex)
