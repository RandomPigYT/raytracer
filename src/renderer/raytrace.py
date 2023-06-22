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


class SceneData(ct.Structure):
    _fields_ = [
        ("cameraPos", ct.c_float * 3),
        ("cameraDir", ct.c_float * 3),
        ("vertices", ct.POINTER(sc.Vertex)),
        ("materials", ct.POINTER(sc.Material)),
        ("meshes", ct.POINTER(sc.Mesh)),
        ("objects", ct.POINTER(sc.Object)),
        ("shaderProgram", ct.c_uint32),
    ]


def raytrace(scene: sc.Scene, maxBounces, raysPerPixel):
    rt_ext = None

    if os.name == "nt":
        rt_ext = ct.CDLL("c_extension/lib/extension.dll")

    else:
        rt_ext = ct.CDLL("c_extension/lib/extension.so")

    rt_ext.sendToShader.restype = None
    rt_ext.sendToShader.argtypes = [SceneData, ArgData]

    data = SceneData(
        scene.cameraPos,
        scene.cameraDirection,
        scene.vertices,
        scene.materials,
        scene.meshes,
        scene.objects,
        scene.computeProgram,
    )

    argumentInfo = ArgData(
        numVertices=len(scene.vertices),
        numMaterials=len(scene.materials),
        numMeshes=len(scene.meshes),
        numObjects=len(scene.objects),
    )

    rt_ext.sendToShader(data, argumentInfo)
