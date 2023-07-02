import ctypes as ct
import renderer.canvas as canvas
import renderer.model.loadModel as lm
import OpenGL.GL as gl


class Vertex(ct.Structure):
    _fields_ = [
        ("position", ct.c_float * 4),
        ("normal", ct.c_float * 4),
        ("textureCoord", ct.c_float * 2),
        ("padding0", ct.c_float * 2)
    ]


class Material(ct.Structure):
    _fields_ = [
        ("kd", ct.c_float * 3),  # 0   12
        ("padding0", ct.c_float),  # 12   4
        ("alpha", ct.c_float * 2),  # 16  8
        ("padding1", ct.c_float * 2),  # 24  8
        ("ks", ct.c_float * 3),  # 32    12
        ("padding1", ct.c_float),  # 44  4
        ("emission", ct.c_float * 3),  # 48  12
        ("padding3", ct.c_float),  # 60    4
    ]


class Mesh(ct.Structure):
    _fields_ = [
        ("startingVertex", ct.c_uint32),
        ("numTriangles", ct.c_uint32),
        ("materialID", ct.c_uint32),
        ("objectID", ct.c_uint32),
    ]


class Object(ct.Structure):
    _fields_ = [("pos", ct.c_float * 3), ("ID", ct.c_uint32)]


class Scene:

    # All the variables defined outside methods have been placed where they have been 
    # for arbitrary reasons. Don't read too much into it.
    vertices = (0 * Vertex)()
    meshes = (0 * Mesh)()
    materials = (0 * Material)()
    objects = (0 * Object)()

    vertSSBO = None
    meshSSBO = None
    materialSSBO = None


    def __init__(self, name, cameraPos, cameraDirection):
        self.name = name

        self.cameraPos = cameraPos
        self.cameraDirection = cameraDirection
        
        self.initSSBO()


    # Methods
    loadModel = lm.loadModel
    initCanvas = canvas.initRenderCavas

    def initSSBO(self):
        self.vertSSBO = gl.glGenBuffers(1)
        self.meshSSBO = gl.glGenBuffers(1)
        self.materialSSBO = gl.glGenBuffers(1)
    
    def allocateSSBO(self):

       #for i in self.vertices:
       #    print(*i.position)


        # Resize vertices ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.vertSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Vertex) * len(self.vertices), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 0, self.vertSSBO)
        
        # Populate vertices ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.vertices, ct.sizeof(Vertex) * len(self.vertices))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)
    
        # Resize meshes ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.meshSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Mesh) * len(self.meshes), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, self.meshSSBO)
        
        # Populate meshes ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.meshes, ct.sizeof(Mesh) * len(self.meshes))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)

        # Resize materials ssbo
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.materialSSBO)
        gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, ct.sizeof(Material) * len(self.materials), None, gl.GL_DYNAMIC_READ)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.materialSSBO)
        
        # Populate materials ssbo
        ptr = ct.cast(gl.glMapBuffer(gl.GL_SHADER_STORAGE_BUFFER, gl.GL_WRITE_ONLY), ct.c_void_p)
        ct.memmove(ptr, self.materials, ct.sizeof(Material) * len(self.materials))
        gl.glUnmapBuffer(gl.GL_SHADER_STORAGE_BUFFER)
        

        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

        self.sendUniforms()
    
    def sendUniforms(self):
        camPosLoc = gl.glGetUniformLocation(self.compute, "cameraPos")
        camDirLoc = gl.glGetUniformLocation(self.compute, "cameraDir")

        gl.glUseProgram(self.compute)

        gl.glUniform3f(camPosLoc, *self.cameraPos)
        gl.glUniform3f(camDirLoc, *self.cameraDirection)
        

        

    

        

