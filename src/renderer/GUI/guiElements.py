import imgui
import deltatime
import sceneManager as sm
import renderer.GUI.modelDebugUI as modelDebugUI
import OpenGL.GL as gl

frameNum = 0
avgFPS = 0

def elements(window):
    global frameNum, avgFPS
    
    frameNum += 1

    dt = deltatime.deltaTime()

    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]

    fps = 1 / dt
    avgFPS = ((frameNum - 1) * avgFPS + (fps)) / frameNum
    
    imgui.begin("FPS")
    imgui.text(str("FPS: " + str(fps)))
    imgui.text(str("Avg FPS: " + str(avgFPS)))
    imgui.text("Frame: " + str(sm.currentScene.frameNum))
    imgui.text("Res: " + str(width) + " " + str(height))

    imgui.text("Colour " + str(sm.currentScene.materials[0].kd[0]) +" "+ str(sm.currentScene.materials[0].kd[1])+ " " +str(sm.currentScene.materials[0].kd[2]))
    imgui.end()

    if sm.currentScene.camera.lockCam:
        modelDebugUI.drawSphereUI(window)


