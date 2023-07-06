from deltatime import *
import sceneManager as sm
from glfw.GLFW import *
import ctypes as ct
import glm



def move():

    dt = deltaTime()
    
    up = glm.vec3(0, 1, 0)
    right = glm.normalize(glm.cross(up, glm.vec3(sm.currentScene.cameraDirection)))
    front = glm.normalize(glm.vec3(sm.currentScene.cameraDirection[0], 0, sm.currentScene.cameraDirection[2]))

    if sm.currentScene.pressedKeys[GLFW_KEY_W]:
        sm.currentScene.cameraPos += sm.currentScene.playerSpeed * front * dt

    if sm.currentScene.pressedKeys[GLFW_KEY_S]:
        sm.currentScene.cameraPos -= sm.currentScene.playerSpeed * front * dt

    if sm.currentScene.pressedKeys[GLFW_KEY_D]:
        sm.currentScene.cameraPos += sm.currentScene.playerSpeed * right * dt

    if sm.currentScene.pressedKeys[GLFW_KEY_A]:
        sm.currentScene.cameraPos -= sm.currentScene.playerSpeed * right * dt

    sm.currentScene.sendUniforms()

        

def lookAround(dy, dx):



