import renderer.scene as sc
import ctypes as ct
import os
import OpenGL as gl
from c_extension import ext
import util


def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):

    
    
    a = (3 * ct.c_int32)(1, 2, 3)
    

    ptr = ct.cast(ext.addOffset(ct.cast(a, ct.c_void_p), 2, util.sizeof(a), 1), ct.POINTER(ct.c_int32))
    

    ptr = ct.cast(ext.addOffset(ct.cast(ptr, ct.c_void_p), 1, ct.sizeof(ct.c_int32), -1), ct.POINTER(ct.c_int32))
    print(ptr.contents)
        
    


