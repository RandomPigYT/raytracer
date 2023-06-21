import renderer.scene as sc
import ctypes as ct
import os

class ArgData(ct.Structure):

    _fields_ = [("numVertices", ct.c_uint64),
                ("numMaterials", ct.c_uint64),
                ("numMeshes", ct.c_uint64),
                ("numObjects", ct.c_uint64)]


def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):
    
    rt_ext = None

    if os.name == 'nt':
        rt_ext = ct.CDLL("c_extension/lib/extension.dll")

    else:
        rt_ext = ct.CDLL("c_extension/lib/extension.so")
        


    rt_ext.sendToShader.restype = None
    rt_ext.sendToShader.argtypes = [ct.POINTER(sc.Vertex),
                                    ct.POINTER(sc.Material),
                                    ct.POINTER(sc.Mesh),
                                    ct.POINTER(sc.Object),
                                    ArgData]

    
    a = (sc.Mesh * 3)((1,2,3,4), (7,8,9,10), (3,4,5,6))
    data = ArgData(0, 0, 3, 0)

    rt_ext.sendToShader(None, None, a, None, data)


