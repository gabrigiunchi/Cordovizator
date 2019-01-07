import os

class ProjectManager:
    def __init__(self, src):
        self.src = src

    def cloneProject(self, path):
        os.system("git clone " + self.src + " " + path)

    def getProjectName(self):
        return self.src.split("/")[-1].split(".")[0]