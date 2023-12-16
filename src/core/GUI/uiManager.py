from enum import Enum
import imgui
import core.GUI.menuBar as mb


class containerTypes(Enum):
    BUTTON = 0
    TEXT_BOX = 1
    DRAG_FLOAT1 = 2
    DRAG_FLOAT2 = 3
    DRAG_FLOAT3 = 4
    COLOUR_PICKER = 5
    DROP_DOWN = 6


class container:
    def __init__(self):
        self.elements = []
        self.labels = []
        self.callBacks = []
        self.isActiveCallbacks = []

    def addElement(self, type, label, callback, isActiveCallback):
        pass

    def render(self):
        pass


class Job:
    def __init__(
        self,
        jobID,
        runFunc,
        renderArgs,
        cleanupFunc,
        cleanupArgs,
        isActive,
        isDefaultJob,
    ):
        self.id = jobID

        self.renderFunc = runFunc
        self.renderArgs = renderArgs
        self.cleanupFunc = cleanupFunc
        self.cleanupArgs = cleanupArgs

        self.isActive = isActive
        self.isDefaultJob = isDefaultJob

    def run(self):
        return self.renderFunc(*self.renderArgs)

    def cleanup(self):
        if self.cleanupFunc != None:
            self.cleanupFunc(*self.cleanupArgs)


class UIManager:
    def __init__(self):
        self.jobs = []
        self.globalJobID = 0

    def addJob(
        self, renderFunc, renderArgs, cleanupFunc, cleanupArgs, isActive, isDefaultJob
    ):
        self.globalJobID += 1
        temp = Job(
            self.globalJobID - 1,
            renderFunc,
            renderArgs,
            cleanupFunc,
            cleanupArgs,
            isActive,
            isDefaultJob,
        )
        self.jobs.append(temp)
        return self.globalJobID - 1

    def removeJob(self, jobID):
        for i in range(len(self.jobs)):
            if self.jobs[i].id == jobID:
                self.jobs.pop(i)
                return

    def activateJobs(self, jobIDs):
        for i in range(len(self.jobs)):
            if self.jobs[i].id in jobIDs:
                self.jobs[i].isActive = True

    def deActivateJobs(self, jobIDs):
        for i in range(len(self.jobs)):
            if self.jobs[i].id in jobIDs:
                self.jobs[i].isActive = False

    def makeDefault(self, jobIDs):
        for i in range(len(self.jobs)):
            if self.jobs[i].id in jobIDs:
                self.jobs[i].isDefaultJob = True

    def removeDefault(self, jobIDs):
        for i in range(len(self.jobs)):
            if self.jobs[i].id in jobIDs:
                self.jobs[i].isDefaultJob = False

    def activateDefault(self):
        for i in range(len(self.jobs)):
            if not self.jobs[i].isDefaultJob:
                self.jobs[i].isActive = False
                continue
            self.jobs[i].isActive = True

    def deactivateAll(self):
        for i in range(len(self.jobs)):
            self.jobs[i].isActive = False

    def render(self):
        # self.renderMenuBar()
        # for i in range(len(self.jobs)):
        #     if self.jobs[i]():
        #         self.jobs.pop(i)

        for i in self.jobs:
            if i.isActive:
                if i.run():
                    i.cleanup()
