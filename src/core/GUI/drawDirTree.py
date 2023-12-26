import imgui
import os
import sceneManager as sm


def drawDirTree(path, condition, callback):
    try:
        dirs = [
            i for i in os.listdir(path) if not os.path.isfile(os.path.join(path, i))
        ]
        files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]

    except PermissionError:
        return False

    for i in dirs:
        if imgui.tree_node(i):
            if drawDirTree(os.path.join(path, i), condition, callback):
                imgui.tree_pop()
                return True
            imgui.tree_pop()

    for i in files:
        if condition(os.path.splitext(i)[1]):
            if imgui.button(i):
                callback(os.path.join(path, i))
                return True

    return False
