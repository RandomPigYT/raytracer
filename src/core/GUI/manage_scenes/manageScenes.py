import sceneManager as sm
import core.save_and_load.load as load
import mysql.connector
import core.GUI.enterText as enterText
import imgui

def manageScenesCleanup(selfIndex, prevJobs):
    ids = [i.id for i in prevJobs]
    sm.currentScene.uiManager.removeJob(selfIndex)
    sm.currentScene.uiManager.activateJobs(ids)

def delete(scene):
    wrapper = sm.currentScene.sqlWrapper

    wrapper.execute("delete from scenes where name = '{}'".format(scene))

    wrapper.execute("drop table if exists {}_objects".format(scene))
    wrapper.execute("drop table if exists {}_meshes".format(scene))
    wrapper.execute("drop table if exists {}_materials".format(scene))
    wrapper.execute("drop table if exists {}_vertices".format(scene))
    wrapper.execute("drop table if exists {}_textures".format(scene))
    wrapper.execute("drop table if exists {}_mesh_transform".format(scene))
    wrapper.execute("drop table if exists {}_obj_transform".format(scene))


def renameTables(oldName, newName):
    wrapper = sm.currentScene.sqlWrapper

    wrapper.execute("alter table {}_objects rename {}_objects".format(oldName, newName))
    wrapper.execute("alter table {}_meshes rename {}_meshes".format(oldName, newName))
    wrapper.execute("alter table {}_materials rename {}_materials".format(oldName, newName))
    wrapper.execute("alter table {}_vertices rename {}_vertices".format(oldName, newName))
    wrapper.execute("alter table {}_textures rename {}_textures".format(oldName, newName))
    wrapper.execute("alter table {}_mesh_transform rename {}_mesh_transform".format(oldName, newName))
    wrapper.execute("alter table {}_obj_transform rename {}_obj_transform".format(oldName, newName))

    if sm.currentScene.name == oldName and sm.currentScene.saved:
        sm.currentScene.name = newName

def rename(selfIndex, scene, name, nameConflict):
    wrapper = sm.currentScene.sqlWrapper

    label = "Rename" + (" (Conflicting names)" if nameConflict else "")
    name, done, cancel = enterText.enterName(label, name, False, False)

    for i in range(len(sm.currentScene.uiManager.jobs)):
        if sm.currentScene.uiManager.jobs[i].id == selfIndex:
            sm.currentScene.uiManager.jobs[i].renderArgs[2] = name

    if done:
        try:
            wrapper.execute(
                "insert into scenes values('{}')".format(name)
            )
        except mysql.connector.errors.IntegrityError:
            if name == scene:
                return True
            for i in range(len(sm.currentScene.uiManager.jobs)):
                if sm.currentScene.uiManager.jobs[i].id == selfIndex:
                    sm.currentScene.uiManager.jobs[i].renderArgs[2] = ""
                    sm.currentScene.uiManager.jobs[i].renderArgs[3] = True
            return False

        wrapper.execute("delete from scenes where name = '{}'".format(scene))
        renameTables(scene, name)

    if cancel:
        return True

    wrapper.execute("commit")
    # sm.currentScene.saved = True
    return done



def manage(selfIndex):
    wrapper = sm.currentScene.sqlWrapper

    wrapper.execute("select * from scenes")
    scenes = wrapper.fetch()

    imgui.begin("Manage Scenes")

    for i in scenes:
        imgui.text(i[0])
        if imgui.button("Rename##" + i[0]):
            imgui.end()
            sm.currentScene.uiManager.deactivateAll()
            sm.currentScene.uiManager.addJob(
                rename,
                [sm.currentScene.uiManager.globalJobID, i[0], "", False],
                manageScenesCleanup,
                [
                    sm.currentScene.uiManager.globalJobID,
                    [i for i in sm.currentScene.uiManager.jobs if i.id == selfIndex],
                ],
                True,
                False,
            )
            return False
        
        imgui.same_line()

        if imgui.button("Delete##" + i[0]):
            delete(i[0])
            imgui.end()
            return False
        
        imgui.separator()

    if imgui.button("Done"):
        imgui.end()
        return True

    imgui.end()





