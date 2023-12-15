import sceneManager as sm
import imgui
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
    print(ids)
    sm.currentScene.uiManager.deactivateAll()
    sm.currentScene.uiManager.activateJobs(ids)


def renderMenuBar(selfIndex):
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_newScene, selected_newScene = imgui.menu_item(
                "New Scene", 'Ctrl+N', False, True
            )

            if clicked_newScene:
                # self.jobs.append(newScene)
                sm.currentScene.uiManager.deactivateAll()

                sm.currentScene.uiManager.addJob(
                    newScene, 
                    [sm.currentScene.uiManager.globalJobID, ""],
                    newSceneCleanup,
                    [sm.currentScene.uiManager.globalJobID, [*sm.currentScene.uiManager.jobs]],
                    True,
                    False
                )


            imgui.end_menu()
    imgui.end_main_menu_bar()

    return False

def menuBarCleanup():
    pass