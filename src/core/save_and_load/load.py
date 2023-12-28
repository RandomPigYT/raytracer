import core.save_and_load.sqlWrapper as sqlWrapper
import sceneManager as sm
import mysql.connector as con
import core.renderer as renderer
import ctypes as ct
import core.model.loadModel as lm
import util
import OpenGL.GL as gl
import glm


def calcTransformMat(transform: renderer.Transform):
    mat = glm.translate(glm.mat4(1), glm.vec3(*transform.position))
    mat = glm.rotate(mat, transform.rotation[0], glm.vec3(1, 0, 0))
    mat = glm.rotate(mat, transform.rotation[1], glm.vec3(0, 1, 0))
    mat = glm.rotate(mat, transform.rotation[2], glm.vec3(0, 0, 1))
    mat = glm.scale(mat, glm.vec3(*transform.scale))

    return mat
    
def applyTransformToMeshes(start, num, transform):
    r = sm.currentScene.sceneRenderer
    for i in range(start, start + num):
        r.meshes[i].transform = util.mat4ToFloatArray4Array4(
            transform * glm.mat4(r.meshes[i].transform)
        )




def load(sceneName):
    wrapper = sm.currentScene.sqlWrapper
    r = sm.currentScene.sceneRenderer

    # Load object transforms
    wrapper.execute("select * from {}_obj_transform order by id".format(sceneName))
    objTransforms = wrapper.fetch()

    r.objectTransforms = []
    for i in objTransforms:
        r.objectTransforms.append(renderer.Transform())
        r.objectTransforms[i[0]].position = [float(i[1]), float(i[2]), float(i[3])]
        r.objectTransforms[i[0]].rotation = [float(i[4]), float(i[5]), float(i[6])]
        r.objectTransforms[i[0]].scale = [float(i[7]), float(i[8]), float(i[9])]
    

    # Load mesh transforms
    wrapper.execute("select * from {}_mesh_transform order by id".format(sceneName))
    meshTransforms = wrapper.fetch()

    r.meshTransforms = []
    for i in meshTransforms:
        r.meshTransforms.append(renderer.Transform())
        r.meshTransforms[i[0]].position = [float(i[1]), float(i[2]), float(i[3])]
        r.meshTransforms[i[0]].rotation = [float(i[4]), float(i[5]), float(i[6])]
        r.meshTransforms[i[0]].scale = [float(i[7]), float(i[8]), float(i[9])]
    
    # Load textures
    wrapper.execute("select * from {}_textures order by id".format(sceneName))
    textures = wrapper.fetch()

    r.textures = [(0 * ct.c_uint32)(), [], (0 * ct.c_uint64)()]
    r.texPaths = []
    for i in textures:
        lm.loadTexture(r, i[1], "", 0, False)
    
    # Load vertices
    wrapper.execute("select * from {}_vertices order by id".format(sceneName))
    verts = wrapper.fetch()

    r.vertices = util.realloc(r.vertices, len(verts))
    for i, v in enumerate(verts):
        r.vertices[i].position = (4 * ct.c_float)(v[1], v[2], v[3], 1.0)
        r.vertices[i].normal = (4 * ct.c_float)(v[4], v[5], v[6])
        r.vertices[i].textureCoord = (2 * ct.c_float)(v[7], v[8])
    
    # Load meshes
    wrapper.execute("select * from {}_meshes order by id".format(sceneName))
    meshes = wrapper.fetch()

    r.meshes = util.realloc(r.meshes, len(meshes))
    r.meshNames = []
    r.meshVBO = []

    for i, mesh in enumerate(meshes):
        r.meshNames.append(mesh[1])
        r.meshVBO.append(gl.glGenBuffers(1))

        r.meshes[i].startingVertex = mesh[2]
        r.meshes[i].numTriangles = mesh[3]
        r.meshes[i].materialID = mesh[5]
        r.meshes[i].transform = util.mat4ToFloatArray4Array4(calcTransformMat(r.meshTransforms[i]))
    
    # Load objects
    wrapper.execute("select * from {}_objects order by id".format(sceneName))
    objs = wrapper.fetch()

    r.objects = util.realloc(r.objects, len(objs))
    r.objectNames = []

    for i, obj in enumerate(objs):
        r.objectNames.append(obj[1])
        
        r.objects[i].ID = i
        r.objects[i].startingMesh = obj[2]
        r.objects[i].numMeshes = obj[3]
        temp = calcTransformMat(r.objectTransforms[i])
        r.objects[i].transform = util.mat4ToFloatArray4Array4(temp)
        applyTransformToMeshes(obj[2], obj[3], temp)
    
    # Load materials
    wrapper.execute("select * from {}_materials order by id".format(sceneName))
    mats = wrapper.fetch()

    r.materials = util.realloc(r.materials, len(mats))
    r.matNames = []

    for i, mat in enumerate(mats):
        r.matNames.append(mat[1])

        r.materials[i].albedo = (ct.c_float * 4)(mat[2], mat[3], mat[4], 1.0)
        r.materials[i].emission = (ct.c_float * 4)(mat[5], mat[6], mat[7], 1.0)
        r.materials[i].roughness[0] = mat[8]
        r.materials[i].metallic = mat[9]
        r.materials[i].reflectance = mat[10]
        r.materials[i].opacity = mat[11]
        
        r.materials[i].textureID = mat[12] if mat[12] != None else -1
        r.materials[i].roughnessMapID = mat[13] if mat[13] != None else -1
        r.materials[i].metallicMapID = mat[14] if mat[14] != None else -1
        r.materials[i].emissiveMapID = mat[15] if mat[15] != None else -1
        r.materials[i].normalMapID = mat[16] if mat[16] != None else -1
        r.materials[i].opacityMapID = mat[17] if mat[17] != None else -1
        r.materials[i].specularMapID = mat[18] if mat[18] != None else -1
        r.materials[i].displacementMapID = mat[19] if mat[19] != None else -1

        
    
    r.updateBvh()
    r.getVertMeshRelation(0)
    r.updateBuffers(0)
    sm.currentScene.allocateSSBO()