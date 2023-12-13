import core.scene as scene
import sceneManager as sm
import imgui

def menu_newScene():
    newScene = scene.Scene("NewScene", (0, 0, 0), 0, 90, (1920, 1080), 0)
    sm.currentScene = newScene
    newScene.loadModel("models/cube.obj")
    
    io = imgui.get_io()
    io.config_flags ^= imgui.CONFIG_NO_MOUSE
    # print("hi", len(sm.currentScene.sceneRenderer.vertices))
    # sm.currentScene.allocateSSBO()
    
    
    

def menu_loadScene():
    pass

def menu_manageScenes():
    pass