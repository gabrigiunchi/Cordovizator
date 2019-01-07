def readFromFile(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content


def writeToFile(path, content):
    file = open(path, "w")
    file.write(content)
    file.close()


def appendToFile(path, content):
    file = open(path, "a")
    file.write(content)
    file.close()
