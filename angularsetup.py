import constants
import iomanager as io
import json
import os

class AngularSetup:

    def setup(self):
        self.updateIndexHTML()
        self.updateOutputPath()

    def updateIndexHTML(self):
        print("Updating index.html")

        filePath = constants.INDEX_HTML_PATH

        content = io.readFromFile(filePath)
        content = content.replace("""<base href="/">""", """<base href="./">""")
        content = content.replace("<head>\n", 
            """<head>\n\t<script type="text/javascript" charset="utf-8" src="cordova.js"></script>\n""")

        io.writeToFile(filePath, content)

    
    def updateOutputPath(self):
        print("Updating angular.json")
        
        projectName = self.getProjectName()
        print("Project name detected: " + projectName)

        filePath = constants.ANGULAR_JSON_PATH

        print("Changin output path to " + constants.OUTPUT_PATH)
        jsonContent = json.loads(io.readFromFile(filePath))
        jsonContent["projects"][projectName]["architect"]["build"]["options"]["outputPath"] = constants.OUTPUT_PATH
        s = json.dumps(jsonContent, indent=4).replace('\'', "\"").replace("True", "true").replace("False", "false")

        io.writeToFile(filePath, s)

    def getProjectName(self):
        content = io.readFromFile(constants.ANGULAR_JSON_PATH)
        jsonContent = json.loads(content)
        keys = jsonContent["projects"].keys()
        projectName = next(iter(keys))
        return projectName

    def build(self):
        print("Installing node modules")
        os.system("npm install")
        print("Building angular project")
        os.system("ng build --prod")
