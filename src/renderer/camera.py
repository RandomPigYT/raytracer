from deltatime import *
import sceneManager as sm
from glfw.GLFW import *
import ctypes as ct
import glm
import math


def move():
    dt = deltaTime()

    up = glm.vec3(0, 1, 0)
    right = glm.normalize(glm.cross(glm.vec3(sm.currentScene.camera.direction), up))
    front = glm.normalize(
        glm.vec3(
            sm.currentScene.camera.direction[0], 0, sm.currentScene.camera.direction[2]
        )
    )

    moved = False
    if sm.currentScene.camera.pressedKeys[GLFW_KEY_W]:
        moved = True
        sm.currentScene.camera.position += (
            sm.currentScene.camera.playerSpeed * front * dt
        )

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_S]:
        moved = True
        sm.currentScene.camera.position -= (
            sm.currentScene.camera.playerSpeed * front * dt
        )

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_D]:
        moved = True
        sm.currentScene.camera.position += (
            sm.currentScene.camera.playerSpeed * right * dt
        )

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_A]:
        moved = True
        sm.currentScene.camera.position -= (
            sm.currentScene.camera.playerSpeed * right * dt
        )

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_SPACE]:
        moved = True
        sm.currentScene.camera.position += sm.currentScene.camera.playerSpeed * up * dt

    if sm.currentScene.camera.pressedKeys[GLFW_KEY_LEFT_SHIFT]:
        moved = True
        sm.currentScene.camera.position -= sm.currentScene.camera.playerSpeed * up * dt

    if moved:
        sm.currentScene.resetFrame()
    sm.currentScene.sendUniforms()


def lookAround(dx, dy):
    sm.currentScene.camera.yaw += dx * sm.currentScene.camera.sensitivity
    sm.currentScene.camera.pitch -= dy * sm.currentScene.camera.sensitivity

    if sm.currentScene.camera.pitch > 89.0:
        sm.currentScene.camera.pitch = 89.0

    if sm.currentScene.camera.pitch < -89.0:
        sm.currentScene.camera.pitch = -89.0

    sm.currentScene.camera.direction[0] = math.cos(
        math.radians(sm.currentScene.camera.yaw)
    ) * math.cos(math.radians(sm.currentScene.camera.pitch))
    sm.currentScene.camera.direction[1] = math.sin(
        math.radians(sm.currentScene.camera.pitch)
    )
    sm.currentScene.camera.direction[2] = math.sin(
        math.radians(sm.currentScene.camera.yaw)
    ) * math.cos(math.radians(sm.currentScene.camera.pitch))

    sm.currentScene.camera.direction = glm.normalize(sm.currentScene.camera.direction)
