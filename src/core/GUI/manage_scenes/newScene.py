import sceneManager as sm
import imgui
import os
import core.GUI.drawDirTree as ddt
import time
import threading
import core.GUI.enterText as enterText

# import core.GUI.uiManager as uiManager


# name = ""
def newScene(selfIndex, name):
    name, done, cancel = enterText.enterName("Scene Name", name)

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
    sm.currentScene.uiManager.removeJob(selfIndex)
    sm.currentScene.uiManager.activateJobs(ids)
