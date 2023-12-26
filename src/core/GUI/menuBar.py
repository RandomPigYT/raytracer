import sceneManager as sm
import imgui
import os
import core.GUI.drawDirTree as ddt
import time
import threading

# import core.GUI.uiManager as uiManager


# name = ""
def newScene(selfIndex, name):
    # global name
    done = False

    imgui.begin("Scene Name")
    changed, name = imgui.input_text("", value=name, buffer_length=400)
    imgui.same_line()
    done = imgui.button("Done")
    imgui.same_line()
    cancel = imgui.button("Cancel")
    imgui.end()

    # sm.currentScene.uiManager.jobs[selfIndex].renderArgs[1] = name
    for i in range(len(sm.currentScene.uiManager.jobs)):
        if sm.currentScene.uiManager.jobs[i].id == selfIndex:
            sm.currentScene.uiManager.jobs[i].renderArgs[1] = name

    if done:
        sm.currentScene.__init__(name, (0, 0, 3), 0, 90, (1920, 1080), 1)
        sm.currentScene.camera.lockCam ^= True

    if cancel:
        return True

    return done


def newSceneCleanup(selfIndex, prevJobs):
    ids = [i.id for i in prevJobs]
    sm.currentScene.uiManager.deactivateAll()
    sm.currentScene.uiManager.activateJobs(ids)


def loadModel(selfIndex, pathInp):
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
    sm.currentScene.uiManager.removeJob(selfIndex)


def renderMenuBar(selfIndex):
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_newScene, selected_newScene = imgui.menu_item(
                "New Scene", "Ctrl+N", False, True
            )

            if clicked_newScene:
                # self.jobs.append(newScene)
                sm.currentScene.uiManager.deactivateAll()
                sm.currentScene.uiManager.activateJobs([selfIndex])

                sm.currentScene.uiManager.addJob(
                    newScene,
                    [sm.currentScene.uiManager.globalJobID, ""],
                    newSceneCleanup,
                    [
                        sm.currentScene.uiManager.globalJobID,
                        [*sm.currentScene.uiManager.jobs],
                    ],
                    True,
                    False,
                )

            clicked_loadScene, selected_LoadScene = imgui.menu_item(
                "Load Scene", "Ctrl+O", False, True
            )

            if clicked_loadScene:
                pass

            clicked_loadModel, selected_loadModel = imgui.menu_item(
                "Load Model", "Ctrl+I", False, True
            )

            if clicked_loadModel:
                sm.currentScene.uiManager.addJob(
                    loadModel,
                    [sm.currentScene.uiManager.globalJobID, "."],
                    loadModelCleanup,
                    [sm.currentScene.uiManager.globalJobID],
                    True,
                    False,
                )

            imgui.end_menu()
    imgui.end_main_menu_bar()

    return False


def menuBarCleanup():
    pass
