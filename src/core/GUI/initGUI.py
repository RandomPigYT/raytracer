# import sceneManager as sm
import core.GUI.menuBar as mb
import core.GUI.guiElements as gElem


def initGUI(s):
    s.menuBarIndex = s.uiManager.addJob(
        mb.renderMenuBar,
        [s.uiManager.globalJobID],
        mb.menuBarCleanup,
        [],
        True,
        True,
    )

    # self.sceneElementsIndex = gElem.elements(None)
    s.sceneElementsIndex = s.uiManager.addJob(
        gElem.elements,
        [None],
        None,
        [None],
        False,
        True
    )
