from glfw.GLFW import *

lastTime = 0


def startTime():
    global lastTime

    lastTime = glfwGetTime()


def deltaTime():
    global lastTime

    currentTime = glfwGetTime()
    dt = currentTime - lastTime

    return dt
