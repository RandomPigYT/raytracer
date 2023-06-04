def readFile(filePath):
    file = open(filePath, "r")

    contents = file.read()

    file.close()
    return contents
