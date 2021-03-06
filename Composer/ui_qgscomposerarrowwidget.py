# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgscomposerarrowwidgetbase.ui'
#
# Created: Thu Sep 22 17:33:53 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from qgis.gui import QgsCollapsibleGroupBoxBasic, QgsDoubleSpinBox, QgsColorButtonV2
# from qgscollapsiblegroupbox import QgsCollapsibleGroupBoxBasic
# from qgsdoublespinbox import QgsDoubleSpinBox
# from qgscolorbuttonv2 import QgsColorButtonV2
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

class Ui_QgsComposerArrowWidgetBase(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName(_fromUtf8("self"))
        self.resize(334, 383)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet(_fromUtf8("padding: 2px; font-weight: bold; background-color: rgb(200, 200, 200);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 332, 360))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.mainLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.groupBox = QgsCollapsibleGroupBoxBasic(self.scrollAreaWidgetContents)
        self.groupBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.groupBox.setProperty("syncGroup", _fromUtf8("composeritem"))
        self.groupBox.setProperty("collapsed", False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.mLineStyleButton = QtGui.QPushButton(self.groupBox)
        self.mLineStyleButton.setObjectName(_fromUtf8("mLineStyleButton"))
        self.verticalLayout_2.addWidget(self.mLineStyleButton)
        self.mainLayout.addWidget(self.groupBox)
        self.mArrowMarkersGroupBox = QgsCollapsibleGroupBoxBasic(self.scrollAreaWidgetContents)
        self.mArrowMarkersGroupBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.mArrowMarkersGroupBox.setProperty("syncGroup", _fromUtf8("composeritem"))
        self.mArrowMarkersGroupBox.setProperty("collapsed", False)
        self.mArrowMarkersGroupBox.setObjectName(_fromUtf8("mArrowMarkersGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.mArrowMarkersGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.mDefaultMarkerRadioButton = QtGui.QRadioButton(self.mArrowMarkersGroupBox)
        self.mDefaultMarkerRadioButton.setObjectName(_fromUtf8("mDefaultMarkerRadioButton"))
        self.horizontalLayout_3.addWidget(self.mDefaultMarkerRadioButton)
        self.mNoMarkerRadioButton = QtGui.QRadioButton(self.mArrowMarkersGroupBox)
        self.mNoMarkerRadioButton.setObjectName(_fromUtf8("mNoMarkerRadioButton"))
        self.horizontalLayout_3.addWidget(self.mNoMarkerRadioButton)
        self.mSvgMarkerRadioButton = QtGui.QRadioButton(self.mArrowMarkersGroupBox)
        self.mSvgMarkerRadioButton.setObjectName(_fromUtf8("mSvgMarkerRadioButton"))
        self.horizontalLayout_3.addWidget(self.mSvgMarkerRadioButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.mArrowMarkersGroupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.mArrowHeadOutlineColorButton = QgsColorButtonV2(self.mArrowMarkersGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mArrowHeadOutlineColorButton.sizePolicy().hasHeightForWidth())
        self.mArrowHeadOutlineColorButton.setSizePolicy(sizePolicy)
        self.mArrowHeadOutlineColorButton.setMinimumSize(QtCore.QSize(120, 0))
        self.mArrowHeadOutlineColorButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.mArrowHeadOutlineColorButton.setText(_fromUtf8(""))
        self.mArrowHeadOutlineColorButton.setObjectName(_fromUtf8("mArrowHeadOutlineColorButton"))
        self.gridLayout.addWidget(self.mArrowHeadOutlineColorButton, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.mArrowMarkersGroupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.mArrowHeadFillColorButton = QgsColorButtonV2(self.mArrowMarkersGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mArrowHeadFillColorButton.sizePolicy().hasHeightForWidth())
        self.mArrowHeadFillColorButton.setSizePolicy(sizePolicy)
        self.mArrowHeadFillColorButton.setMinimumSize(QtCore.QSize(120, 0))
        self.mArrowHeadFillColorButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.mArrowHeadFillColorButton.setText(_fromUtf8(""))
        self.mArrowHeadFillColorButton.setObjectName(_fromUtf8("mArrowHeadFillColorButton"))
        self.gridLayout.addWidget(self.mArrowHeadFillColorButton, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.mArrowMarkersGroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.mOutlineWidthSpinBox = QgsDoubleSpinBox(self.mArrowMarkersGroupBox)
        self.mOutlineWidthSpinBox.setPrefix(_fromUtf8(""))
        self.mOutlineWidthSpinBox.setShowClearButton(False)
        self.mOutlineWidthSpinBox.setObjectName(_fromUtf8("mOutlineWidthSpinBox"))
        self.gridLayout.addWidget(self.mOutlineWidthSpinBox, 3, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.mArrowMarkersGroupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.mArrowHeadWidthSpinBox = QgsDoubleSpinBox(self.mArrowMarkersGroupBox)
        self.mArrowHeadWidthSpinBox.setPrefix(_fromUtf8(""))
        self.mArrowHeadWidthSpinBox.setShowClearButton(False)
        self.mArrowHeadWidthSpinBox.setObjectName(_fromUtf8("mArrowHeadWidthSpinBox"))
        self.gridLayout.addWidget(self.mArrowHeadWidthSpinBox, 4, 1, 1, 1)
        self.mStartMarkerLabel = QtGui.QLabel(self.mArrowMarkersGroupBox)
        self.mStartMarkerLabel.setObjectName(_fromUtf8("mStartMarkerLabel"))
        self.gridLayout.addWidget(self.mStartMarkerLabel, 5, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mStartMarkerLineEdit = QtGui.QLineEdit(self.mArrowMarkersGroupBox)
        self.mStartMarkerLineEdit.setObjectName(_fromUtf8("mStartMarkerLineEdit"))
        self.horizontalLayout.addWidget(self.mStartMarkerLineEdit)
        self.mStartMarkerToolButton = QtGui.QToolButton(self.mArrowMarkersGroupBox)
        self.mStartMarkerToolButton.setObjectName(_fromUtf8("mStartMarkerToolButton"))
        self.horizontalLayout.addWidget(self.mStartMarkerToolButton)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 1, 1, 1)
        self.mEndMarkerLabel = QtGui.QLabel(self.mArrowMarkersGroupBox)
        self.mEndMarkerLabel.setObjectName(_fromUtf8("mEndMarkerLabel"))
        self.gridLayout.addWidget(self.mEndMarkerLabel, 6, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.mEndMarkerLineEdit = QtGui.QLineEdit(self.mArrowMarkersGroupBox)
        self.mEndMarkerLineEdit.setObjectName(_fromUtf8("mEndMarkerLineEdit"))
        self.horizontalLayout_2.addWidget(self.mEndMarkerLineEdit)
        self.mEndMarkerToolButton = QtGui.QToolButton(self.mArrowMarkersGroupBox)
        self.mEndMarkerToolButton.setObjectName(_fromUtf8("mEndMarkerToolButton"))
        self.horizontalLayout_2.addWidget(self.mEndMarkerToolButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 1, 1, 1)
        self.mainLayout.addWidget(self.mArrowMarkersGroupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.scrollArea, self.groupBox)
        self.setTabOrder(self.groupBox, self.mLineStyleButton)
        self.setTabOrder(self.mLineStyleButton, self.mArrowMarkersGroupBox)
        self.setTabOrder(self.mArrowMarkersGroupBox, self.mDefaultMarkerRadioButton)
        self.setTabOrder(self.mDefaultMarkerRadioButton, self.mNoMarkerRadioButton)
        self.setTabOrder(self.mNoMarkerRadioButton, self.mSvgMarkerRadioButton)
        self.setTabOrder(self.mSvgMarkerRadioButton, self.mArrowHeadOutlineColorButton)
        self.setTabOrder(self.mArrowHeadOutlineColorButton, self.mArrowHeadFillColorButton)
        self.setTabOrder(self.mArrowHeadFillColorButton, self.mOutlineWidthSpinBox)
        self.setTabOrder(self.mOutlineWidthSpinBox, self.mArrowHeadWidthSpinBox)
        self.setTabOrder(self.mArrowHeadWidthSpinBox, self.mStartMarkerLineEdit)
        self.setTabOrder(self.mStartMarkerLineEdit, self.mStartMarkerToolButton)
        self.setTabOrder(self.mStartMarkerToolButton, self.mEndMarkerLineEdit)
        self.setTabOrder(self.mEndMarkerLineEdit, self.mEndMarkerToolButton)

    def retranslateUi(self):
        self.setWindowTitle(_translate("QgsComposerArrowWidgetBase", "Form", None))
        self.label_3.setText(_translate("QgsComposerArrowWidgetBase", "Arrow", None))
        self.groupBox.setTitle(_translate("QgsComposerArrowWidgetBase", "Main properties", None))
        self.mLineStyleButton.setText(_translate("QgsComposerArrowWidgetBase", "Line style...", None))
        self.mArrowMarkersGroupBox.setTitle(_translate("QgsComposerArrowWidgetBase", "Arrow markers", None))
        self.mDefaultMarkerRadioButton.setText(_translate("QgsComposerArrowWidgetBase", "Default", None))
        self.mNoMarkerRadioButton.setText(_translate("QgsComposerArrowWidgetBase", "None", None))
        self.mSvgMarkerRadioButton.setText(_translate("QgsComposerArrowWidgetBase", "SVG", None))
        self.label_5.setText(_translate("QgsComposerArrowWidgetBase", "Arrow outline color", None))
        self.label_4.setText(_translate("QgsComposerArrowWidgetBase", "Arrow fill color", None))
        self.label.setText(_translate("QgsComposerArrowWidgetBase", "Arrow outline width", None))
        self.mOutlineWidthSpinBox.setSuffix(_translate("QgsComposerArrowWidgetBase", " mm", None))
        self.label_2.setText(_translate("QgsComposerArrowWidgetBase", "Arrow head width", None))
        self.mArrowHeadWidthSpinBox.setSuffix(_translate("QgsComposerArrowWidgetBase", " mm", None))
        self.mStartMarkerLabel.setText(_translate("QgsComposerArrowWidgetBase", "Start marker", None))
        self.mStartMarkerToolButton.setText(_translate("QgsComposerArrowWidgetBase", "...", None))
        self.mEndMarkerLabel.setText(_translate("QgsComposerArrowWidgetBase", "End marker", None))
        self.mEndMarkerToolButton.setText(_translate("QgsComposerArrowWidgetBase", "...", None))


