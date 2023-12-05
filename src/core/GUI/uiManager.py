from enum import Enum

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





class UIManager:

    def __init__(self):
        self.containerID = 0
        self.containers = []
    
    def addContainer(self, types, labels, callbacks, isACtiveCallbacks):
        pass



    
