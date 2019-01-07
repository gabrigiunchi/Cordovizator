import os
from shutil import copyfile, rmtree
import random
import constants
import iomanager as io

class CordovaSetup:
        def installPlatforms(self):
                for p in constants.CORDOVA_PLATFORMS:
                        os.system("cordova platforms add " + p)

        def build(self):
                os.system("cordova build")

        def updateGitIgnore(self):
                content = "\n\n#CORDOVA"
                for entry in constants.GIT_IGNORE_ENTRIES:
                        content += "\n" + entry

                io.appendToFile(constants.GIT_IGNORE_PATH, content)
                print("done updating .gitignore")

        def copyConfigXML(self):
                randomName = str(random.randint(1, 1000000))
                print("Creating cordova project in folder " + randomName)
                os.system("cordova create " + randomName)
                configPath = "./" + randomName + "/" + constants.CORDOVA_CONFIG_PATH
                print("Copying config.xml")
                copyfile(configPath, constants.CORDOVA_CONFIG_PATH)
                print("Deleting folder " + randomName)
                rmtree(randomName)

        def updateProjectInfo(self):
