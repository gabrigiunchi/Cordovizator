import os
import constants
import iomanager as io
import xml.etree.ElementTree as ET
from shutil import copyfile

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
        print("Updating .gitignore")
        content = "\n\n#CORDOVA"
        for entry in constants.GIT_IGNORE_ENTRIES:
            content += "\n" + entry

        io.appendToFile(self.destDirectory + "/" + constants.GIT_IGNORE_PATH, content)

    def copyConfigFile(self):
        print("Copying cordova configuration file")
        dest = self.destDirectory + "/" + constants.CORDOVA_CONFIG_DEST_PATH
        copyfile(constants.CORDOVA_CONFIG_SOURCE_PATH, dest)