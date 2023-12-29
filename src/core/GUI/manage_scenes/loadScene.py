import sceneManager as sm
import core.save_and_load.load as load
import mysql.connector
import core.GUI.enterText as enterText
import imgui

def loadScene(selfIndex):
    wrapper = sm.currentScene.sqlWrapper

    wrapper.execute("select * from scenes")
    scenes = wrapper.fetch()

    done = False

    imgui.begin("Load Scene")
    
    for i in scenes:
        if done := imgui.button(i[0]):
            sm.currentScene.__init__(i[0], (0, 0, 3), 0, 90, (1920, 1080), 1)
            sm.currentScene.camera.lockCam ^= True
            sm.currentScene.saved = True
            load.load(i[0])

    imgui.separator()

    done = imgui.button("Cancel")

    imgui.end()

    return done

def loadSceneCleanup(selfIndex, prevJobs):
    ids = [i.id for i in prevJobs]
    sm.currentScene.uiManager.removeJob(selfIndex)
    sm.currentScene.uiManager.activateJobs(ids)