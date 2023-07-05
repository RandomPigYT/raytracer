from deltatime import *
import sceneManager as sm
from glfw.GLFW import *
import ctypes as ct
import glm



def move(key: int, action: int):

    # Remember to change this code after implementing camera rays
    

    if key == GLFW_KEY_W and (action == GLFW_REPEAT or action == GLFW_PRESS):
        direction = glm.vec3(sm.currentScene.cameraDirection[0], 0, sm.currentScene.cameraDirection[2])
        position = glm.vec3(*sm.currentScene.cameraPos)

        sm.currentScene.cameraPos = (ct.c_float * 3)(*glm.add(glm.mul(direction, -sm.currentScene.playerSpeed * deltaTime()), position))


        
    if key == GLFW_KEY_S and (action == GLFW_REPEAT or action == GLFW_PRESS):
        direction = glm.vec3(sm.currentScene.cameraDirection[0], 0, sm.currentScene.cameraDirection[2])
        position = glm.vec3(*sm.currentScene.cameraPos)

        sm.currentScene.cameraPos = (ct.c_float * 3)(*glm.add(glm.mul(direction, sm.currentScene.playerSpeed * deltaTime()), position))
        
    if key == GLFW_KEY_D and (action == GLFW_REPEAT or action == GLFW_PRESS):
        direction = glm.cross(-glm.vec3(sm.currentScene.cameraDirection[0], 0, sm.currentScene.cameraDirection[2]), glm.vec3(0, 1, 0))
        position = glm.vec3(*sm.currentScene.cameraPos)

        sm.currentScene.cameraPos = (ct.c_float * 3)(*glm.add(glm.mul(direction, sm.currentScene.playerSpeed * deltaTime()), position))

    if key == GLFW_KEY_A and (action == GLFW_REPEAT or action == GLFW_PRESS):
        direction = glm.cross(-glm.vec3(sm.currentScene.cameraDirection[0], 0, -sm.currentScene.cameraDirection[2]), glm.vec3(0, 1, 0))
        position = glm.vec3(*sm.currentScene.cameraPos)

        sm.currentScene.cameraPos = (ct.c_float * 3)(*glm.add(glm.mul(direction, sm.currentScene.playerSpeed * deltaTime()), position))
    sm.currentScene.sendUniforms()

        




