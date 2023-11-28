import glm
import ctypes as ct


def isVecNull(vec):
    for i in vec:
        if i:
            return False
    return True


def generateNormals(self):
    for i in range(0, len(self.vertices), 3):
        if not (
            isVecNull(self.vertices[i].normal)
            and isVecNull(self.vertices[i + 1].normal)
            and isVecNull(self.vertices[i + 2].normal)
        ):
            continue

        edge1 = glm.vec3(self.vertices[i + 1].position) - glm.vec3(
            self.vertices[i].position
        )
        edge2 = glm.vec3(self.vertices[i + 2].position) - glm.vec3(
            self.vertices[i].position
        )

        normal = glm.normalize(glm.cross(edge1, edge2))

        self.vertices[i].normal = (4 * ct.c_float)(*normal, 0.0)
        self.vertices[i + 1].normal = (4 * ct.c_float)(*normal, 0.0)
        self.vertices[i + 2].normal = (4 * ct.c_float)(*normal, 0.0)
