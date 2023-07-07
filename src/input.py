from glfw.GLFW import *
import renderer.camera as camera
import sceneManager as sm
import glm


def keyCallback(window, key, scancode, action, mods):

    if action != GLFW_RELEASE:
        sm.currentScene.camera.pressedKeys[key] = True

    elif action == GLFW_RELEASE:
        sm.currentScene.camera.pressedKeys[key] = False
    
    


