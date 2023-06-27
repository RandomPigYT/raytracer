import renderer.scene as sc
import ctypes as ct
import util


class modelStruct:
    
    positions = []
    normals = []
    texCoords = []

def parseFace(scene, line, model: modelStruct, index):

    def replaceEmptyStrings(l):
        for i in range(len(l)):
            if l[i] == '':
                l[i] = '0'

    toks = line.split()

    if toks[0] != 'f':
        return line

    v, vn, vt = 0, 0, 0
    
    # Basically omits the first element of 'toks'
    for i in toks[1:]:
        temp = i.split('/')
        
        replaceEmptyStrings(temp)
        
        # This is so that temp has a minimum size of 3
        temp.extend(['0', '0'])


        v, vt, vn = temp[:3]
        v = int(v); vt = int(vt); vn = int(vn)

        
        # generate the real vertices
        

    




def parseLine(line, model: modelStruct):
    
    toks = line.split()

    if not len(toks):
        return
    
    # Parse positions
    if toks[0] == 'v':
        temp = (3 * ct.c_float)(float(toks[1]),
                                float(toks[2]),
                                float(toks[3]))

        model.positions.append(temp)

    # Parse texture coordinates
    elif toks[0] == 'vt':
        temp = (2 * ct.c_float)(float(toks[1]),
                                float(toks[2]))
        
        model.texCoords.append(temp)

    # Parse vertex normals
    elif toks[0] == 'vn':
        temp = (3 * ct.c_float)(float(toks[1]),
                                float(toks[2]),
                                float(toks[3]))
        
        model.normals.append(temp)

    else:
        return line
    

    
    

def loadModel(self, filename):
    
    def numFaces(lines):
        count = 0
        for i in lines:
            if i.split()[0] == 'f':
                count += 1

        return count

            

    objFile = open(filename, "r")

    lines = objFile.readlines()

    objFile.close()

    model = modelStruct()

    unprocessedLines = []
    
    for i in lines:

        # Omits the newline character at the end of the line
        temp = parseLine(i[:-1], model)
        
        if temp:
            unprocessedLines.append(temp)

    print(len(self.vertices))
    
    self.vertices = util.realloc(self.vertices, 
                                 len(self.vertices) + (3 * numFaces(unprocessedLines)))
    
    print(len(self.vertices))
        
    for i in unprocessedLines:
        parseFace(self, i, model, numFaces(unprocessedLines))




