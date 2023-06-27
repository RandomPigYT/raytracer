import ctypes as ct

def readFile(filePath):
    file = open(filePath, "r")

    contents = file.read()

    file.close()
    return contents


def sizeof(obj):
   return ct.sizeof((obj._type_))


def realloc(array, n):
    
    resized = (n * array._type_)()
    ct.memmove(resized, array, len(array) * ct.sizeof(array._type_))

    return resized



