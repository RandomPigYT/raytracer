from deltatime import *
import sceneManager as sm
from glfw.GLFW import *
import ctypes as ct
import glm



def move():

    dt = deltaTime()
    
    up = glm.vec3(0, 1, 0)
    right = glm.normalize(glm.cross(up, glm.vec3(sm.currentScene.camera.direction)))
    front = glm.normalize(glm.vec3(sm.currentScene.camera.direction[0], 0, sm.currentScene.camera.direction[2]))

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_W]:
        sm.currentScene.camera.position += sm.currentScene.playerSpeed * front * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_S]:
        sm.currentScene.camera.position -= sm.currentScene.playerSpeed * front * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_D]:
        sm.currentScene.camera.position += sm.currentScene.playerSpeed * right * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_A]:
        sm.currentScene.camera.position -= sm.currentScene.playerSpeed * right * dt

    sm.currentScene.sendUniforms()

        

def lookAround(dy, dx):
    pass



