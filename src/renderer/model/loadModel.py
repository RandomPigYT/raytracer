import renderer.scene as sc
import ctypes as ct


class modelStruct:
    
    positions = []
    normals = []
    texCoords = []

def parseFace(line, model: modelStruct):
    toks = line.split()

    if toks[0] != 'f':
        return line

    v, vn, vt = 0, 0, 0
    
    # Basically omits the first element of 'toks'
    for i in toks[1:]:
        temp = i.split('/')
        
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
    

    
    

def loadModel(filename):
    objFile = open(filename, "r")

    lines = objFile.readlines()

    model = modelStruct()

    unprocessedLines = []
    
    for i in lines:

        # Omits the newline character at the end of the line
        temp = parseLine(i[:-1], model)
        
        if temp:
            unprocessedLines.append(temp)
        
    for i in unprocessedLines:
        parseFace(i, model)




