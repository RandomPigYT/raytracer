import ctypes as ct
import util
import tinyobjloader as tol
from sys import stderr
import c_extension as cext
import core.renderer as renderer
import OpenGL.GL as gl
import glm
import time
import os
import pathlib
from PIL import Image
import numpy as np


class face(ct.Structure):
    _fields_ = [
        ("v_index", ct.c_int32),
        ("vt_index", ct.c_int32),
        ("vn_index", ct.c_int32),
    ]


def numFaces(shapes):
    count = 0
    for i in shapes:
        count += len(i.mesh.indices)

    return count


def loadTexture(renderer, filename, texType):
    # types
    # 0: diffuse texture
    # 1: roughness map
    # 2: metallic map
    # 3: emissive map
    # 4: normal map
    # 5: opacity map
    types = [
        renderer.textures,
        renderer.roughnessMaps,
        renderer.metallicMaps,
        renderer.emissiveMaps,
        renderer.normalMaps,
        renderer.opacityMaps,
        renderer.specularMaps
    ]

    numChannels = [
        3,
        1,
        1,
        3,
        3,
        1,
        1
    ]

    texArray = types[texType]
    texIndex = len(texArray)

    texHandlex = None

    filename = os.path.expanduser(filename)

    try:
        texHandle = Image.open(filename).convert("RGB")
    except FileNotFoundError:
        stderr.write("Failed to load texture " + filename + "\n")
        return False
    
    texArray = util.realloc(texArray, len(texArray) + 1)

    red, green, blue = texHandle.split()

    texData = np.array(texHandle).flatten() / 255
    redData = np.array(red).flatten() / 255


    







def loadModel(self, filename):

    loadTexture(self.sceneRenderer, r"C:\Users\HP\Desktop\vintage-lamp-free\textures\Curves_Emissive_emissive.jpeg", 0)

    oldLen = len(self.sceneRenderer.vertices)
    oldMeshLen = len(self.sceneRenderer.meshes)
    oldMaterialLen = len(self.sceneRenderer.materials)

    reader = tol.ObjReader()
    status = reader.ParseFromFile(filename)

    if not status:
        stderr.write("Failed to load " + filename + "\n")
        return False

    attribs = reader.GetAttrib()
    shapes = reader.GetShapes()
    materials = reader.GetMaterials()

    v = (len(attribs.vertices) * ct.c_float)(*attribs.vertices)
    vn = (len(attribs.normals) * ct.c_float)(*attribs.normals)
    vt = (len(attribs.texcoords) * ct.c_float)(*attribs.texcoords)

    vertOffset = len(self.sceneRenderer.vertices)
    meshOffset = len(self.sceneRenderer.meshes)

    # Allocate memory
    self.sceneRenderer.vertices = util.realloc(
        self.sceneRenderer.vertices, len(self.sceneRenderer.vertices) + numFaces(shapes)
    )
    self.sceneRenderer.meshes = util.realloc(
        self.sceneRenderer.meshes, len(self.sceneRenderer.meshes) + len(shapes)
    )
    self.sceneRenderer.materials = util.realloc(
        self.sceneRenderer.materials, len(self.sceneRenderer.materials) + len(materials)
    )
    self.sceneRenderer.objects = util.realloc(
        self.sceneRenderer.objects, len(self.sceneRenderer.objects) + 1
    )

    # Add materials
    for i in range(len(materials)):
        pass
        print(materials[i].specular_texname)

    # Set object data
    objIndex = len(self.sceneRenderer.objects) - 1
    self.sceneRenderer.objects[objIndex].transform = util.mat4ToFloatArray4Array4(
        glm.mat4(1)
    )
    self.sceneRenderer.objects[objIndex].ID = objIndex
    self.sceneRenderer.objects[objIndex].startingMesh = oldMeshLen
    self.sceneRenderer.objects[objIndex].numMeshes = len(shapes)

    objname = pathlib.Path(filename).stem
    if objname not in self.sceneRenderer.objectNames:
        self.sceneRenderer.objectNames.append(objname)

    else:
        self.sceneRenderer.objectNames.append(
            objname + "(" + str(self.sceneRenderer.objectNames.count(objname)) + ")"
        )

    self.sceneRenderer.objectTransforms.append(renderer.Transform())

    # generate mesh data
    startingVertCount = 0
    for i in range(len(shapes)):
        if shapes[i].name not in self.sceneRenderer.meshNames:
            self.sceneRenderer.meshNames.append(shapes[i].name)

        else:
            self.sceneRenderer.meshNames.append(
                shapes[i].name
                + "("
                + str(self.sceneRenderer.meshNames.count(shapes[i].name))
                + ")"
            )

        self.sceneRenderer.meshes[i + meshOffset].startingVertex = (
            startingVertCount + vertOffset
        )
        self.sceneRenderer.meshes[i + meshOffset].numTriangles = len(
            shapes[i].mesh.indices
        )

        self.sceneRenderer.meshes[i + meshOffset].materialID = i + meshOffset

        startingVertCount += self.sceneRenderer.meshes[i + meshOffset].numTriangles

        self.sceneRenderer.meshes[
            i + meshOffset
        ].transform = util.mat4ToFloatArray4Array4(glm.mat4(1))

        self.sceneRenderer.meshTransforms.append(renderer.Transform())

        # Generate the VBOs for the newly added meshes
        self.sceneRenderer.meshVBO.append(gl.glGenBuffers(1))

    # generate vertices
    for shape in shapes:
        temp = (len(shape.mesh.indices) * face)(
            *[
                face(
                    v_index=i.vertex_index,
                    vt_index=i.texcoord_index,
                    vn_index=i.normal_index,
                )
                for i in shape.mesh.indices
            ]
        )

        cext.ext.generateVerts(
            ct.byref(ct.cast(self.sceneRenderer.vertices, ct.POINTER(renderer.Vertex))),
            v,
            vn,
            vt,
            temp,
            len(temp),
            vertOffset,
        )

        vertOffset += len(temp)

    self.sceneRenderer.generateNormals(oldLen)
    self.sceneRenderer.updateBvh()
    self.sceneRenderer.getVertMeshRelation(oldLen)

    self.sceneRenderer.updateBuffers(oldMeshLen)

    self.sendVertMeshRel()

    self.allocateSSBO()

    return True
