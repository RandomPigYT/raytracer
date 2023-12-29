import imgui
import deltatime
import sceneManager as sm
import core.GUI.modelDebugUI as modelDebugUI
import OpenGL.GL as gl
import core.GUI.modelUI as modelUI
import core.save_and_load.save as save
import core.save_and_load.load as load


def docking_space(name: str):
    flags = (
        imgui.WINDOW_MENU_BAR
        | imgui.WINDOW_NO_DOCKING
        # | imgui.WINDOW_NO_BACKGROUND
        | imgui.WINDOW_NO_TITLE_BAR
        | imgui.WINDOW_NO_COLLAPSE
        | imgui.WINDOW_NO_RESIZE
        | imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
        | imgui.WINDOW_NO_NAV_FOCUS
    )

    viewport = imgui.get_main_viewport()
    x, y = viewport.pos
    w, h = viewport.size
    imgui.set_next_window_position(x, y)
    imgui.set_next_window_size(w, h)
    # imgui.set_next_window_viewport(viewport.id)
    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)

    # When using ImGuiDockNodeFlags_PassthruCentralNode, DockSpace() will render our background and handle the pass-thru hole, so we ask Begin() to not render a background.
    # local window_flags = self.window_flags
    # if bit.band(self.dockspace_flags, ) ~= 0 then
    #     window_flags = bit.bor(window_flags, const.ImGuiWindowFlags_.NoBackground)
    # end

    # Important: note that we proceed even if Begin() returns false (aka window is collapsed).
    # This is because we want to keep our DockSpace() active. If a DockSpace() is inactive,
    # all active windows docked into it will lose their parent and become undocked.
    # We cannot preserve the docking relationship between an active window and an inactive docking, otherwise
    # any change of dockspace/settings would lead to windows being stuck in limbo and never being visible.
    imgui.set_next_window_bg_alpha(0.0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
    imgui.begin(name, None, flags)
    imgui.pop_style_var()
    imgui.pop_style_var(2)

    # DockSpace
    dockspace_id = imgui.get_id(name)
    imgui.dockspace(dockspace_id, (0, 0), imgui.DOCKNODE_PASSTHRU_CENTRAL_NODE)

    imgui.end()


frameNum = 0
avgFPS = 0


def elements(window):
    global frameNum, avgFPS

    docking_space("Docking space")

    frameNum += 1

    dt = deltatime.deltaTime()

    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    width = viewport[2]
    height = viewport[3]

    fps = 1 / dt
    # avgFPS = ((frameNum - 1) * avgFPS + (fps)) / frameNum

    imgui.begin("FPS")
    imgui.text(str("FPS: " + str(fps)))
    imgui.text("Frame: " + str(sm.currentScene.sceneRenderer.frameNum))
    imgui.text("Res: " + str(width) + " " + str(height))
    imgui.end()

    # modelDebugUI.drawModel(window)
    modelUI.drawUI()

    imgui.begin("Scene")

    imgui.text(
        "Scene name: "
        + (sm.currentScene.name if sm.currentScene.name != "" else "(Untitled)")
    )

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

    if imgui.button("Toggle Raytracy"):
        sm.currentScene.resetFrame()
        sm.currentScene.sceneRenderer.updateBvh()
        sm.currentScene.sendBvhs()
        sm.currentScene.sceneRenderer.mode ^= 1

    if imgui.button("Refresh Scene"):
        sm.currentScene.allocateSSBO()
    imgui.end()
