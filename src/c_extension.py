import os
import ctypes as ct

ext = None

if os.name == "nt":
    ext = ct.CDLL("c_extension/lib/extension.dll")

else:
    ext = ct.CDLL("c_extension/lib/extension.so")


def init():
    global ext

    ext.addOffset.restype = ct.c_void_p
    ext.addOffset.argtypes = [ct.c_void_p, ct.c_uint64, ct.c_int8]
