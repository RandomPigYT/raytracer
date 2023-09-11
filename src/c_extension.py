import os
import ctypes as ct
import core.model.loadModel as lm
import core.scene as sc
import core.renderer as renderer

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
        ct.POINTER(ct.POINTER(renderer.Vertex)),
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_float),
        ct.POINTER(lm.face),
        ct.c_int32,
        ct.c_int32,
    ]
    
    ext.constructBvh.restype = ct.POINTER(renderer.Bvh)
    ext.constructBvh.argtypes = [
        ct.POINTER(ct.c_uint32),
        ct.POINTER(renderer.Vertex),
        ct.c_uint32
    ]

    
