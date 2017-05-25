
from PyQt4.QtGui import QMessageBox
from ProjectManager.AppSetting import AppSetting
from ProjectManager.UserList import UserList
from ProjectManager.ProjectInfo import ProjectList


class AirCraftOperation:
    userList = UserList()
    loginedUser = None
    g_projectList = ProjectList()

    currentProject = None
    currentSubproject = None
    currentWorkspace = None
    currentProcedure = None
    currentAIP = None

    ApplicationSetting = AppSetting()

    def __init__(self):
        pass

    @staticmethod
    def SelectProjectFolder(folder):
        AirCraftOperation.loginedUser = None
        AirCraftOperation.currentProcedure = None
        AirCraftOperation.currentProject = None
        AirCraftOperation.currentSubproject = None
        AirCraftOperation.currentWorkspace = None
        AirCraftOperation.userList.ListUserInfo = []
        AirCraftOperation.g_projectList.ProjectsList = []

        AirCraftOperation.ApplicationSetting.ProjectFolderPath = folder
        AirCraftOperation.userList.SetUserInfoPath(folder)
        AirCraftOperation.g_projectList.SetProjectInfoPath(folder)

        if AirCraftOperation.userList.ReadUserInfoFile():
            if len(AirCraftOperation.userList.ListUserInfo) > 0:
                AirCraftOperation.g_projectList = ProjectList()
                AirCraftOperation.g_projectList.SetProjectInfoPath(AirCraftOperation.ApplicationSetting.ProjectFolderPath)

                if not AirCraftOperation.g_projectList.ReadProjectInfoXml():
                    QMessageBox.warning(None, "Warning", "Project information file is not exist! Please create project.")
            else:
                QMessageBox.warning(None, "Warning", "User information file dose not contain any user!")
