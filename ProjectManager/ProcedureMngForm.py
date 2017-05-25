

from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QIcon
from PyQt4.QtCore import SIGNAL, QFileInfo, QDir
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel

from ProjectManager.ProjectInfo import enumProjectType
from ProjectManager.ProjectInfo import ProjectInfo, ProjectList
from AircraftOperation import AirCraftOperation
import define

class ProcedureMngForm(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.setObjectName(("ui_ProcedureMngForm"))
        self.resize(200, 200)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.setWindowTitle("Procedure Manage Dialog")

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName(("vl_ProceduretMngForm"))
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.frameName = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.frameName

        self.frame = Frame(self.frameName)
        self.frameName.Add = self.frame

        self.comboProjectProcedure = ComboBoxPanel(self.frame)
        self.comboProjectProcedure.Caption = "Project"
        self.comboProjectProcedure.LabelWidth = 120
        self.frame.Add = self.comboProjectProcedure

        self.comboSubProjectProcedure = ComboBoxPanel(self.frame)
        self.comboSubProjectProcedure.Caption = "Sub-Project"
        self.comboSubProjectProcedure.LabelWidth = 120
        self.frame.Add = self.comboSubProjectProcedure

        self.comboWorkspaceProcedure = ComboBoxPanel(self.frame)
        self.comboWorkspaceProcedure.Caption = "Workspace"
        self.comboWorkspaceProcedure.LabelWidth = 120
        self.frame.Add = self.comboWorkspaceProcedure

        self.textNameProcedure = TextBoxPanel(self.frame)
        self.textNameProcedure.Caption = "Procedure Name"
        self.textNameProcedure.LabelWidth = 120
        self.textNameProcedure.Width = 120
        self.frame.Add = self.textNameProcedure

        self.textFullName = TextBoxPanel(self.frame)
        self.textFullName.Caption = "Full Name"
        self.textFullName.LabelWidth = 120
        self.textFullName.Width = 120
        self.textFullName.Visible = False
        self.frame.Add = self.textFullName

        self.groubox = GroupBox(self.frameName)
        self.groubox.Caption = "Procedures"
        self.frameName.Add = self.groubox

        self.listBoxProcedure = ListBox(self.groubox)
        self.groubox.Add = self.listBoxProcedure

        self.textPathProcedure = TextBoxPanel(self.basicFrame)
        self.textPathProcedure.Caption = "Procedure Path"
        self.textPathProcedure.imageButton.setIcon(QIcon())
        self.textPathProcedure.Button = "opens.png"
        self.textPathProcedure.LabelWidth = 120
        self.textPathProcedure.textBox.setMaximumWidth(10000)
        self.textPathProcedure.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathProcedure

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddProcedure = QPushButton(self.btnFrame)
        self.buttonAddProcedure.setObjectName("buttonAddProcedure")
        self.buttonAddProcedure.setText("Add")
        self.btnFrame.Add = self.buttonAddProcedure

        self.buttonModifyProcedure = QPushButton(self.btnFrame)
        self.buttonModifyProcedure.setObjectName("buttonModifyProcedure")
        self.buttonModifyProcedure.setText("Modify")
        self.btnFrame.Add = self.buttonModifyProcedure

        self.buttonDeleteProcedure = QPushButton(self.btnFrame)
        self.buttonDeleteProcedure.setObjectName("buttonDeleteProcedure")
        self.buttonDeleteProcedure.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteProcedure

        self.buttonSaveProcedure = QPushButton(self.btnFrame)
        self.buttonSaveProcedure.setObjectName("buttonSaveProcedure")
        self.buttonSaveProcedure.setText("Save")
        self.buttonSaveProcedure.setVisible(False)
        self.btnFrame.Add = self.buttonSaveProcedure

        self.buttonCloseProcedure = QPushButton(self.btnFrame)
        self.buttonCloseProcedure.setObjectName("buttonCloseProcedure")
        self.buttonCloseProcedure.setText("Close")
        self.btnFrame.Add = self.buttonCloseProcedure

        self.connect(self.listBoxProcedure, SIGNAL("Event_0"), self.listBoxProcedure_SelectedIndexChanged)
        self.connect(self.comboProjectProcedure, SIGNAL("Event_0"), self.comboProjectProcedure_SelectedIndexChanged)
        self.connect(self.comboSubProjectProcedure, SIGNAL("Event_0"), self.comboSubProjectProcedure_SelectedIndexChanged)
        self.connect(self.textPathProcedure, SIGNAL("Event_1"), self.buttonBrowseWorkspace_Click)
        self.connect(self.comboWorkspaceProcedure, SIGNAL("Event_0"), self.comboWorkspaceProcedure_SelectedIndexChanged)
        self.connect(self.textNameProcedure, SIGNAL("Event_0"), self.setFullName)

        self.buttonCloseProcedure.clicked.connect(self.buttonCloseProcedure_Click)
        self.buttonSaveProcedure.clicked.connect(self.buttonSaveProcedure_Click)
        self.buttonDeleteProcedure.clicked.connect(self.buttonDeleteProcedure_Click)
        self.buttonModifyProcedure.clicked.connect(self.buttonModifyProcedure_Click)
        self.buttonAddProcedure.clicked.connect(self.buttonAddProcedure_Click)
        self.editFlag = True
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if (pi.Pt == enumProjectType.ptFile):
                self.listBoxProcedure.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptProject):
                self.comboProjectProcedure.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptSubProject):
                self.comboSubProjectProcedure.Add(pi.Name)
            elif (pi.Pt == enumProjectType.ptWorkspace):
                self.comboWorkspaceProcedure.Add(pi.Name)
        self.editFlag = False
        self.comboProjectProcedure_SelectedIndexChanged()

    def setFullName(self):
        if self.editFlag:
            return
        self.editFlag = True

        index = AirCraftOperation.g_projectList.GetIndexOfWsOrProcedure(enumProjectType.ptWorkspace,
                                                                        self.comboProjectProcedure.SelectedItem,
                                                                        self.comboSubProjectProcedure.SelectedItem,
                                                                        self.comboWorkspaceProcedure.SelectedItem)
        if index == None:
            self.editFlag = False
            return
        projPath = AirCraftOperation.g_projectList.ProjectsList[index].Path
        self.textFullName.Value = self.comboProjectProcedure.SelectedItem + "_" + self.comboSubProjectProcedure.SelectedItem + "_" + self.comboWorkspaceProcedure.SelectedItem + "_" + self.textNameProcedure.Text

        self.textPathProcedure.Value = projPath + "/" + self.textNameProcedure.Value

        self.editFlag = False

    
    def CheckInputValues(self):
        if (self.textNameProcedure.Text == None or self.textNameProcedure.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return False
        if (self.textPathProcedure.Text == None or self.textPathProcedure.Text == ""):
            QMessageBox.warning(self, "Warning", "Please input project path!")
            return False
        if (self.comboProjectProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Project!")
            return False
        if (self.comboSubProjectProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Sub-Project!")
            return False
        if (self.comboWorkspaceProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select an Workspace!")
            return
        directory = QDir(self.textPathProcedure.Text)
        if (not directory.exists()):
            if (QMessageBox.question(self, "Question", "Procedure path dose not exist! Do you create the directory?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
                directory.mkpath(self.textPathProcedure.Text)
            else:
                return False
        return True

    def listBoxProcedure_SelectedIndexChanged(self):
        if (self.listBoxProcedure.SelectedIndex < 0):
            return
        pi = AirCraftOperation.g_projectList.Find(self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex])

        pi = AirCraftOperation.g_projectList.GetIndexOfWsOrProcedure(enumProjectType.ptFile,
                                                                     self.comboProjectProcedure.SelectedItem,
                                                                     self.comboSubProjectProcedure.SelectedItem,
                                                                     self.comboWorkspaceProcedure.SelectedItem,
                                                                     self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex])
        if pi == None:
            return
        self.textNameProcedure.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Name
        self.textPathProcedure.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Path

        self.comboProjectProcedure.SelectedIndex = self.comboProjectProcedure.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].ProjName)
        self.comboSubProjectProcedure.SelectedIndex = self.comboSubProjectProcedure.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].SubProjName)
        self.comboWorkspaceProcedure.SelectedIndex = self.comboWorkspaceProcedure.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].WorkspaceName)

    def buttonBrowseWorkspace_Click(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Project Path", define.projectManageDir)
        if (folderPath != None and folderPath != ""):
            self.textPathProcedure.Value = folderPath
            define.projectManageDir = folderPath

    def buttonSaveProcedure_Click(self):
        res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        if (res == QMessageBox.Yes):
            AirCraftOperation.g_projectList.WriteProjectInfoXml()
            self.buttonSaveProcedure.setEnabled(False)

    def buttonCloseProcedure_Click(self):
        res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)
        if (res == QMessageBox.Yes):
            AirCraftOperation.g_projectList.WriteProjectInfoXml()
            self.buttonSaveProcedure.setEnabled(False)
        self.accept()

    def buttonAddProcedure_Click(self):
        if (not self.CheckInputValues()):
            return

        index = AirCraftOperation.g_projectList.GetIndexOfWsOrProcedure(enumProjectType.ptFile,
                                                                        self.comboProjectProcedure.SelectedItem,
                                                                        self.comboSubProjectProcedure.SelectedItem,
                                                                        self.comboWorkspaceProcedure.SelectedItem,
                                                                        self.textNameProcedure.Text)

        if (index != None):
            QMessageBox.warning(self, "Warning", "The same name exist!")
            return
        pi = ProjectInfo()
        pi.Pt = enumProjectType.ptFile
        pi.Name = self.textNameProcedure.Text
        pi.ProcedureName = self.textNameProcedure.Text
        pi.Path = self.textPathProcedure.Text
        pi.ProjName = self.comboProjectProcedure.SelectedItem
        pi.SubProjName = self.comboSubProjectProcedure.SelectedItem
        pi.WorkspaceName = self.comboWorkspaceProcedure.SelectedItem
        pi.FullName = self.textFullName.Text
        pi.UserName = AirCraftOperation.loginedUser.Name

        AirCraftOperation.g_projectList.Add(pi)

        nIndex = self.listBoxProcedure.Add(pi.Name)
        self.listBoxProcedure.SelectedIndex = nIndex
        self.buttonSaveProcedure.setEnabled(True)

    def buttonModifyProcedure_Click(self):
        if (self.listBoxProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return
        if (not self.CheckInputValues()):
            return
        index = AirCraftOperation.g_projectList.GetIndexOfWsOrProcedure(enumProjectType.ptFile,
                                                                        self.comboProjectProcedure.SelectedItem,
                                                                        self.comboSubProjectProcedure.SelectedItem,
                                                                        self.comboWorkspaceProcedure.SelectedItem,
                                                                        self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex])

        AirCraftOperation.g_projectList.ProjectsList[index].Pt = enumProjectType.ptFile
        AirCraftOperation.g_projectList.ProjectsList[index].Name = self.textNameProcedure.Text
        AirCraftOperation.g_projectList.ProjectsList[index].ProcedureName = self.textNameProcedure.Text
        AirCraftOperation.g_projectList.ProjectsList[index].Path = self.textPathProcedure.Text
        AirCraftOperation.g_projectList.ProjectsList[index].ProjName = self.comboProjectProcedure.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].SubProjName = self.comboSubProjectProcedure.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].WorkspaceName = self.comboWorkspaceProcedure.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].FullName = self.textFullName.Text
        AirCraftOperation.g_projectList.ProjectsList[index].UserName = AirCraftOperation.loginedUser.Name

        self.listBoxProcedure.Clear()
        self.comboProjectProcedure_SelectedIndexChanged()
        # for pi in AirCraftOperation.g_projectList.ProjectsList:
        #     if (pi.Pt == enumProjectType.ptFile):
        #         self.listBoxProcedure.Add(pi.Name)

        # AirCraftOperation.g_projectList.Remove(pi)
        #
        # AirCraftOperation.g_projectList.Add(pi)
        self.buttonSaveProcedure.setEnabled(True)

    def buttonDeleteProcedure_Click(self):
        if (self.listBoxProcedure.SelectedIndex < 0):
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return

        if (QMessageBox.question(self, "Question", "Are you sure to delete " + self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex] + "?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return
        index = AirCraftOperation.g_projectList.GetIndexOfWsOrProcedure(enumProjectType.ptFile,
                                                                        self.comboProjectProcedure.SelectedItem,
                                                                        self.comboSubProjectProcedure.SelectedItem,
                                                                        self.comboWorkspaceProcedure.SelectedItem,
                                                                        self.listBoxProcedure.Items[self.listBoxProcedure.SelectedIndex])
        AirCraftOperation.g_projectList.Remove(index)
        self.buttonSaveProcedure.setEnabled(True)
        self.listBoxProcedure.Clear()
        self.comboProjectProcedure_SelectedIndexChanged()
        AirCraftOperation.g_projectList.WriteProjectInfoXml()
        # for pi in AirCraftOperation.g_projectList.ProjectsList:
        #     if (pi.Pt == enumProjectType.ptFile):
        #         self.listBoxProcedure.Add(pi.Name)

    def comboProjectProcedure_SelectedIndexChanged(self):
        if self.editFlag:
            return
        listSubprojects = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboProjectProcedure.SelectedItem,
                                                                            enumProjectType.ptProject,
                                                                            enumProjectType.ptSubProject)
        self.editFlag = True
        self.comboSubProjectProcedure.Clear()
        if (listSubprojects != None and len(listSubprojects) > 0):
            self.comboSubProjectProcedure.Items = listSubprojects
            self.comboSubProjectProcedure.SelectedIndex = 0
        self.editFlag = False
        self.comboSubProjectProcedure_SelectedIndexChanged()

    def comboSubProjectProcedure_SelectedIndexChanged(self):
        if self.editFlag:
            return
        listWorkspaceList = AirCraftOperation.g_projectList.GetListOfWsOrProcedure(enumProjectType.ptWorkspace,
                                                                                   self.comboProjectProcedure.SelectedItem,
                                                                                   self.comboSubProjectProcedure.SelectedItem)
        self.editFlag = True
        self.comboWorkspaceProcedure.Clear()
        if (listWorkspaceList != None and len(listWorkspaceList) > 0):
            self.comboWorkspaceProcedure.Items = listWorkspaceList
            self.comboWorkspaceProcedure.SelectedIndex = 0
        self.editFlag = False
        self.comboWorkspaceProcedure_SelectedIndexChanged()

    def comboWorkspaceProcedure_SelectedIndexChanged(self):
        if self.editFlag:
            return
        listProcedureList = AirCraftOperation.g_projectList.GetListOfWsOrProcedure(enumProjectType.ptFile,
                                                                                   self.comboProjectProcedure.SelectedItem,
                                                                                   self.comboSubProjectProcedure.SelectedItem,
                                                                                   self.comboWorkspaceProcedure.SelectedItem)
        self.textNameProcedure.Text = ""
        self.listBoxProcedure.Clear()
        self.editFlag = True
        if len(listProcedureList) > 0:
            self.listBoxProcedure.Items = listProcedureList
            self.listBoxProcedure.SelectedIndex = 0
        self.editFlag = False
        self.setFullName()

    # def comboProjectProcedure_SelectedIndexChanged(self):
    #     listSubprojects = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboProjectProcedure.SelectedItem, enumProjectType.ptProject, enumProjectType.ptSubProject)
    #     self.comboSubProjectProcedure.Clear()
    #     if (listSubprojects != None and len(listSubprojects) > 0):
    #
    #         self.comboSubProjectProcedure.Items = listSubprojects
    #         self.comboSubProjectProcedure.SelectedIndex = 0
    #     self.comboSubProjectProcedure_SelectedIndexChanged()
    #
    # def comboSubProjectProcedure_SelectedIndexChanged(self):
    #     listWorkspace = AirCraftOperation.g_projectList.GetLinkedProjects(self.comboSubProjectProcedure.SelectedItem, enumProjectType.ptSubProject, enumProjectType.ptWorkspace)
    #     self.comboWorkspaceProcedure.Clear()
    #     if (listWorkspace != None and len(listWorkspace) > 0):
    #
    #         self.comboWorkspaceProcedure.Items = listWorkspace
    #         self.comboWorkspaceProcedure.SelectedIndex = 0