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
    ct.memmove(resized, array, min(len(array), n) * ct.sizeof(array._type_))

    return resized


def toCtypesArr(pyarr, arrType):
    return (len(pyarr) * arrType)(*pyarr)


def pointerArithmetic(ptr, offset):
    temp = ct.cast(ct.pointer(ptr), ct.c_void_p)
    temp.value += offset * ct.sizeof(ptr._type_)

    return ct.cast(temp.value, ct.POINTER(ptr._type_))