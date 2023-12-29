import sceneManager as sm
import core.save_and_load.save as save
import mysql.connector
import core.GUI.enterText as enterText


def saveSceneAs(selfIndex, name, nameConflict):
    wrapper = sm.currentScene.sqlWrapper

    label = "Save As" + (" (Conflicting names)" if nameConflict else "")
    name, done, cancel = enterText.enterName(label, name, False, False)

    for i in range(len(sm.currentScene.uiManager.jobs)):
        if sm.currentScene.uiManager.jobs[i].id == selfIndex:
            sm.currentScene.uiManager.jobs[i].renderArgs[1] = name

    if done:
        sm.currentScene.name = name
        try:
            wrapper.execute(
                "insert into scenes values('{}')".format(sm.currentScene.name)
            )
            sm.currentScene.saved = True
        except mysql.connector.errors.IntegrityError:
            for i in range(len(sm.currentScene.uiManager.jobs)):
                if sm.currentScene.uiManager.jobs[i].id == selfIndex:
                    sm.currentScene.uiManager.jobs[i].renderArgs[1] = ""
                    sm.currentScene.uiManager.jobs[i].renderArgs[2] = True
            return False
        save.save()

    if cancel:
        return True

    # sm.currentScene.saved = True
    return done


def saveSceneAsCleanup(selfIndex, prevJobs):
    ids = [i.id for i in prevJobs]
    sm.currentScene.uiManager.removeJob(selfIndex)
    sm.currentScene.uiManager.activateJobs(ids)


def addSaveAsJob(nameConflict):
    sm.currentScene.uiManager.deactivateAll()
    sm.currentScene.uiManager.addJob(
        saveSceneAs,
        [sm.currentScene.uiManager.globalJobID, "", nameConflict],
        saveSceneAsCleanup,
        [sm.currentScene.uiManager.globalJobID, [*sm.currentScene.uiManager.jobs]],
        True,
        False,
    )


def saveScene():
    wrapper = sm.currentScene.sqlWrapper


    if not sm.currentScene.saved:
        if sm.currentScene.name == "":
            addSaveAsJob(False)
            return
        try:
            wrapper.execute(
                "insert into scenes values('{}')".format(sm.currentScene.name)
            )
            sm.currentScene.saved = True
        except mysql.connector.errors.IntegrityError:
            addSaveAsJob(True)
            return

    save.save()
