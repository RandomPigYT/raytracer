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
import OpenGL.raw.GL.ARB.bindless_texture as bindless


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


def loadTexture(
    rendererInstance: renderer.renderer, filename, modelDir, texType, prependTexDir=True
):
    if prependTexDir and filename != "":
        filename = os.path.join(modelDir, filename)
        # print("Loading texture:", filename)
    maxSize = (4096, 4096)

    if filename == "":
        return -1

    # types
    # 0: diffuse texture
    # 1: roughness map
    # 2: metallic map
    # 3: emissive map
    # 4: normal map
    # 5: opacity map
    # 6: specular map

    numChannels = [3, 1, 1, 3, 3, 1, 1]

    texArray = rendererInstance.textures
    texIndex = len(texArray[0])

    image = None

    filename = os.path.expanduser(filename)

    try:
        image = Image.open(filename).convert("RGB")
        image.thumbnail(maxSize, Image.Resampling.LANCZOS)

    except:
        stderr.write("Failed to load texture " + filename + "\n")
        return -1

    oldLen = len(texArray[0])
    texArray[0] = util.realloc(texArray[0], oldLen + 1)
    texArray[0][texIndex] = gl.glGenTextures(1)

    texArray[2] = util.realloc(texArray[2], len(texArray[0]))

    width, height = image.size

    red = None
    if numChannels[texType] == 1:
        red, green, blue = image.split()

        red = red.convert("RGB")

        green.close()
        blue.close()

    if numChannels[texType] == 1:
        data = np.array(red).flatten() / 255

    else:
        data = np.array(image).flatten() / 255

    texBaseName = os.path.basename(filename)

    if texBaseName in texArray[1]:
        texBaseName += "(" + str(texArray[1].count(texBaseName)) + ")"

    texArray[1].append(texBaseName)

    gl.glBindTexture(gl.GL_TEXTURE_2D, texArray[0][texIndex])

    # gl.glTexImage2D(
    #     gl.GL_TEXTURE_2D,
    #     0,
    #     gl.GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT,
    #     width,
    #     height,
    #     0,
    #     gl.GL_RGB,
    #     gl.GL_FLOAT,
    #     data,
    # )

    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGB32F,
        width,
        height,
        0,
        gl.GL_RGB,
        gl.GL_FLOAT,
        data,
    )
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

    texArray[2][texIndex] = bindless.glGetTextureHandleARB(texArray[0][texIndex])
    bindless.glMakeTextureHandleResidentARB(texArray[2][texIndex])

    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    image.close()

    if numChannels[texType] == 1:
        red.close()

    return texIndex


def loadModel(self, filename):
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

    # loadTexture(self.sceneRenderer, "./src/core/model/BLANK.jpg", "", 0, False)
    modelDir = os.path.dirname(os.path.realpath(filename))
    # Add materials
    for i in range(len(materials)):
        tempName = materials[i].name if materials[i].name != "" else "(Unnamed)"
        if materials[i].name in self.sceneRenderer.matNames:
            tempName = (
                tempName + "(" + str(self.sceneRenderer.matnames.count(tempName)) + ")"
            )
        self.sceneRenderer.matNames.append(tempName)
        self.sceneRenderer.materials[oldMaterialLen + i].albedo = (4 * ct.c_float)(
            *materials[i].diffuse, 0.0
        )
        self.sceneRenderer.materials[oldMaterialLen + i].emission = (4 * ct.c_float)(
            0.0, 0.0, 0.0, 0.0
        )
        self.sceneRenderer.materials[oldMaterialLen + i].intensity = (4 * ct.c_float)(
            1, 0, 0, 0
        )
        self.sceneRenderer.materials[oldMaterialLen + i].refractiveIndex = (
            4 * ct.c_float
        )(materials[i].ior, 0.0, 0.0, 0.0)
        self.sceneRenderer.materials[oldMaterialLen + i].transmittance = (
            4 * ct.c_float
        )(*materials[i].transmittance, 0.0)
        self.sceneRenderer.materials[oldMaterialLen + i].roughness = (2 * ct.c_float)(
            materials[i].roughness, 0.0
        )
        self.sceneRenderer.materials[oldMaterialLen + i].metallic = materials[
            i
        ].metallic
        self.sceneRenderer.materials[oldMaterialLen + i].reflectance = materials[
            i
        ].specular[0]
        self.sceneRenderer.materials[oldMaterialLen + i].opacity = materials[i].dissolve
        self.sceneRenderer.materials[oldMaterialLen + i].transmissionRoughness = 0

        self.sceneRenderer.materials[oldMaterialLen + i].textureID = loadTexture(
            self.sceneRenderer, materials[i].diffuse_texname, modelDir, 0
        )
        self.sceneRenderer.materials[oldMaterialLen + i].roughnessMapID = loadTexture(
            self.sceneRenderer, materials[i].roughness_texname, modelDir, 1
        )
        self.sceneRenderer.materials[oldMaterialLen + i].metallicMapID = loadTexture(
            self.sceneRenderer, materials[i].metallic_texname, modelDir, 2
        )
        self.sceneRenderer.materials[oldMaterialLen + i].emissiveMapID = loadTexture(
            self.sceneRenderer, materials[i].emissive_texname, modelDir, 3
        )
        self.sceneRenderer.materials[oldMaterialLen + i].normalMapID = loadTexture(
            self.sceneRenderer, materials[i].normal_texname, modelDir, 4
        )
        self.sceneRenderer.materials[oldMaterialLen + i].specularMapID = loadTexture(
            self.sceneRenderer, materials[i].specular_texname, modelDir, 6
        )

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

        self.sceneRenderer.meshes[i + meshOffset].materialID = (
            oldMaterialLen + shapes[i].mesh.material_ids[0]
            if shapes[i].mesh.material_ids[0] != -1
            else 0
        )
        # print(shapes[i].name)
        # print(self.sceneRenderer.materials[self.sceneRenderer.meshes[i + meshOffset].materialID].textureID)

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
