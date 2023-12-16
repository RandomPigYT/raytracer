import sceneManager as sm
import imgui
import os

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

    sm.currentScene.uiManager.jobs[selfIndex].renderArgs[1] = name

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

def drawDirTree(path):
    dirs = [i for i in os.listdir(path) if not os.path.isfile(os.path.join(path, i))]
    files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]

    for i in dirs:
        if imgui.tree_node(i):
            if drawDirTree(os.path.join(path, i)):
                imgui.tree_pop()
                return True
            imgui.tree_pop()

    for i in files:
        if os.path.splitext(i)[1].lower() == ".obj":
            if imgui.button(i):
                sm.currentScene.loadModel(os.path.join(path, i))
                return True
    
    return False








def loadModel(selfIndex):
    imgui.begin("Select file")
    result = drawDirTree("/")
    imgui.end()

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
                    [sm.currentScene.uiManager.globalJobID],
                    loadModelCleanup,
                    [sm.currentScene.uiManager.globalJobID],
                    True,
                    False
                )


            imgui.end_menu()
    imgui.end_main_menu_bar()

    return False


def menuBarCleanup():
    pass
