import os
from shutil import copyfile, rmtree
import random
import constants
import iomanager as io
import xml.etree.ElementTree as ET

class CordovaSetup:

        def setup(self):
                self.updateGitIgnore()
                self.updateProjectInfo()

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

        def updateProjectInfo(self):
                self._copyConfigXML()

                ET.register_namespace("", "http://www.w3.org/ns/widgets")
                tree = ET.parse(constants.CORDOVA_CONFIG_PATH)
                root = tree.getroot()

                namespace = "{http://www.w3.org/ns/widgets}"

                for child in root.iter(f"{namespace}widget"):
                        child.attrib["id"] = constants.CORDOVA_WIDGET_ID

                for child in root.iter(f"{namespace}name"):
                        child.text = constants.CORDOVA_PROJECT_NAME

                for child in root.findall(f"{namespace}author"):
                        child.text = constants.CORDOVA_AUTHOR
                        child.attrib.pop("email")
                        child.attrib.pop("href")

                for child in root.findall(f"{namespace}description"):
                        root.remove(child)

                icon = ET.Element("icon")
                icon.attrib["src"] = constants.CORDOVA_ICON_PATH
                root.insert(0, icon)

                tree.write(constants.CORDOVA_CONFIG_PATH, xml_declaration="true", encoding="utf-8", method="xml")

        def _copyConfigXML(self):
                randomName = str(random.randint(1, 1000000))
                print("Creating cordova project in folder " + randomName)
                os.system("cordova create " + randomName)
                configPath = "./" + randomName + "/" + constants.CORDOVA_CONFIG_PATH
                print("Copying cordova configuration file")
                copyfile(configPath, constants.CORDOVA_CONFIG_PATH)
                print("Deleting folder " + randomName)
                rmtree(randomName)