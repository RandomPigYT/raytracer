import imgui
import sceneManager as sm
import ctypes as ct
import glm
import util
import math
import core.GUI.delete as delete


def enterName(label, name):
    imgui.begin(label)
    changed, name = imgui.input_text("", value=name, buffer_length=400)
    imgui.same_line()
    done = imgui.button("Done")
    imgui.same_line()
    cancel = imgui.button("Cancel")

    if done and name == "":
        cancel = True
        done = False
    imgui.end()

    return name, done, cancel
