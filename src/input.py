from glfw.GLFW import *
import core.camera as camera
import sceneManager as sm
import glm
import ctypes as ct
import imgui


def keyCallback(window, key, scancode, action, mods):
    if action != GLFW_RELEASE and not sm.currentScene.camera.lockCam:
        sm.currentScene.camera.pressedKeys[key] = True

    elif action == GLFW_RELEASE and not sm.currentScene.camera.lockCam:
        sm.currentScene.camera.pressedKeys[key] = False

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        sm.currentScene.camera.lockCam ^= True
        io = imgui.get_io()
        io.config_flags ^= imgui.CONFIG_NO_MOUSE

        if sm.currentScene.camera.lockCam:
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)
            sm.currentScene.uiManager.activateDefault()

        else:
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
            sm.currentScene.uiManager.deactivateAll()

    if key == GLFW_KEY_BACKSPACE and action == GLFW_PRESS:
        io = imgui.get_io()
        io.keys_down[io.key_map[imgui.KEY_BACKSPACE]] = 1

    if key == GLFW_KEY_BACKSPACE and action == GLFW_RELEASE:
        io = imgui.get_io()
        io.keys_down[io.key_map[imgui.KEY_BACKSPACE]] = 0


def mouseButtonCallback(window, button, action, mods):
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        sm.currentScene.camera.mouseHeldRight = True
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE:
        sm.currentScene.camera.mouseHeldRight = False
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)


def mousePosCallback(window, xpos, ypos):
    prevPos = sm.currentScene.camera.prevMousePos
    sm.currentScene.camera.prevMousePos = (2 * ct.c_float)(xpos, ypos)

    if not sm.currentScene.camera.lockCam:
        dx = xpos - prevPos[0]
        dy = ypos - prevPos[1]

        camera.lookAround(dx, dy)

        sm.currentScene.resetFrame()
