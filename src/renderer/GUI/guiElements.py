import imgui
import deltatime
import sceneManager as sm
import renderer.GUI.sphereControls as sphCont

frameNum = 0
avgFPS = 0

def elements(window):
    global frameNum, avgFPS
    
    frameNum += 1

    dt = deltatime.deltaTime()


    fps = 1 / dt
    avgFPS = ((frameNum - 1) * avgFPS + (fps)) / frameNum
    
    imgui.begin("FPS")
    imgui.text(str("FPS: " + str(fps)))
    imgui.text(str("Avg FPS: " + str(avgFPS)))
    imgui.text("Frame: " + str(frameNum))
    imgui.end()

    sphCont.drawSphereUI(window)


