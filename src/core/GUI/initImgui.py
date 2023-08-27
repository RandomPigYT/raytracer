import imgui
from imgui.integrations.glfw import GlfwRenderer


def init(window):
    imgui.create_context()

    return GlfwRenderer(window)


