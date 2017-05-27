# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ProjectManager/RegProjectFolderForm.ui'
#
# Created: Tue May 23 03:49:39 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_RegProjectFolderDialog(object):
    def setupUi(self, RegProjectFolderDialog):
        RegProjectFolderDialog.setObjectName(_fromUtf8("RegProjectFolderDialog"))
        RegProjectFolderDialog.resize(556, 398)
        self.verticalLayout_2 = QtGui.QVBoxLayout(RegProjectFolderDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(RegProjectFolderDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidgetProjectFolder = QtGui.QListWidget(self.groupBox)
        self.listWidgetProjectFolder.setObjectName(_fromUtf8("listWidgetProjectFolder"))
        self.verticalLayout.addWidget(self.listWidgetProjectFolder)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(RegProjectFolderDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEditProjectName = QtGui.QLineEdit(RegProjectFolderDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditProjectName.sizePolicy().hasHeightForWidth())
        self.lineEditProjectName.setSizePolicy(sizePolicy)
        self.lineEditProjectName.setReadOnly(False)
        self.lineEditProjectName.setObjectName(_fromUtf8("lineEditProjectName"))
        self.horizontalLayout.addWidget(self.lineEditProjectName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(RegProjectFolderDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditProjectFolder = QtGui.QLineEdit(RegProjectFolderDialog)
        self.lineEditProjectFolder.setReadOnly(True)
        self.lineEditProjectFolder.setObjectName(_fromUtf8("lineEditProjectFolder"))
        self.horizontalLayout_2.addWidget(self.lineEditProjectFolder)
        self.pushButtonSelectFolder = QtGui.QPushButton(RegProjectFolderDialog)
        self.pushButtonSelectFolder.setText(_fromUtf8(""))
        self.pushButtonSelectFolder.setObjectName(_fromUtf8("pushButtonSelectFolder"))
        self.horizontalLayout_2.addWidget(self.pushButtonSelectFolder)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonSelect = QtGui.QPushButton(RegProjectFolderDialog)
        self.pushButtonSelect.setObjectName(_fromUtf8("pushButtonSelect"))
        self.horizontalLayout_3.addWidget(self.pushButtonSelect)
        self.pushButtonAdd = QtGui.QPushButton(RegProjectFolderDialog)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout_3.addWidget(self.pushButtonAdd)
        self.pushButtonModify = QtGui.QPushButton(RegProjectFolderDialog)
        self.pushButtonModify.setObjectName(_fromUtf8("pushButtonModify"))
        self.horizontalLayout_3.addWidget(self.pushButtonModify)
        self.pushButtonDelete = QtGui.QPushButton(RegProjectFolderDialog)
        self.pushButtonDelete.setObjectName(_fromUtf8("pushButtonDelete"))
        self.horizontalLayout_3.addWidget(self.pushButtonDelete)
        self.pushButtonClose = QtGui.QPushButton(RegProjectFolderDialog)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout_3.addWidget(self.pushButtonClose)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.retranslateUi(RegProjectFolderDialog)
        QtCore.QMetaObject.connectSlotsByName(RegProjectFolderDialog)

    def retranslateUi(self, RegProjectFolderDialog):
        RegProjectFolderDialog.setWindowTitle(_translate("RegProjectFolderDialog", "Register Project Folder", None))
        self.groupBox.setTitle(_translate("RegProjectFolderDialog", "Select a project", None))
        self.label.setText(_translate("RegProjectFolderDialog", "Name:", None))
        self.label_2.setText(_translate("RegProjectFolderDialog", "Path:  ", None))
        self.pushButtonSelect.setText(_translate("RegProjectFolderDialog", "Select", None))
        self.pushButtonAdd.setText(_translate("RegProjectFolderDialog", "Add", None))
        self.pushButtonModify.setText(_translate("RegProjectFolderDialog", "Modify", None))
        self.pushButtonDelete.setText(_translate("RegProjectFolderDialog", "Delete", None))
        self.pushButtonClose.setText(_translate("RegProjectFolderDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RegProjectFolderDialog = QtGui.QDialog()
    ui = Ui_RegProjectFolderDialog()
    ui.setupUi(RegProjectFolderDialog)
    RegProjectFolderDialog.show()
    sys.exit(app.exec_())

