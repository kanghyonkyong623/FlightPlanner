from ui_RegProjectFolderForm import Ui_RegProjectFolderDialog

from PyQt4 import QtCore
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QString

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QListWidgetItem

from AircraftOperation import AirCraftOperation


class RegProjectFolderForm(QDialog):
    DataSeparator = QString("*")
    NamePathSeparator = QString("?")

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.ui = Ui_RegProjectFolderDialog()
        self.ui.setupUi(self)

        self.ui.pushButtonSelectFolder.setIcon(QApplication.style().standardIcon(QStyle.SP_DirOpenIcon))

        self.ui.listWidgetProjectFolder.currentItemChanged.connect(self.__listWidgetProjectFolder_currentItemChanged)
        self.ui.pushButtonSelectFolder.clicked.connect(self.__pushButtonSelectFolder_clicked)
        self.ui.pushButtonSelect.clicked.connect(self.__pushButtonSelect_clicked)
        self.ui.pushButtonAdd.clicked.connect(self.__pushButtonAdd_clicked)
        self.ui.pushButtonModify.clicked.connect(self.__pushButtonModify_clicked)
        self.ui.pushButtonDelete.clicked.connect(self.__pushButtonDelete_clicked)
        self.ui.pushButtonClose.clicked.connect(self.__pushButtonClose_clicked)

        # Our internal data is the python dictionary
        # Its key is QString type, this means project 's name
        # It's value is QString type, this means project 's folder
        self.__projectFolderData = {}

        self.__readProjectFoldersData()
        self.__displayProjectFoldersData()

    # From system registry, read saved projects 's folder data
    def __readProjectFoldersData(self):
        settings = QSettings("FlightPlanner", "Project")
        totaldata = settings.value("/SavedProjectFolders", "").toString()

        datalist = totaldata.split(self.DataSeparator)

        for projectdatastring in datalist:
            if projectdatastring == "":
                continue

            projectdatalist = projectdatastring.split(self.NamePathSeparator)
            projectname = projectdatalist[0]
            projectfolder = projectdatalist[1]

            self.__projectFolderData[projectname] = projectfolder

    # To system registry, save project 's folder data
    def __saveProjectFoldersData(self):
        totaldata = QString("")

        for key in self.__projectFolderData.keys():
            projectfolder = self.__projectFolderData[key]
            data = key + self.NamePathSeparator + projectfolder

            totaldata = totaldata + self.DataSeparator + data

        settings = QSettings("FlightPlanner", "Project")
        settings.setValue("/SavedProjectFolders", totaldata)

    # update listwidget with __projectFolderData content.
    # Note that clear all and replace with current data.

    def __displayProjectFoldersData(self):
        self.ui.listWidgetProjectFolder.clear()

        for key in self.__projectFolderData.keys():
            label = key + "  (" + self.__projectFolderData[key] + ")"
            item = QListWidgetItem(label)
            item.setData(QtCore.Qt.UserRole, QString(key))
            self.ui.listWidgetProjectFolder.addItem(item)

    # precondition: name is a entirely new key in __projectFolderData dictionary
    # folder must be existed
    def __addProjectFolder(self, name, folder):
        self.__projectFolderData[name] = folder

    # precondition: name must be existed in keys of __projectFolderData dictionary
    def __deleteProjectFolder(self, name):
        del self.__projectFolderData[name]

    # precondition: name must be existed in keys of __projectFolderData dictionary
    def __modifyProjectFolder(self, name, path):
        self.__projectFolderData[name] = path

    # Invoked when current item changed
    def __listWidgetProjectFolder_currentItemChanged(self, curr, prev):
        if curr is None:
            return

        projectname = curr.data(QtCore.Qt.UserRole).toString()

        if projectname.isEmpty():
            return

        self.ui.lineEditProjectName.setText(projectname)

        projectpath = self.__projectFolderData[projectname]
        self.ui.lineEditProjectFolder.setText(projectpath)

    def __pushButtonSelectFolder_clicked(self):
        folder = self.ui.lineEditProjectFolder.text()

        if folder == "":
            folder = QDir.rootPath()

        folder = QFileDialog.getExistingDirectory(self, "Select Folder!", folder)

        if folder is not None and folder != "":
            self.ui.lineEditProjectFolder.setText(folder)

    def __pushButtonSelect_clicked(self):
        if self.ui.lineEditProjectFolder.text() == "":
            QMessageBox.critical(self, "Error", "Please select project folder!")
            return

        folder = self.ui.lineEditProjectFolder.text()

        AirCraftOperation.SelectProjectFolder(folder)
        self.accept()

    def __pushButtonAdd_clicked(self):
        if self.ui.lineEditProjectName.text() == "":
            QMessageBox.critical(self, "Error", "Please enter project name!")
            return

        if self.ui.lineEditProjectName.text().contains(self.DataSeparator) or \
           self.ui.lineEditProjectName.text().contains(self.NamePathSeparator):
            QMessageBox.critical(self, "Error", "Invalid project name!")
            return

        if self.ui.lineEditProjectFolder.text() == "":
            QMessageBox.critical(self, "Error", "Please select project folder!")
            return

        projectname = self.ui.lineEditProjectName.text()

        if projectname in self.__projectFolderData:
            QMessageBox.critical(self, "Error", "Project name that you have enter has already been used!\n"
                                                "Please select another project name!")
            return

        projectfolder = self.ui.lineEditProjectFolder.text()

        if projectfolder in self.__projectFolderData.values():
            QMessageBox.critical(self, "Error",
                                 "Project folder that you have selected has already existed!\n"
                                 "Please select another project folder!")
            return

        self.__addProjectFolder(projectname, projectfolder)
        self.__displayProjectFoldersData()

    def __pushButtonModify_clicked(self):
        if self.ui.listWidgetProjectFolder.selectedItems().__len__() == 0:
            return

        if self.ui.lineEditProjectName.text() == "":
            QMessageBox.critical(self, "Error", "Please enter project name!")
            return

        if self.ui.lineEditProjectName.text().contains(self.DataSeparator) or \
           self.ui.lineEditProjectName.text().contains(self.NamePathSeparator):
            QMessageBox.critical(self, "Error", "Invalid project name!")
            return

        if self.ui.lineEditProjectFolder.text() == "":
            QMessageBox.critical(self, "Error", "Please select project folder!")
            return

        newprojectname = self.ui.lineEditProjectName.text()
        projectfolder = self.ui.lineEditProjectFolder.text()

        item = self.ui.listWidgetProjectFolder.currentItem()

        oldprojectname = item.data(QtCore.Qt.UserRole).toString()

        if newprojectname == oldprojectname:
            if projectfolder in self.__projectFolderData.values():
                QMessageBox.critical(self, "Alert", "There is no updated data!")
                return

        result = QMessageBox.warning(self,
                                     "Alert",
                                     "Do you want to modify selected project folder?", QMessageBox.Yes | QMessageBox.No)

        if result != QMessageBox.Yes:
            return

        self.__deleteProjectFolder(oldprojectname)
        self.__addProjectFolder(newprojectname, projectfolder)
        self.__displayProjectFoldersData()

    def __pushButtonDelete_clicked(self):
        if self.ui.listWidgetProjectFolder.selectedItems().__len__() == 0:
            return

        result = QMessageBox.warning(self,
                                     "Alert",
                                     "Do you want to delete selected project folder?", QMessageBox.Yes | QMessageBox.No)

        if result != QMessageBox.Yes:
            return

        item = self.ui.listWidgetProjectFolder.currentItem()

        if item is None:
            return

        projectname = item.data(QtCore.Qt.UserRole).toString()

        self.__deleteProjectFolder(projectname)
        self.__displayProjectFoldersData()

        if self.ui.listWidgetProjectFolder.count() > 0:
            self.ui.listWidgetProjectFolder.setCurrentRow(0)

    def __pushButtonClose_clicked(self):
        self.__saveProjectFoldersData()
        self.accept()
