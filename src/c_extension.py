import os
import ctypes as ct
import renderer.model.loadModel as lm
import renderer.scene as sc

ext = None

if os.name == "nt":
    ext = ct.CDLL("c_extension/lib/extension.dll")

else:
    ext = ct.CDLL("c_extension/lib/extension.so")


def init():
    global ext

    ext.addOffset.restype = ct.c_void_p
    ext.addOffset.argtypes = [ct.c_void_p, ct.c_uint64, ct.c_int8]

    ext.generateVerts.restype = None
    ext.generateVerts.argtypes = [
        ct.POINTER(ct.POINTER(sc.Vertex)),
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_float),
        ct.POINTER(lm.face),
        ct.c_int32,
        ct.c_int32,
    ]
