import ctypes as ct


class Vertex(ct.Structure):
    _fields_ = [("position", ct.c_float * 3), 
                ("padding0", ct.c_float),
                ("normal", ct.c_float * 3),
                ("padding1", ct.c_float),
                ("textureCoord", ct.c_float * 3),
                ("padding2", ct.c_float)]


class Material(ct.Structure):
                                        
    _fields_ = [("kd", ct.c_float * 3),      
                ("alpha_x", ct.c_float),    
                ("ks", ct.c_float * 3),      
                ("alpha_y", ct.c_float),     
                ("emission", ct.c_float * 3),
                ("padding3", ct.c_float)]



class Mesh(ct.Structure):

    _fields_ = [("startingVertex", ct.c_uint64),
               ("numTriangles", ct.c_uint64),
               ("materialID", ct.c_uint64),
               ("objectID", ct.c_uint64)]


class Object(ct.Structure):
    
    _fields_ = [("pos", ct.c_float * 3),
                ("ID", ct.c_uint32)]


class Scene:
    def __init__(
        self,
        name,
        cameraPos,
        cameraDirection,
        vertices,
        materials,
        meshes,
        objects,
        objectNames,
        shaderProgram,
        computeProgram
    ):
        self.name = name

        self.shaderProgram = shaderProgram
        self.computeProgram = computeProgram

        self.cameraPos = cameraPos
        self.cameraDirection = cameraDirection

        self.vertices = vertices
        self.material = materials
        self.meshes = meshes
        self.objects = objects
        self.objectNames = objectNames
