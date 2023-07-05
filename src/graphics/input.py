from glfw.GLFW import *
import renderer.camera as camera


def keyCallback(window, key, scancode, action, mods):

    camera.move(key, action)

    


