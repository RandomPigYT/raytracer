import renderer.scene as sc
import ctypes as ct
import os


class ArgData(ct.Structure):
    _fields_ = [
        ("numVertices", ct.c_uint64),
        ("numMaterials", ct.c_uint64),
        ("numMeshes", ct.c_uint64),
        ("numObjects", ct.c_uint64),
    ]


def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):
    rt_ext = None

    if os.name == "nt":
        rt_ext = ct.CDLL("c_extension/lib/extension.dll")

    else:
        rt_ext = ct.CDLL("c_extension/lib/extension.so")

    rt_ext.sendToShader.restype = None
    rt_ext.sendToShader.argtypes = [
        ct.c_float * 3,
        ct.c_float * 3,
        ct.POINTER(sc.Vertex),
        ct.POINTER(sc.Material),
        ct.POINTER(sc.Mesh),
        ct.POINTER(sc.Object),
        ArgData,
        ct.c_uint32,
    ]

    argumentInfo = ArgData(
        numVertices=len(scene.vertices),
        numMaterials=len(scene.materials),
        numMeshes=len(scene.meshes),
        numObjects=len(scene.objects),
    )

    rt_ext.sendToShader(
        scene.cameraPos,
        scene.cameraDirection,
        scene.vertices,
        scene.materials,
        scene.meshes,
        scene.objects,
        argumentInfo,
        scene.computeProgram,
    )
