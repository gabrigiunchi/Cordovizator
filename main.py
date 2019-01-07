import os
import cordovasetup
import projectmanager as pm
import sys
import angularsetup
import constants

src = constants.DEFAULT_GIT_SRC

if sys.argv.__len__() == 2:
    src = sys.argv[1]

projectManager = pm.ProjectManager(src)

if sys.argv.__len__() > 2:
    directory = sys.argv[2]

else:
    directory = "../" + projectManager.getProjectName()

projectManager.cloneProject(directory)
os.chdir(directory)

angularSetup = angularsetup.AngularSetup()
cordovaSetup = cordovasetup.CordovaSetup()

angularSetup.updateIndexHTML()
angularSetup.updateOutputPath()

cordovaSetup.updateProjectInfo()
cordovaSetup.updateGitIgnore()

angularSetup.build()
cordovaSetup.installPlatforms()
cordovaSetup.build()