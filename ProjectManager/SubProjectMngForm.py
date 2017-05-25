from PyQt4.QtGui import QDialog, QPushButton, QVBoxLayout, QFont, QFileDialog, QMessageBox, QIcon
from PyQt4.QtCore import SIGNAL, QDir
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel

from ProjectManager.ProjectInfo import enumProjectType
from ProjectManager.ProjectInfo import ProjectInfo
from AircraftOperation import AirCraftOperation
import define


class SubProjectMngForm(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setObjectName("ui_SubProjectMngForm")
        self.resize(200, 200)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.vlForm = QVBoxLayout(self)
        self.vlForm.setObjectName("vl_ProjectMngForm")
        self.vlForm.setSpacing(9)
        self.vlForm.setMargin(9)

        self.setWindowTitle("SubProject Manage Dialog")

        self.basicFrame = Frame(self)
        self.vlForm.addWidget(self.basicFrame)

        self.frameName = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.frameName

        self.frame = Frame(self.frameName)
        self.frameName.Add = self.frame

        self.comboProjectSubproject = ComboBoxPanel(self.frame)
        self.comboProjectSubproject.Caption = "Project"
        self.comboProjectSubproject.LabelWidth = 120
        self.frame.Add = self.comboProjectSubproject

        self.textNameSubproject = TextBoxPanel(self.frame)
        self.textNameSubproject.Caption = "Sub-Project Name"
        self.textNameSubproject.LabelWidth = 120
        self.textNameSubproject.Width = 120
        self.frame.Add = self.textNameSubproject

        self.textFullName = TextBoxPanel(self.frame)
        self.textFullName.Caption = "Full Name"
        self.textFullName.LabelWidth = 120
        self.textFullName.Width = 120
        self.textFullName.Visible = False
        self.frame.Add = self.textFullName

        self.groubox = GroupBox(self.frameName)
        self.groubox.Caption = "Sub-Projects"
        self.frameName.Add = self.groubox

        self.listBoxSubproject = ListBox(self.groubox)
        self.groubox.Add = self.listBoxSubproject

        self.textPathSubproject = TextBoxPanel(self.basicFrame)
        self.textPathSubproject.Caption = "Sub-Project Path"
        self.textPathSubproject.imageButton.setIcon(QIcon())
        self.textPathSubproject.Button = "opens.png"
        self.textPathSubproject.LabelWidth = 120

        self.textPathSubproject.textBox.setMaximumWidth(10000)
        self.textPathSubproject.textBox.setMinimumWidth(100)
        self.basicFrame.Add = self.textPathSubproject

        self.btnFrame = Frame(self.basicFrame, "HL")
        self.basicFrame.Add = self.btnFrame

        self.buttonAddSubproject = QPushButton(self.btnFrame)
        self.buttonAddSubproject.setObjectName("buttonAddSubproject")
        self.buttonAddSubproject.setText("Add")
        self.btnFrame.Add = self.buttonAddSubproject

        self.buttonModifySubproject = QPushButton(self.btnFrame)
        self.buttonModifySubproject.setObjectName("buttonModifySubproject")
        self.buttonModifySubproject.setText("Modify")
        self.btnFrame.Add = self.buttonModifySubproject

        self.buttonDeleteSubproject = QPushButton(self.btnFrame)
        self.buttonDeleteSubproject.setObjectName("buttonDeleteSubproject")
        self.buttonDeleteSubproject.setText("Delete")
        self.btnFrame.Add = self.buttonDeleteSubproject

        self.buttonCloseSubproject = QPushButton(self.btnFrame)
        self.buttonCloseSubproject.setObjectName("buttonCloseSubproject")
        self.buttonCloseSubproject.setText("Close")
        self.btnFrame.Add = self.buttonCloseSubproject

        self.connect(self.listBoxSubproject, SIGNAL("Event_0"), self.listBoxSubproject_SelectedIndexChanged)
        self.connect(self.textPathSubproject, SIGNAL("Event_1"), self.buttonBrowseSubproject_Click)

        self.connect(self.textNameSubproject, SIGNAL("Event_0"), self.setFullName)
        self.connect(self.comboProjectSubproject, SIGNAL("Event_0"), self.setFullNameProjectNameChanged)

        self.buttonCloseSubproject.clicked.connect(self.buttonCloseSubproject_Click)
        self.buttonDeleteSubproject.clicked.connect(self.buttonDeleteSubproject_Click)
        self.buttonModifySubproject.clicked.connect(self.buttonModifySubproject_Click)
        self.buttonAddSubproject.clicked.connect(self.buttonAddSubproject_Click)
        self.editFlag = True

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if pi.Pt == enumProjectType.ptSubProject:
                self.listBoxSubproject.Add(pi.Name)
            elif pi.Pt == enumProjectType.ptProject:
                self.comboProjectSubproject.Add(pi.Name)

        self.editFlag = False
        self.setFullNameProjectNameChanged()

    def setFullName(self):
        if self.editFlag:
            return

        if self.comboProjectSubproject.Count <= 0:
            return

        self.editFlag = True

        index = AirCraftOperation.g_projectList.Find(self.comboProjectSubproject.SelectedItem, enumProjectType.ptProject)
        projPath = AirCraftOperation.g_projectList.ProjectsList[index].Path
        self.textFullName.Value = self.comboProjectSubproject.SelectedItem + "_" + self.textNameSubproject.Value
        self.textPathSubproject.Value = projPath + "/" + self.textNameSubproject.Value

        self.editFlag = False

    def setFullNameProjectNameChanged(self):
        if self.editFlag:
            return

        self.editFlag = True

        index = AirCraftOperation.g_projectList.Find(self.comboProjectSubproject.SelectedItem, enumProjectType.ptProject)

        if index is None:
            self.editFlag = False
            return

        projPath = AirCraftOperation.g_projectList.ProjectsList[index].Path
        d = QDir(projPath)
        fileInfoList = d.entryInfoList()

        self.listBoxSubproject.Clear()
        self.textNameSubproject.Value = ""

        piList = AirCraftOperation.g_projectList.FindProjectListByPt(enumProjectType.ptSubProject)

        if len(piList) == 0:
            self.editFlag = False
            self.textPathSubproject.Value = projPath + "/" + self.textNameSubproject.Value
            self.textFullName.Value = self.comboProjectSubproject.SelectedItem + "_" + self.textNameSubproject.Value
            return

        subProjNameList = []
        i = 0

        for pi in piList:
            if pi.ProjName == self.comboProjectSubproject.SelectedItem:
                subProjNameList.append(pi.SubProjName)
                self.listBoxSubproject.Add(pi.SubProjName)
            i += 1

        if len(subProjNameList) > 0:
            self.textNameSubproject.Value = subProjNameList[0]

        self.textFullName.Value = self.comboProjectSubproject.SelectedItem + "_" + self.textNameSubproject.Value

        self.textPathSubproject.Value = projPath + "/" + self.textNameSubproject.Value
        self.editFlag = False

    def CheckInputValues(self):
        if self.textNameSubproject.Text is None or self.textNameSubproject.Text == "":
            QMessageBox.warning(self, "Warning", "Please input project name!")
            return False

        if self.textPathSubproject.Text is None or self.textPathSubproject.Text == "":
            QMessageBox.warning(self, "Warning", "Please input project path!")
            return False

        if self.comboProjectSubproject.SelectedIndex < 0:
            QMessageBox.warning(self, "Warning", "Please select an project!")
            return False

        directory = QDir(self.textPathSubproject.Text)

        if not directory.exists():
            if QMessageBox.question(self, "Question", "Procedure path dose not exist! Do you create the directory?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                directory.mkpath(self.textPathSubproject.Text)
            else:
                return False

        return True
    
    def listBoxSubproject_SelectedIndexChanged(self):
        if self.listBoxSubproject.SelectedIndex < 0:
            return

        self.textFullName.Value = self.comboProjectSubproject.SelectedItem + "_" + self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex]
        pi = AirCraftOperation.g_projectList.Find(self.textFullName.Value)
        self.textNameSubproject.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Name
        self.textPathSubproject.Text = AirCraftOperation.g_projectList.ProjectsList[pi].Path
        self.comboProjectSubproject.SelectedIndex = self.comboProjectSubproject.IndexOf(AirCraftOperation.g_projectList.ProjectsList[pi].ProjName)

    def buttonBrowseSubproject_Click(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Open Project Path", define.projectManageDir)

        if folderPath is not None and folderPath != "":
            self.textPathSubproject.Value = folderPath
            define.projectManageDir = folderPath

    def buttonCloseSubproject_Click(self):
        res = QMessageBox.question(self, "Question", "Save changes to project information?", QMessageBox.Yes | QMessageBox.No)

        if res == QMessageBox.Yes:
            AirCraftOperation.g_projectList.WriteProjectInfoXml()

        self.accept()
    
    def buttonAddSubproject_Click(self):
        if not self.CheckInputValues():
            return

        if AirCraftOperation.g_projectList.Find(self.textFullName.Text) is not None:
            QMessageBox.warning(self, "Warning", "The same sub-project exist!")
            return

        pi = ProjectInfo()
        pi.Pt = enumProjectType.ptSubProject
        pi.Name = self.textNameSubproject.Text
        pi.SubProjName = self.textNameSubproject.Text
        pi.Path = self.textPathSubproject.Text
        pi.ProjName = self.comboProjectSubproject.SelectedItem
        pi.UserName = AirCraftOperation.loginedUser.Name
        pi.FullName = self.textFullName.Value

        AirCraftOperation.g_projectList.Add(pi)

        nIndex = self.listBoxSubproject.Add(pi.Name)
        self.listBoxSubproject.SelectedIndex = nIndex

    def buttonModifySubproject_Click(self):
        if self.listBoxSubproject.SelectedIndex < 0:
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return

        if not self.CheckInputValues():
            return

        index = AirCraftOperation.g_projectList.Find(self.comboProjectSubproject.SelectedItem + "_" + self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex])
        AirCraftOperation.g_projectList.ProjectsList[index].Pt = enumProjectType.ptSubProject
        AirCraftOperation.g_projectList.ProjectsList[index].Name = self.textNameSubproject.Text
        AirCraftOperation.g_projectList.ProjectsList[index].SubProjName = self.textNameSubproject.Text
        AirCraftOperation.g_projectList.ProjectsList[index].Path = self.textPathSubproject.Text
        AirCraftOperation.g_projectList.ProjectsList[index].ProjName = self.comboProjectSubproject.SelectedItem
        AirCraftOperation.g_projectList.ProjectsList[index].UserName = AirCraftOperation.loginedUser.Name
        AirCraftOperation.g_projectList.ProjectsList[index].FullName = self.textFullName.Value

        self.listBoxSubproject.Clear()

        for pi in AirCraftOperation.g_projectList.ProjectsList:
            if pi.Pt == enumProjectType.ptSubProject:
                self.listBoxSubproject.Add(pi.Name)

    def buttonDeleteSubproject_Click(self):
        if self.listBoxSubproject.SelectedIndex < 0:
            QMessageBox.warning(self, "Warning", "Please select project in the projects list!")
            return

        if QMessageBox.question(self, "Question", "Are you sure to delete " + self.listBoxSubproject.Items[self.listBoxSubproject.SelectedIndex] + "?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return

        AirCraftOperation.g_projectList.Remove(self.textFullName.Value)

        self.listBoxSubproject.Clear()

        self.setFullNameProjectNameChanged()

        AirCraftOperation.g_projectList.WriteProjectInfoXml()