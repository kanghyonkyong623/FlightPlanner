from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QIcon
from PyQt4.QtCore import SIGNAL, QDir
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame

from ProjectManager.ProjectInfo import enumProjectType
from ProjectManager.ProjectInfo import ProjectInfo
from AircraftOperation import AirCraftOperation
import define


class ProjectMngForm(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setObjectName("ui_ProjectMngForm")
        self.resize(200, 200)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.setWindowTitle("Project Manage Dialog")

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName("vl_ProjectMngForm")
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.groubox = GroupBox(self.basicFrame)
        self.groubox.Caption = "Projects"
        self.basicFrame.Add = self.groubox

        self.listBoxProject = ListBox(self.groubox)
        self.groubox.Add = self.listBoxProject

        self.textNameProject = TextBoxPanel(self.basicFrame)
        self.textNameProject.Caption = "Name"
        self.textNameProject.LabelWidth = 50
        self.textNameProject.Width = 120
        self.basicFrame.Add = self.textNameProject

        self.textPathProject = TextBoxPanel(self.basicFrame)
        self.textPathProject.Caption = "Path"
        self.textPathProject.imageButton.setIcon(QIcon())
        self.textPathProject.Button = "opens.png"
        self.textPathProject.LabelWidth = 50
        self.textPathProject.textBox.setMaximumWidth(10000)
        self.textPathProject.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathProject

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddProject = QPushButton(self.btnFrame)
        self.buttonAddProject.setObjectName("buttonAddProject")
        self.buttonAddProject.setText("Add")
        self.btnFrame.Add = self.buttonAddProject

        self.buttonModifyProject = QPushButton(self.btnFrame)
        self.buttonModifyProject.setObjectName("buttonModifyProject")
        self.buttonModifyProject.setText("Modify")
        self.btnFrame.Add = self.buttonModifyProject

        self.buttonDeleteProject = QPushButton(self.btnFrame)
        self.buttonDeleteProject.setObjectName("buttonDeleteProject")
        self.buttonDeleteProject.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteProject

        self.buttonCloseProject = QPushButton(self.btnFrame)
        self.buttonCloseProject.setObjectName("buttonCloseProject")
        self.buttonCloseProject.setText("Close")
        self.btnFrame.Add = self.buttonCloseProject

        self.connect(self.listBoxProject, SIGNAL("Event_0"), self.listBoxProject_SelectedIndexChanged)
        self.connect(self.textPathProject, SIGNAL("Event_1"), self.buttonBrowseProject_Click)

        self.buttonAddProject.clicked.connect(self.buttonAddProject_Click)
        self.buttonModifyProject.clicked.connect(self.buttonModifyProject_Click)
        self.buttonDeleteProject.clicked.connect(self.buttonDeleteProject_Click)
        self.buttonCloseProject.clicked.connect(self.buttonCloseProject_Click)
        
        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if pi.Pt == enumProjectType.ptProject:
                self.listBoxProject.Add(pi.Name)

    def buttonBrowseProject_Click(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Project Path", define.projectManageDir)
        if folderPath is not None and folderPath != "":
            self.textPathProject.Value = folderPath
            define.projectManageDir = folderPath

    def buttonAddProject_Click(self):
        try:
            if not self.CheckInputValues():
                return

            if AirCraftOperation.g_projectList.Find(self.textNameProject.Value) is not None:
                QMessageBox.warning(self, "Warning", "The same project exist!")
                return

            pi = ProjectInfo()
            pi.Pt = enumProjectType.ptProject
            pi.Name = self.textNameProject.Value
            pi.ProjName = self.textNameProject.Value
            pi.Path = self.textPathProject.Value
            pi.UserName = AirCraftOperation.loginedUser.Name
            pi.FullName = self.textNameProject.Value

            AirCraftOperation.g_projectList.Add(pi)

            nIndex = self.listBoxProject.Add(pi.Name)
            self.listBoxProject.SelectedIndex = nIndex
        except:#(System.Exception ex)
            # MessageBox.Show(ex.Message)
            pass

    def CheckInputValues(self):
        if self.textNameProject.Value is None or self.textNameProject.Value == "":
            raise "Please input project name!"

        if self.textPathProject.Value is None or self.textPathProject.Value == "":
            raise "Please input project path!"

        d = QDir(self.textPathProject.Value)

        if not d.exists():
            if QMessageBox.question(self, "Question", "Procedure path dose not exist! Do you create the directory?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                d = QDir(self.textPathProject.Value)
                d.mkpath(self.textPathProject.Value)
            else:
                return False
        return True

    def buttonModifyProject_Click(self):
        try:
            if self.listBoxProject.SelectedIndex < 0:
                raise "Please select project in the projects list!"

            if not self.CheckInputValues():
                return

            pi = ProjectInfo()
            pi.Pt = enumProjectType.ptProject
            pi.Name = self.textNameProject.Value
            pi.ProjName = self.textNameProject.Value
            pi.Path = self.textPathProject.Value
            pi.UserName = AirCraftOperation.loginedUser.Name
            pi.FullName = self.textNameProject.Value

            AirCraftOperation.g_projectList.Remove(self.listBoxProject.SelectedIndex)

            AirCraftOperation.g_projectList.Insert(self.listBoxProject.SelectedIndex, pi)
            self.listBoxProject.Clear()

            for pi in AirCraftOperation.g_projectList.ProjectsList:
                if pi.Pt == enumProjectType.ptProject:
                    self.listBoxProject.Add(pi.Name)
        except:
            # MessageBox.Show(ex.Message)
            pass

    def buttonDeleteProject_Click(self):
        try:
            if self.listBoxProject.SelectedIndex < 0:
                QMessageBox.warning (self, "Warning", "Please select project in the projects list!")
                return

            res = QMessageBox.question(self, "Alert", "Delete selected project?", QMessageBox.Yes | QMessageBox.No)

            if res == QMessageBox.No:
                return

            AirCraftOperation.g_projectList.Remove(self.listBoxProject.Items[self.listBoxProject.SelectedIndex])
            self.listBoxProject.Clear()
            self.textNameProject.Value = ""
            self.textPathProject.Value = ""

            for pi in AirCraftOperation.g_projectList.ProjectsList:
                if (pi.Pt == enumProjectType.ptProject):
                    self.listBoxProject.Add(pi.Name)

            AirCraftOperation.g_projectList.WriteProjectInfoXml()
        except:
            pass
            # MessageBox.Show(ex.Message)

    def listBoxProject_SelectedIndexChanged(self):
        try:
            if self.listBoxProject.SelectedIndex < 0:
                return

            i = AirCraftOperation.g_projectList.Find(self.listBoxProject.Items[self.listBoxProject.SelectedIndex])
            self.textNameProject.Value = AirCraftOperation.g_projectList.ProjectsList[i].Name
            self.textPathProject.Value = AirCraftOperation.g_projectList.ProjectsList[i].Path
        except:
            pass

    def buttonCloseProject_Click(self):
        AirCraftOperation.g_projectList.WriteProjectInfoXml()
        self.accept()
