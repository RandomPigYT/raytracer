import sceneManager as sm
import imgui
import os
import core.GUI.drawDirTree as ddt
import time
import threading
import core.GUI.manage_scenes.newScene as newScene
import core.GUI.modelLoadUI as modelLoadUI
import core.GUI.manage_scenes.saveScene as saveScene


def renderMenuBar(selfIndex):
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_newScene, selected_newScene = imgui.menu_item(
                "New Scene", "Ctrl+N", False, True
            )

            if clicked_newScene:
                sm.currentScene.uiManager.deactivateAll()

                sm.currentScene.uiManager.addJob(
                    newScene.newScene,
                    [sm.currentScene.uiManager.globalJobID, ""],
                    newScene.newSceneCleanup,
                    [
                        sm.currentScene.uiManager.globalJobID,
                        [*sm.currentScene.uiManager.jobs],
                    ],
                    True,
                    False,
                )
            
            clicked_saveScene, selected_saveScene = imgui.menu_item(
                "Save", "Ctrl+S", False, True
            )

            if clicked_saveScene:
                saveScene.saveScene()
            
            clicked_saveSceneAs, selected_saveSceneAs = imgui.menu_item(
                "Save As", "Ctrl+S", False, True
            )

            if clicked_saveSceneAs:
                saveScene.addSaveAsJob(False)
            

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
                    modelLoadUI.loadModel,
                    [sm.currentScene.uiManager.globalJobID, "."],
                    modelLoadUI.loadModelCleanup,
                    [sm.currentScene.uiManager.globalJobID],
                    True,
                    False,
                )

            imgui.end_menu()
    imgui.end_main_menu_bar()

    return False


def menuBarCleanup():
    pass
