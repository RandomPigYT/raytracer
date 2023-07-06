from glfw.GLFW import *
import renderer.camera as camera
import sceneManager as sm


def keyCallback(window, key, scancode, action, mods):

    if action != GLFW_RELEASE:
        sm.currentScene.pressedKeys[key] = True

    elif action == GLFW_RELEASE:
        sm.currentScene.pressedKeys[key] = False
    
    

    


