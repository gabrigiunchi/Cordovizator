import json
import os
from shutil import copyfile, rmtree
import random
import sys

# GIT CLONE 
projectSrc = "git@git.eu-de.bluemix.net:alessiosaltarin/MobilePwa.git"

if sys.argv.__len__() > 1:
    projectSrc = sys.argv[1]
    print(projectSrc)

projectName = projectSrc.split("/")[1].split(".")[0]
print("Project name: " + projectName)
print("Cloning from git")
os.system("git clone " + projectSrc)
print("Going in the project directory")
os.chdir(projectName)

#UPDATE index.html
print("Updating index.html")
filePath = "src/index.html"
file = open(filePath, "r")
line = "a"
content = ""

while line != "":
    line = file.readline()
    if line.strip() == """<base href="/">""":
        line = """\t<base href="./">\n"""

    content += line
    if line == "<head>\n":
        content += """\t<script type="text/javascript" charset="utf-8" src="cordova.js"></script>\n"""

file.close()
file = open(filePath, "w")
file.write(content)
file.close()
    

# UPDATE angular.json
print("Updating angular.json")
fileName = "angular.json"

print("Reading from " + fileName)

file = open(fileName, "r")
content = file.read()
file.close()
print("Content loaded")

jsonContent = json.loads(content)

keys = jsonContent["projects"].keys()
projectName = next(iter(keys))
print("Project name detected: " + projectName)

print("Changin output directory to www")
jsonContent["projects"][projectName]["architect"]["build"]["options"]["outputPath"] = "www"

s = json.dumps(jsonContent, indent=4).replace('\'', "\"").replace("True", "true").replace("False", "false")

print("Writing to " + fileName)
file = open(fileName, "w")
file.write(s)
file.close()
print("Write successful")

# UPDATE GITIGNORE
linesToWrite = ["/www", "/platforms", "/plugins"]

file = open(".gitignore", "r")

for line in file.readlines():
    line = line.replace("\n", "").replace("\r", "")
    if line in linesToWrite:
        print(line + " was already in the .gitignore file")
        linesToWrite.remove(line)

file.close()

if linesToWrite.__len__() == 0:
    print(".gitignore is already up to date")

else:
    print("Updating .gitignore")
    file = open(".gitignore", "a")
    file.write("\n")
    for s in linesToWrite:
        file.write("\n" + s)
        print("Added " + s)

file.close()
print("done updating .gitignore")

# SETUP OF NODE AND CORDOVA
randomName = str(random.randint(1, 1000000))
print("Creating cordova project in folder " + randomName)
os.system("cordova create " + randomName)
configPath = "./" + randomName + "/config.xml"
print("Copying config.xml")
copyfile(configPath, "config.xml")
print("Deleting folder " + randomName)
rmtree(randomName)

print("Installing node modules")
os.system("npm install")

print("Building angular project")
os.system("ng build --prod")

print("Installing platforms cordova")
os.system("cordova platforms add android")
os.system("cordova platforms add ios")
os.system("cordova platforms add browser")

print("Building cordova")
os.system("cordova build")

print("Running on ios emulator")
os.system("cordova run ios")