import imgui
import sceneManager as sm
import ctypes as ct
import glm
import util
import math
import core.GUI.delete as delete

def filterChars(callbackData):
    callbackData.event_char = callbackData.event_char.lower()

    if not callbackData.user_data[0] and callbackData.event_char == ' ':
        return 1
    
    if not callbackData.user_data[1] and not callbackData.event_char.isalnum():
        if callbackData.event_char != '_':
            return 1



def enterName(label, name, allowSpace=True, allowSpecial=True):

    flags = 0 

    flags |= imgui.INPUT_TEXT_CALLBACK_CHAR_FILTER
    userData = (allowSpace, allowSpecial)

    imgui.begin(label)
    changed, name = imgui.input_text("", value=name, buffer_length=400, flags=flags, callback=filterChars, user_data=userData)
    imgui.same_line()
    done = imgui.button("Done")
    imgui.same_line()
    cancel = imgui.button("Cancel")

    if done and name == "":
        cancel = True
        done = False
    imgui.end()

    return name, done, cancel
