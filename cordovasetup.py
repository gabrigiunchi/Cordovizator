import os
import constants
import iomanager as io
import xml.etree.ElementTree as ET

class CordovaSetup:

    def __init__(self, directory):
        self.destDirectory = directory

    def setup(self):
        self.updateGitIgnore()
        self.copyConfigFile()

    def installPlatforms(self):
        for p in constants.CORDOVA_PLATFORMS:
            os.system("cordova platforms add " + p)

    def build(self):
        os.system("cordova build")

    def updateGitIgnore(self):
        content = "\n\n#CORDOVA"
        for entry in constants.GIT_IGNORE_ENTRIES:
            content += "\n" + entry

        io.appendToFile(self.destDirectory + "/" + constants.GIT_IGNORE_PATH, content)
        print("done updating .gitignore")

    def copyConfigFile(self):
        print("Copying cordova configuration file")
        tree = self.__updateConfigFile()
        dest = self.destDirectory + "/" + constants.CORDOVA_CONFIG_DEST_PATH
        tree.write(dest, xml_declaration="true", encoding="utf-8", method="xml")


    def __updateConfigFile(self):
        namespace = "{http://www.w3.org/ns/widgets}"
        ET.register_namespace("", "http://www.w3.org/ns/widgets")
        ET.register_namespace("android", "schemas.android.com/apk/res/android")
        ET.register_namespace("cdv", "http://cordova.apache.org/ns/1.0")
        
        tree = ET.parse(constants.CORDOVA_CONFIG_SOURCE_PATH)
        root = tree.getroot()

        root.attrib["id"] = constants.CORDOVA_WIDGET_ID

        root.find(f"{namespace}name").text = constants.CORDOVA_PROJECT_NAME

        author = root.find(f"{namespace}author")
        author.text = constants.CORDOVA_AUTHOR
        author.attrib.pop("email", None)
        author.attrib.pop("href", None)

        return tree
