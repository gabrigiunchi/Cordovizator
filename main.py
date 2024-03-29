import os
import sys
from projectmanager import ProjectManager
from angularsetup import AngularSetup
from cordovasetup import CordovaSetup
import constants

src = constants.DEFAULT_PROJECT_SRC

if sys.argv.__len__() == 2:
    src = sys.argv[1]

projectManager = ProjectManager(src)

if sys.argv.__len__() > 2:
    directory = sys.argv[2]

else:
    directory = "../" + projectManager.getProjectName()

projectManager.cloneProject(directory)

angularSetup = AngularSetup(directory)
cordovaSetup = CordovaSetup(directory)

angularSetup.setup()
cordovaSetup.setup()

os.chdir(directory)

angularSetup.build()
cordovaSetup.installPlatforms()
cordovaSetup.build()
