from deltatime import *
import sceneManager as sm
from glfw.GLFW import *
import ctypes as ct
import glm



def move():

    dt = deltaTime()
    
    up = glm.vec3(0, 1, 0)
    right = glm.normalize(glm.cross(glm.vec3(sm.currentScene.camera.direction), up))
    front = glm.normalize(glm.vec3(sm.currentScene.camera.direction[0], 0, sm.currentScene.camera.direction[2]))


    if sm.currentScene.camera.pressedKeys[GLFW_KEY_W]:
        sm.currentScene.camera.position += sm.currentScene.camera.playerSpeed * front * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_S]:
        sm.currentScene.camera.position -= sm.currentScene.camera.playerSpeed * front * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_D]:
        sm.currentScene.camera.position += sm.currentScene.camera.playerSpeed * right * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_A]:
        sm.currentScene.camera.position -= sm.currentScene.camera.playerSpeed * right * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_SPACE]:
        sm.currentScene.camera.position += sm.currentScene.camera.playerSpeed * up * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_LEFT_SHIFT]:
        sm.currentScene.camera.position -= sm.currentScene.camera.playerSpeed * up * dt


    if sm.currentScene.camera.pressedKeys[GLFW_KEY_L]:
        sm.currentScene.camera.direction += right * sm.currentScene.camera.sensitivity * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_J]:
        sm.currentScene.camera.direction -= right * sm.currentScene.camera.sensitivity * dt
    
    if sm.currentScene.camera.pressedKeys[GLFW_KEY_I]:
        sm.currentScene.camera.direction += up * sm.currentScene.camera.sensitivity * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_K]:
        sm.currentScene.camera.direction -= up * sm.currentScene.camera.sensitivity * dt

    sm.currentScene.sendUniforms()

        

def lookAround():
    pass



