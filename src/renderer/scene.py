class Vertex:
    def __init__(self, position, normal, textureCoord):
        self.position = position
        self.normal = normal
        self.textureCoord = textureCoord


class Material:
    def __init__(
        self,
        colour,
        specularColour,
        roughness,
        metallicity,
        transparency,
        refractiveIndex,
    ):
        self.colour = colour
        self.specularColour = specularColour
        self.roughness = roughness
        self.metallicity = metallicity
        self.transmittivity = transmittivity


class Mesh:
    def __init__(self, startingVertex, numTriangles, objectId, material):
        self.startingVertex = startingVertex
        self.numTriangles = numTriangles
        self.materialID = material

        self.objectId = objectId


class Object:
    def __init__(self, name, ID, pos):
        self.ID = ID
        self.name = name
        self.pos = pos


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
        shaderProgram,
        computeProgram,
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
