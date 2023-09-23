import imgui
import deltatime
import sceneManager as sm
import core.GUI.modelDebugUI as modelDebugUI
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
    imgui.text("Frame: " + str(sm.currentScene.sceneRenderer.frameNum))
    imgui.text("Res: " + str(width) + " " + str(height))
    imgui.end()

    if sm.currentScene.camera.lockCam:
        modelDebugUI.drawModel(window)

        imgui.begin("Camera")

        status, blur = imgui.drag_float(
            "blur strength",
            sm.currentScene.camera.blur,
            0.01,
            format="%0.2f",
            min_value=0,
        )

        if status:
            sm.currentScene.camera.blur = blur
            sm.currentScene.sendUniforms()

        status, fov = imgui.drag_float(
            "FOV", sm.currentScene.camera.fov, 0.1, format="%0.1f"
        )

        if status:
            sm.currentScene.camera.fov = fov

        status, numBounces = imgui.drag_int(
            "bounce limit", sm.currentScene.sceneRenderer.numBounces, min_value=1
        )
        numBounces = max(numBounces, 1)

        if status:
            sm.currentScene.sceneRenderer.numBounces = numBounces

        status, raysPerPixel = imgui.drag_int(
            "rays per pixel", sm.currentScene.sceneRenderer.raysPerPixel, min_value=1
        )
        raysPerPixel = max(raysPerPixel, 1)

        if status:
            sm.currentScene.sceneRenderer.raysPerPixel = raysPerPixel
        imgui.end()
