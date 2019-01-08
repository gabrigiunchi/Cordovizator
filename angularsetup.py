import constants
import iomanager as io
import json
import os
from shutil import copytree

class AngularSetup:

    def __init__(self, directory):
        self.destDirectory = directory

    def setup(self):
        self.updateIndexHTML()
        self.updateOutputPath()
        self.copyAndroidIconsFolder()
        self.copyIosIconsFolder()

    def copyAndroidIconsFolder(self):
        print("Copying android icons")
        dest = self.destDirectory + "/" + constants.ANDROID_ICON_DEST_PATH

        if os.path.isdir(dest):
            print("Android icons already exist")
        
        else:
            copytree(constants.ANDROID_ICON_SOURCE_PATH, dest)

    def copyIosIconsFolder(self):
        print("Copying IOS icons")
        dest = self.destDirectory + "/" + constants.IOS_ICON_DEST_PATH

        if os.path.isdir(dest):
            print("IOS icons already exist")
        
        else:
            copytree(constants.IOS_ICON_SOURCE_PATH, dest)

    def updateIndexHTML(self):
        print("Updating index.html")

        filePath = self.destDirectory + "/" + constants.INDEX_HTML_PATH

        content = io.readFromFile(filePath)
        content = content.replace("""<base href="/">""", """<base href="./">""")
        content = content.replace("<head>\n", """<head>\n\t<script type="text/javascript" charset="utf-8" src="cordova.js"></script>\n""")

        io.writeToFile(filePath, content)

    def updateOutputPath(self):
        print("Updating angular.json")

        projectName = self.getProjectName()
        print("Project name detected: " + projectName)

        filePath = self.destDirectory + "/" + constants.ANGULAR_JSON_PATH

        print("Changin output path to " + constants.ANGULAR_OUTPUT_PATH)
        jsonContent = json.loads(io.readFromFile(filePath))
        jsonContent["projects"][projectName]["architect"]["build"]["options"]["outputPath"] = constants.ANGULAR_OUTPUT_PATH
        s = json.dumps(jsonContent, indent=4).replace('\'', "\"").replace("True", "true").replace("False", "false")

        io.writeToFile(filePath, s)

    def getProjectName(self):
        content = io.readFromFile(self.destDirectory + "/" + constants.ANGULAR_JSON_PATH)
        jsonContent = json.loads(content)
        keys = jsonContent["projects"].keys()
        return next(iter(keys))

    def build(self):
        print("Installing node modules")
        os.system("npm install")
        print("Building angular project")
        os.system("ng build --prod")
