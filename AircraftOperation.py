
from PyQt4.QtGui import QMessageBox
from ProjectManager.ProjectInfo import ProjectList


class AirCraftOperation:
    g_userList = None
    g_loginedUser = None
    g_projectList = None

    g_currentProject = None
    g_currentSubproject = None
    g_currentWorkspace = None
    g_currentProcedure = None
    g_currentAIP = None

    g_stateList = None
    g_aeroList = None
    g_runwayList = None
    g_AppSetting = None

    g_geoForms = []
    g_proForms = []

    g_snapping = True

    def __init__(self):
        pass

    @staticmethod
    def SelectProjectFolder(folder):
        AirCraftOperation.g_loginedUser = None
        AirCraftOperation.g_currentProcedure = None
        AirCraftOperation.g_currentProject = None
        AirCraftOperation.g_currentSubproject = None
        AirCraftOperation.g_currentWorkspace = None
        AirCraftOperation.g_userList.ListUserInfo = []
        AirCraftOperation.g_projectList.ProjectsList = []

        AirCraftOperation.g_AppSetting.ProjectFolderPath = folder
        AirCraftOperation.g_userList.SetUserInfoPath(folder)
        AirCraftOperation.g_projectList.SetProjectInfoPath(folder)

        if AirCraftOperation.g_userList.ReadUserInfoFile():
            if len(AirCraftOperation.g_userList.ListUserInfo) > 0:
                AirCraftOperation.g_projectList = ProjectList()
                AirCraftOperation.g_projectList.SetProjectInfoPath(AirCraftOperation.g_AppSetting.ProjectFolderPath)

                if not AirCraftOperation.g_projectList.ReadProjectInfoXml():
                    QMessageBox.warning(None, "Warning", "Project information file is not exist! Please create project.")
            else:
                QMessageBox.warning(None, "Warning", "User information file dose not contain any user!")
