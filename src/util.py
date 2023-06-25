import ctypes as ct

def readFile(filePath):
    file = open(filePath, "r")

    contents = file.read()

    file.close()
    return contents


def sizeof(obj):
   return (ct.sizeof(type(obj)()._type_))
    
