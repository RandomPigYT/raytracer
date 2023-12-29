import sceneManager as sm
import imgui
import os
import core.GUI.drawDirTree as ddt
import time
import threading
import core.GUI.manage_scenes.newScene as newScene
import core.GUI.modelLoadUI as modelLoadUI
import core.GUI.manage_scenes.saveScene as saveScene
import core.GUI.manage_scenes.loadScene as loadScene
import core.GUI.manage_scenes.manageScenes as manageScenes


def renderMenuBar(selfIndex):
    def loadModelUiDelFunc():
        modelLoadUI.prevUiIndex = None

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
                sm.currentScene.uiManager.deactivateAll()

                sm.currentScene.uiManager.addJob(
                    loadScene.loadScene,
                    [sm.currentScene.uiManager.globalJobID],
                    loadScene.loadSceneCleanup,
                    [
                        sm.currentScene.uiManager.globalJobID,
                        [*sm.currentScene.uiManager.jobs],
                    ],
                    True,
                    False,
                )

            clicked_manageScnenes, selected_manageScnenes = imgui.menu_item(
                "Manage Scenes", "", False, True
            )

            if clicked_manageScnenes:
                sm.currentScene.uiManager.deactivateAll()

                sm.currentScene.uiManager.addJob(
                    manageScenes.manage,
                    [sm.currentScene.uiManager.globalJobID],
                    manageScenes.manageScenesCleanup,
                    [
                        sm.currentScene.uiManager.globalJobID,
                        [*sm.currentScene.uiManager.jobs],
                    ],
                    True,
                    False,
                )

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
                    loadModelUiDelFunc,
                    [],
                )

            imgui.end_menu()
    imgui.end_main_menu_bar()

    return False


def menuBarCleanup():
    pass
