# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QFileDialog, QMessageBox, QMainWindow
from PyQt4.QtCore import QString, QFileInfo, Qt
from PyQt4.QtCore import SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.TreeView import TreeNode
from FlightPlanner.Panels.GroupBox import GroupBox
from Type.FasDataBlockFile import FasDataBlockFile
from ui_QaWindow import Ui_MainWindow
from Type.QA.QAReportEntry import QAReportEntry
from Type.QA.QASession import QASessionType, QASession
from Type.QA.QAAttached import QAAttached
from Type.QA.QA import QA


from FlightPlanner.types import QARecordType, QAColorCode, QASnapshotFormat
from FlightPlanner.Captions import Captions
from FlightPlanner.Confirmations import Confirmations

from Type.switch import switch
from Type.String import String



class QADefaultView:
    QA = "QA"
    Report = "Report"

class QaWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(100, 70)
        self.setWindowTitle("QaWindow")

        self.NO_INDEX = -1999

        self.activeDocument = None
        self.size = None
        self.location = None
        self.splitterDistance = None
        self.previousState = None
        self.boundsSpecified = None
        self.loaded = False
        self.shown = False
        self.boldFont = None
        self.labelEditInProgress = None
        self.dragNodeNewIndex = -1

        self.previousState = self.windowState()

        self.ui.mniFileExportQA.triggered.connect(self.btnExportQA_Click)

        # self.method_21()

    def btnExportQA_Click(self):
        pass
    def method_10(self, treeNode_0, int_0):
        if (treeNode_0 == None):
            return None
        if (treeNode_0.Parent == None):
            return None
        if (treeNode_0.Parent.Level == int_0):
            return treeNode_0.Parent
        return self.method_10(treeNode_0.Parent, int_0)

    


    def get_ActiveDocument(self):
        return self.activeDocument
    def set_ActiveDocument(self, value):
        self.activeDocument = value
        self.method_21()
        if (self.activeDocument != None):
            if (self.activeDocument.ReportEntriesSupported):
                if (self.ui.tabControl.currentIndex() == 1):
                    self.ui.tabControl.addTab(self.tabReport, "Report")
            elif (self.ui.tabControl.currentIndex() == 2):
                self.tabControl.TabPages.RemoveAt(1)
            self.method_2()
            if (self.ui.tabControl.count() == 2):
                self.method_3()
            self.treeView.SelectedNode = self.method_8(self.activeDocument.SelectedRecord)
            if (self.ui.treeView.SelectedNode == None):
                self.ui.treeView.SelectedNode = self.lastSessionNode
            self.treeViewReport.SelectedNode = self.method_12(self.activeDocument.SelectedReportEntry)
            if (not self.isVisible()):
                self.setVisible(True)
        self.method_20()

    ActiveDocument = property(get_ActiveDocument, set_ActiveDocument, None, None)

    def get_CreateParams(self):
        createParams = self.CreateParams
        # createParams.Parent = Win32.GetDesktopWindow()
        return createParams
    CreateParams = property(get_CreateParams, None, None, None)

    def get_DefaultView(self):
        if (self.ui.tabControl.currentIndex() == 0):
            return QADefaultView.QA
        return QADefaultView.Report
    def set_DefaultView(self, value):
        if (value == QADefaultView.QA):
            self.ui.tabControl.setCurrentIndex(0)
            return
        self.ui.tabControl.setCurrentIndex(1)
    DefaultView = property(get_DefaultView, set_DefaultView, None, None)

    def get_isCopyAvailable(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.currentIndex() == 0) else self.ui.treeViewReport.SelectedNode
        flag = treeNode != None
        flag1 = flag
        if (flag and self.ui.tabControl.currentIndex() == 1):
            tag = treeNode.Tag# as QAReportEntry
            if (tag != None and tag.Value == None):
                flag1 = False
        return flag1
    isCopyAvailable = property(get_isCopyAvailable, None, None, None)

    def get_isCopyEntryToReportAvailable(self):
        if (self.ui.tabControl.currentIndex() != 0):
            return False
        if (self.ui.tabControl.count() != 2):
            return False
        selectedNode = self.ui.treeView.SelectedNode
        if (selectedNode == None):
            return False
        if (selectedNode.Parent == None):
            return False
        if (selectedNode.Parent.Level != 0):
            return False
        return True
    isCopyEntryToReportAvailable = property(get_isCopyEntryToReportAvailable, None, None, None)

    def get_isDeleteAvailable(self):
        if (self.ui.tabControl.currentIndex() == 0):
            return self.method_16()
        selectedNode = self.ui.treeViewReport.SelectedNode
        if (selectedNode == None):
            return False
        return isinstance(selectedNode.Tag, QAReportEntry)
    isDeleteAvailable = property(get_isDeleteAvailable, None, None, None)

    def get_isEditCommentAvailable(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.currentIndex() == 0) else self.ui.treeViewReport.SelectedNode
        flag = False
        flag = self.method_17(treeNode) if(self.ui.tabControl.currentIndex() != 0) else self.method_16()
        if (self.method_15(treeNode, QARecordType.Comment)):
            return flag
        return False
    isEditCommentAvailable = property(get_isEditCommentAvailable, None, None, None)

    def get_isExportQaAvailable(self):
        return self.ui.tabControl.currentIndex() == 0
    isExportQaAvailable = property(get_isExportQaAvailable, None, None, None)

    def get_isExportReportAvailable(self):
        return self.ui.tabControl.currentIndex() == 1
    isExportReportAvailable = property(get_isExportReportAvailable, None, None, None)

    def get_isExportToWordAvailable(self):
        flag = False
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.currentIndex() == 0) else self.ui.treeViewReport.SelectedNode
        flag = False if(treeNode == None) else not self.method_15(treeNode, QARecordType.Session)
        flag1 = flag
        if (flag and self.ui.tabControl.currentIndex() == 1):
            tag = treeNode.Tag# as QAReportEntry;
            if (tag != None and tag.Value == None):
                flag1 = False
        return flag1
    isExportToWordAvailable = property(get_isExportToWordAvailable, None, None, None)

    def get_isFlagAvailable(self):
        if (self.ui.tabControl.currentIndex() != 1):
            return False
        selectedNode = self.ui.treeViewReport.SelectedNode
        if (selectedNode == None):
            return False
        tag = selectedNode.Tag# as QAReportEntry;
        if (tag == None):
            return False
        if (tag.Value == None):
            return False
        return True
    isFlagAvailable = property(get_isFlagAvailable, None, None, None)

    def get_isSnapshotActionAvailable(self):
        return self.method_15(self.ui.treeView.SelectedNode if(self.ui.tabControl.currentIndex() == 0) else self.ui.treeViewReport.SelectedNode, QARecordType.Snapshot)
    isSnapshotActionAvailable = property(get_isSnapshotActionAvailable, None, None, None)

    def get_lastSessionNode(self):
        if (self.ui.treeView.Nodes.Count < 1):
            return None
        return self.treeView.Nodes[self.treeView.Nodes.Count - 1]
    lastSessionNode = property(get_lastSessionNode, None, None, None)

    def get_PreviousWindowState(self):
        return self.previousState
    def set_PreviousWindowState(self, value):
        self.previousState = value
    PreviousWindowState = property(get_PreviousWindowState, set_PreviousWindowState, None, None)

    def get_ShowWithoutActivation(self):
        return True
    ShowWithoutActivation = property(get_ShowWithoutActivation, None, None, None)
    
    
    def method_11(self, treeNode_0):
        if (treeNode_0 == None):
            return None
        tag = treeNode_0.Tag# as QAReportEntry
        if (tag != None):
            return tag
        return self.method_11(treeNode_0.Parent)

    def method_12(self, qareportEntry_0):
        treeNode = None
        if (qareportEntry_0 != None):
            enumerator = self.ui.treeViewReport.Nodes#.GetEnumerator()
            for current in enumerator:
                if (current.Tag != qareportEntry_0):
                    enumerator1 = current.Nodes#.GetEnumerator()
                    for current1 in enumerator1:
                        if (current1.Tag != qareportEntry_0):
                            continue
                        treeNode = current1
                        return treeNode
                else:
                    treeNode = current
                    return treeNode
            return treeNode
        return None

    def method_13(self, qarecord_0):
        treeNode = None
        enumerator = self.treeViewReport.Nodes
        for current in enumerator:
            tag = current.Tag# as QAReportEntry
            if (tag == None or tag.Value != qarecord_0):
                enumerator1 = current.Nodes#.GetEnumerator()
                for current1 in enumerator1:
                    tag = current1.Tag# as QAReportEntry
                    if (tag == None or tag.Value != qarecord_0):
                        continue
                    treeNode = current1
                    return treeNode
            else:
                treeNode = current
                return treeNode
            return None
        return treeNode

    def method_14(self, treeNode_0, bool_0):
        if (treeNode_0 != None):
            text = treeNode_0.Text
            treeNode_0.Text = " "
            # if (not bool_0):
            #     treeNode_0.NodeFont = new System.Drawing.Font(treeNode_0.TreeView.Font, System.Drawing.FontStyle.Regular)
            # else:
            #     treeNode_0.NodeFont = new System.Drawing.Font(treeNode_0.TreeView.Font, System.Drawing.FontStyle.Bold)
            treeNode_0.Text = text

    def method_15(self, treeNode_0, qarecordType_0):
        if (treeNode_0 == None):
            return False
        tag = treeNode_0.Tag# as QARecord
        if (tag == None):
            qAReportEntry = treeNode_0.Tag# as QAReportEntry
            if (qAReportEntry == None):
                return False
            tag = qAReportEntry.Value
            if (tag == None):
                return False
        return tag.Type == qarecordType_0

    def method_16(self):
        if (self.lastSessionNode == None or self.treeView.SelectedNode == None):
            return False
        return self.method_10(self.treeView.SelectedNode, 0) == self.lastSessionNode

    def method_17(self, treeNode_0):
        if (self.lastSessionNode != None):
            if (treeNode_0 == None):
                return False
            tag = treeNode_0.Tag #as QARecord
            if (tag != None):
                return self.method_10(treeNode_0, 0) == self.lastSessionNode
            qAReportEntry = treeNode_0.Tag #as QAReportEntry
            if (qAReportEntry == None):
                return False
            tag = qAReportEntry.Value
            if (tag == None):
                return False
            if (treeNode_0.Parent == None):
                return self.activeDocument.Sessions[self.activeDocument.Sessions.Count - 1].Children.Contains(tag)
            tag1 = treeNode_0.Parent.Tag #as QAReportEntry
            if (tag1 != None and tag1.Value == None):
                return self.activeDocument.Sessions[self.activeDocument.Sessions.Count - 1].Children.Contains(tag)
        return False

    def method_18(self, qarecordType_0, qacolorCode_0):
        for case in switch (qarecordType_0):
            if case(QARecordType.Attached):
                return "attachment_{0}.png".format(qacolorCode_0.ToString())
            elif case(QARecordType.Table):
                return "program_{0}.png".format(qacolorCode_0.ToString())
            elif case(QARecordType.Comment):
                return "comment_{0}.png".format(qacolorCode_0.ToString())
            elif case(QARecordType.Snapshot):
                return "snapshot_{0}.png".format(qacolorCode_0.ToString())
            else:
                return "session_{0}.png".format(qacolorCode_0.ToString())

    def method_19(self):
        for node in self.ui.treeViewReport.Nodes:
            tag = node.Tag# as QAReportEntry
            if (tag == None or tag.Value != None):
                continue
            str0 = self.method_18(QARecordType.Session, QAColorCode.None)
            enumerator = tag.Children#.GetEnumerator()
            for current in enumerator:
                if (current.ColorCode != QAColorCode.None):
                    str0 = self.method_18(QARecordType.Session, current.ColorCode)
                    break
            node.ImageKey = str0
            node.SelectedImageKey = str0

    def method_2(self):
        self.ui.treeView.Nodes.Clear()
        if (self.activeDocument == None):
            return
        count = self.activeDocument.Sessions.Count
        for i in range(count):
            item = self.activeDocument.Sessions[i]
            treeNode = TreeNode()
            if (item.SessionType != QASessionType.Started):
                treeNode.Text = Captions.QA_OPENED
            else:
                treeNode.Text = Captions.QA_STARTED
            if (i == count - 1):
                treeNode1 = treeNode
                treeNode1.Text = String.Concat([treeNode1.Text, " ({0})".format(Captions.CURRENT)])
            treeNode.ImageKey = "Session.png"
            treeNode.SelectedImageKey = treeNode.ImageKey
            treeNode.Tag = item
            self.treeView.Nodes.Add(treeNode)
            for child in item.Children:
                self.method_4(treeNode, child)

    def method_20(self):
        flag = self.isExportQaAvailable
        self.btnExportQA.Visible = flag
        self.mniFileExportQA.Visible = flag
        flag = self.isExportReportAvailable
        self.btnExportReport.Visible = flag
        self.mniFileExportReport.Visible = flag
        flag = self.isCopyAvailable
        self.mniEditCopy.Enabled = flag
        self.btnCopy.Enabled = flag
        flag = self.isDeleteAvailable
        self.mniEditDelete.Visible = flag
        self.btnDelete.Visible = flag
        flag = self.isExportToWordAvailable
        self.mniEditExportWord.Visible = flag
        self.btnExportWord.Visible = flag
        flag = self.isEditCommentAvailable
        self.mniEditComment.Visible = flag
        self.btnEditComment.Visible = flag
        flag = self.isSnapshotActionAvailable
        self.mniEditExportSST.Visible = flag
        self.mniEditRestoreView.Visible = flag
        self.btnExportSST.Visible = flag
        self.btnRestoreView.Visible = flag
        self.btnSubmit.Enabled = False if(self.ui.txtHeading.Text.trimmed() == "") else self.ui.txtComment.Text.trimmed() != ""

    def method_21(self):
        self.treeView.Nodes.Clear()
        self.ui.lblDateTime.setText("")
        self.ui.txtHeading.setText("")
        self.ui.txtComment.setText("")
        if (self.activeDocument != None):
            self.method_28()
            self.ui.lblFile.Text = self.activeDocument.FileNameQA
            self.ui.mniFileExportQA.setEnabled(True)
            self.ui.mniFileExportReport.setEnabled(True)
            self.ui.btnExportQA.setEnabled(True)
            self.ui.btnExportReport.setEnabled(True)
            self.ui.toolStrip.setEnabled(True)
            # self.ui.splitContainer.Enabled = True
            # self.ui.tblComment.Enabled = True
        else:
            self.setWindowTitle(Captions.QUALITY_ASSURANCE_ASSISTENT)
            self.ui.lblFile.setText("")
            self.ui.mniFileExportQA.setEnabled(False)
            self.ui.mniFileExportReport.setEnabled(False)
            self.ui.btnExportQA.setEnabled(False)
            self.ui.btnExportReport.setEnabled(False)
            self.ui.toolStrip.setEnabled(False)
            # self.splitContainer.Enabled = False
            # self.tblComment.Enabled = False
        self.method_23(None, False)
        self.method_22(None, True)
        self.method_20()

    def method_22(self, string_0, bool_0):
        self.ui.richBox.setPlainText("")
        if (not String.IsNoneOrEmpty(string_0)):
            self.ui.richBox.setPlainText(string_0)
        if (self.ui.richBox.setVisible() != bool_0):
            self.ui.richBox.setVisible(bool_0)

    def method_23(self, image_0, bool_0):
        # self.ui.picSnapshot.setS.Size = new System.Drawing.Size(100, 100)
        self.ui.picSnapshot.Image = image_0
        if (self.ui.pnlSnapshot.setVisible() != bool_0):
            self.pnlSnapshot.setVisible(bool_0)

    def method_24(self):
        if (not self.isVisible()):
            self.setVisible(True)
        if (self.windowState() == Qt.WindowMinimized):
            self.setWindowState(self.previousState)
        # base.Activate()

    def method_25(self, qarecord_0):
        if (qarecord_0 == None):
            return
        if (self.activeDocument == None):
            return
        if (self.lastSessionNode == None):
            return
        tag = self.lastSessionNode.Tag
        if (tag == None):
            return
        tag.Children.Add(qarecord_0)
        self.method_4(self.lastSessionNode, qarecord_0)
        self.ui.treeView.SelectedNode = self.lastSessionNode.LastNode
        if (QA.AutoReportEntry and not isinstance(qarecord_0, QASession) and not isinstance(qarecord_0, QAAttached) and self.ui.tabControl.count() == 2):
            treeNode = None
            qAReportEntry = QAReportEntry()
            qAReportEntry.Value = qarecord_0
            self.activeDocument.ReportEntries.Add(qAReportEntry)
            self.method_5(treeNode, qAReportEntry)
            self.ui.treeViewReport.SelectedNode = self.ui.treeViewReport.Nodes[self.ui.treeViewReport.Nodes.Count - 1]
        self.activeDocument.method_2(self)

    def method_26(self, string_0, string_1):
        str0 = Path.ChangeExtension(string_0, string_1)
        qAAttached = QAAttached()
        qAAttached.Heading = Captions.QA_ATTACHED,
        qAAttached.Text = Captions.QA_CONTINUING_WITH.format(str0)
        self.method_25(qAAttached)
        self.ActiveDocument.FileNameQA = str0
        qAAttached.Text = Captions.QA_ATTACHED_TO.format(string_0)
        self.method_27()
        self.ActiveDocument.method_2(self)

    def method_27(self):
        self.method_7()

    def method_28(self):
        self.setWindowTitle("{0} ({1})".format(Captions.QUALITY_ASSURANCE_ASSISTENT, Path.GetFileNameWithoutExtension(self.activeDocument.FileNameQA)))

    def method_29(self, treeNode_0):
        if (treeNode_0.ImageKey == None or treeNode_0.TreeView.ImageList == None or not treeNode_0.TreeView.ImageList.Images.ContainsKey(treeNode_0.ImageKey)):
            return 8
        size = treeNode_0.TreeView.ImageList.Images[treeNode_0.ImageKey].Size
        return size.Width + 8

    def method_3(self):
        self.treeViewReport.Nodes.Clear()
        if (self.activeDocument == None):
            return
        for reportEntry in self.activeDocument.ReportEntries:
            self.method_5(None, reportEntry)
        self.method_19()

    # def method_30(self, treeNode_0):
    #     # prevNode = treeNode_0.PrevNode ?? treeNode_0.Parent ?? treeNode_0
    #     return self.method_32(prevNode)
    #
    # def method_31(self, treeNode_0):
    #     nextNode = treeNode_0.NextNode ?? treeNode_0.Parent
    #     if (nextNode != None):
    #         nextNode = nextNode.NextNode
    #     if (nextNode == None):
    #         nextNode = treeNode_0
    #     return self.method_32(nextNode)

    def method_32(self, treeNode_0):
        bounds = treeNode_0.Bounds
        clientRectangle = treeNode_0.TreeView.ClientRectangle
        if (bounds.Top >= clientRectangle.Top and bounds.Bottom <= clientRectangle.Bottom):
            return True
        treeNode_0.EnsureVisible()
        return False

    def method_33(self, treeView_0, treeNode_0):
        pass
        # using (Graphics graphic = treeView_0.CreateGraphics())
        # {
        #     int num = self.method_29(treeNode_0)
        #     int left = treeNode_0.Bounds.Left - num
        #     int width = treeView_0.ClientSize.Width
        #     Point[] point = new Point[5]
        #     Rectangle bounds = treeNode_0.Bounds
        #     point[0] = new Point(left, bounds.Top - 4)
        #     Rectangle rectangle = treeNode_0.Bounds
        #     point[1] = new Point(left, rectangle.Top + 4)
        #     Rectangle bounds1 = treeNode_0.Bounds
        #     point[2] = new Point(left + 4, bounds1.Y)
        #     Rectangle rectangle1 = treeNode_0.Bounds
        #     point[3] = new Point(left + 4, rectangle1.Top - 1)
        #     Rectangle bounds2 = treeNode_0.Bounds
        #     point[4] = new Point(left, bounds2.Top - 5)
        #     Point[] pointArray = point
        #     Point[] point1 = new Point[5]
        #     Rectangle rectangle2 = treeNode_0.Bounds
        #     point1[0] = new Point(width, rectangle2.Top - 4)
        #     Rectangle bounds3 = treeNode_0.Bounds
        #     point1[1] = new Point(width, bounds3.Top + 4)
        #     Rectangle rectangle3 = treeNode_0.Bounds
        #     point1[2] = new Point(width - 4, rectangle3.Y)
        #     Rectangle bounds4 = treeNode_0.Bounds
        #     point1[3] = new Point(width - 4, bounds4.Top - 1)
        #     Rectangle rectangle4 = treeNode_0.Bounds
        #     point1[4] = new Point(width, rectangle4.Top - 5)
        #     Point[] pointArray1 = point1
        #     graphic.FillPolygon(Brushes.Black, pointArray)
        #     graphic.FillPolygon(Brushes.Black, pointArray1)
        #     Pen pen = new Pen(System.Drawing.Color.Black, 2f)
        #     Point point2 = new Point(left, treeNode_0.Bounds.Top)
        #     Rectangle bounds5 = treeNode_0.Bounds
        #     graphic.DrawLine(pen, point2, new Point(width, bounds5.Top))
        # }

    def method_34(self, treeView_0, treeNode_0):
        pass
    #     using (Graphics graphic = treeView_0.CreateGraphics())
    #     {
    #         int num = self.method_29(treeNode_0)
    #         int left = treeNode_0.Bounds.Left - num
    #         int width = treeView_0.ClientSize.Width
    #         Point[] point = new Point[5]
    #         Rectangle bounds = treeNode_0.Bounds
    #         point[0] = new Point(left, bounds.Bottom - 4)
    #         Rectangle rectangle = treeNode_0.Bounds
    #         point[1] = new Point(left, rectangle.Bottom + 4)
    #         Rectangle bounds1 = treeNode_0.Bounds
    #         point[2] = new Point(left + 4, bounds1.Bottom)
    #         Rectangle rectangle1 = treeNode_0.Bounds
    #         point[3] = new Point(left + 4, rectangle1.Bottom - 1)
    #         Rectangle bounds2 = treeNode_0.Bounds
    #         point[4] = new Point(left, bounds2.Bottom - 5)
    #         Point[] pointArray = point
    #         Point[] point1 = new Point[5]
    #         Rectangle rectangle2 = treeNode_0.Bounds
    #         point1[0] = new Point(width, rectangle2.Bottom - 4)
    #         Rectangle bounds3 = treeNode_0.Bounds
    #         point1[1] = new Point(width, bounds3.Bottom + 4)
    #         Rectangle rectangle3 = treeNode_0.Bounds
    #         point1[2] = new Point(width - 4, rectangle3.Bottom)
    #         Rectangle bounds4 = treeNode_0.Bounds
    #         point1[3] = new Point(width - 4, bounds4.Bottom - 1)
    #         Rectangle rectangle4 = treeNode_0.Bounds
    #         point1[4] = new Point(width, rectangle4.Bottom - 5)
    #         Point[] pointArray1 = point1
    #         graphic.FillPolygon(Brushes.Black, pointArray)
    #         graphic.FillPolygon(Brushes.Black, pointArray1)
    #         Pen pen = new Pen(System.Drawing.Color.Black, 2f)
    #         Point point2 = new Point(left, treeNode_0.Bounds.Bottom)
    #         Rectangle bounds5 = treeNode_0.Bounds
    #         graphic.DrawLine(pen, point2, new Point(width, bounds5.Bottom))
    #     }
    # }

    def method_35(self, treeView_0, treeNode_0):
        pass
    #     using (Graphics graphic = treeView_0.CreateGraphics())
    #     {
    #         self.method_29(treeNode_0)
    #         int right = treeNode_0.Bounds.Right
    #         int width = treeView_0.ClientSize.Width
    #         int top = treeNode_0.Bounds.Top
    #         int bottom = treeNode_0.Bounds.Bottom
    #         Rectangle bounds = treeNode_0.Bounds
    #         int num = top + (bottom - bounds.Top) / 2
    #         Point[] point = new Point[] { new Point(right, num - 4), new Point(right, num + 4), new Point(right + 4, num), new Point(right + 4, num - 1), new Point(right, num - 5) }
    #         Point[] pointArray = point
    #         Point[] point1 = new Point[] { new Point(width, num - 4), new Point(width, num + 4), new Point(width - 4, num), new Point(width - 4, num - 1), new Point(width, num - 5) }
    #         Point[] pointArray1 = point1
    #         graphic.FillPolygon(Brushes.Black, pointArray)
    #         graphic.FillPolygon(Brushes.Black, pointArray1)
    #         graphic.DrawLine(new Pen(System.Drawing.Color.Black, 2f), new Point(right, num), new Point(width, num))
    #     }
    # }

    def method_36(self, treeView_0):
        self.ui.treeView_0.Refresh()
        self.dragNodeNewIndex = -1999
        self.dragTargetParentNode = None

    def method_4(self, treeNode_0, qarecord_0):
        treeNode = TreeNode(qarecord_0.Heading)
        for case in switch (qarecord_0.Type):
            if case(QARecordType.Unknown) or case(QARecordType.Table):
                treeNode.ImageKey = "Program.png"
                break
            elif case(QARecordType.Attached):
                treeNode.ImageKey = "Attachment.png"
                break
            elif case(QARecordType.Comment):
                treeNode.ImageKey = "Comment.png"
                break
            elif case(QARecordType.Snapshot):
                treeNode.ImageKey = "Snapshot.png"
                break
            elif case(QARecordType.Session):
                treeNode.ImageKey = "Session.png"
                break
        treeNode.SelectedImageKey = treeNode.ImageKey
        treeNode.Tag = qarecord_0
        treeNode_0.Nodes.Add(treeNode)
        for child in qarecord_0.Children:
            self.method_4(treeNode, child)

    def method_5(self, treeNode_0, qareportEntry_0):
        treeNode = TreeNode(qareportEntry_0.Title)
        str0 = "Session_None.png"
        if (qareportEntry_0.Value != None):
            for case in switch (qareportEntry_0.Value.Type):
                if case(QARecordType.Unknown) or case(QARecordType.Table):
                    str0 = "Program_{0}.png".format(qareportEntry_0.ColorCode.ToString())
                    break
                elif case(QARecordType.Attached):
                    str0 = "Attachment_{0}.png".format(qareportEntry_0.ColorCode.ToString())
                    break
                elif case(QARecordType.Comment):
                    str0 = "Comment_{0}.png".format(qareportEntry_0.ColorCode.ToString())
                    break
                elif case(QARecordType.Snapshot):
                    str0 = "Snapshot_{0}.png".format(qareportEntry_0.ColorCode.ToString())
                    break
        treeNode.ImageKey = str0
        treeNode.SelectedImageKey = str0
        treeNode.Tag = qareportEntry_0
        if (treeNode_0 != None):
            treeNode_0.Nodes.Add(treeNode)
        else:
            self.ui.treeViewReport.Nodes.Add(treeNode)
        if (qareportEntry_0.Children.Count != 0 or qareportEntry_0.Value == None):
            for child in qareportEntry_0.Children:
                self.method_5(treeNode, child)
        else:
            for qARecord in qareportEntry_0.Value.Children:
                self.method_6(treeNode, qARecord, str0)

    def method_6(self, treeNode_0, qarecord_0, string_0):
        treeNode = TreeNode(qarecord_0.Heading)
        treeNode.ImageKey = string_0
        treeNode.SelectedImageKey = string_0
        treeNode.Tag = qarecord_0
        treeNode_0.Nodes.Add(treeNode)
        for child in qarecord_0.Children:
            self.method_6(treeNode, child, string_0)

    def method_7(self):
        image = None
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.SelectedIndex == 0) else self.ui.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag# as QARecord
        if (tag != None):
            self.ui.lblDateTime.Text = tag.Stamp.smethod_19()
        else:
            qAReportEntry = treeNode.Tag# as QAReportEntry
            if (qAReportEntry == None):
                return
            self.ui.lblDateTime.seText(qAReportEntry.Stamp.smethod_19())
            tag = qAReportEntry.Value
            if (tag == None):
                self.method_22(None, True)
                return
        if (tag.Type != QARecordType.Snapshot):
            self.method_22(tag.method_7(), True)
            self.method_23(None, False)
        else:
            qASnapshot = tag# as QASnapshot
            if (qASnapshot != None):
                image = qASnapshot.Image
            else:
                image = None
            self.method_23(image, True)
            self.method_22(None, False)
        self.method_20()

    def method_8(self, qarecord_0):
        treeNode = None
        for node in self.ui.treeView.Nodes:
            if (node.Tag != qarecord_0):
                continue
            treeNode = node
            return treeNode
        treeNode1 = None
        enumerator = self.ui.treeView.Nodes#.GetEnumerator()
        for cur in enumerator:
            treeNode1 = self.method_9(cur, qarecord_0)
            if (treeNode1 == None):
                continue
            treeNode = treeNode1
            return treeNode
        return treeNode

    def method_9(self, treeNode_0, qarecord_0):
        treeNode = None
        if (treeNode_0.Tag == qarecord_0):
            return treeNode_0
        treeNode1 = None
        enumerator = treeNode_0.Nodes#.GetEnumerator()
        for cur in enumerator:
            treeNode1 = self.method_9(cur, qarecord_0)
            if (treeNode1 == None):
                continue
            treeNode = treeNode1
            return treeNode
        return treeNode

    def mniCopyToReport_Click(self):
        selectedNode = self.ui.treeView.SelectedNode
        if (selectedNode == None):
            return
        tag = selectedNode.Tag# as QARecord
        if (tag == None):
            return
        treeNode = self.method_13(tag)
        if (treeNode != None):
            self.treeViewReport.SelectedNode = treeNode
            return
        treeNode1 = None
        qAReportEntry = QAReportEntry()
        qAReportEntry.Value = tag
        self.activeDocument.ReportEntries.Add(qAReportEntry)
        self.method_5(treeNode1, qAReportEntry)
        self.ui.treeViewReport.SelectedNode = self.ui.treeViewReport.Nodes[self.ui.treeViewReport.Nodes.Count - 1]
        self.activeDocument.method_2(self)

    def mniFileClose_Click(self):
        self.hide()

    def mniFlagYellow_Click(self, sender):
        selectedNode = self.ui.treeViewReport.SelectedNode
        if (selectedNode == None):
            return
        qAColorCode = QAColorCode.None
        if (sender == self.ui.mniFlagBlue):
            qAColorCode = QAColorCode.Blue
        elif (sender == self.ui.mniFlagRed):
            qAColorCode = QAColorCode.Red
        elif (sender == self.ui.mniFlagGreen):
            qAColorCode = QAColorCode.Green
        elif (sender == self.ui.mniFlagMagenta):
            qAColorCode = QAColorCode.Magenta
        elif (sender == self.ui.mniFlagCyan):
            qAColorCode = QAColorCode.Cyan
        elif (sender == self.ui.mniFlagYellow):
            qAColorCode = QAColorCode.Yellow
        tag = selectedNode.Tag# as QAReportEntry
        if (tag == None):
            return
        value = tag.Value
        if (value == None):
            return
        tag.ColorCode = qAColorCode
        str0 = self.method_18(value.Type, qAColorCode)
        selectedNode.ImageKey = str0
        selectedNode.SelectedImageKey = str0
        for node in selectedNode.Nodes:
            node.ImageKey = str0
            node.SelectedImageKey = str0
        self.method_19()
        self.activeDocument.method_2(self)

    def mniNewFolder_Click(self):
        qAReportEntry = QAReportEntry()
        self.activeDocument.ReportEntries.Add(qAReportEntry)
        self.method_5(None, qAReportEntry)
        self.ui.treeViewReport.SelectedNode = self.ui.treeViewReport.Nodes[self.ui.treeViewReport.Nodes.Count - 1]
        self.ui.treeViewReport.SelectedNode.BeginEdit()
        self.activeDocument.method_2(self)

    def mniQaComment_Click(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.SelectedIndex == 0) else self.ui.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag #as QAComment
        if (tag == None):
            qAReportEntry = treeNode.Tag #as QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value #as QAComment
            if (tag == None):
                return
        text = tag.Text
        result, text = QA.smethod_4(self, text)
        if (result):
            tag.Text = text
            self.activeDocument.method_2(self)
            self.method_7()

    def mniQaCopy_Click(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.SelectedIndex == 0) else self.ui.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag #as QARecord
        if (tag == None):
            qAReportEntry = treeNode.Tag #as QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value
            if (tag == None):
                return
        tag.method_11()

    def mniQaDelete_Click(self):
        if (self.activeDocument == None):
            return
        if (self.lastSessionNode == None):
            return
        if (self.ui.tabControl.SelectedIndex != 0):
            selectedNode = self.ui.treeViewReport.SelectedNode
            if (selectedNode == None):
                return
            tag = selectedNode.Tag #as QAReportEntry
            if (tag == None):
                return
            if (selectedNode.Parent != None):
                selectedNode.Parent.Tag.Children.Remove(tag)
            else:
                self.activeDocument.ReportEntries.Remove(tag)
            if (selectedNode.NextNode != None):
                self.ui.treeView.SelectedNode = selectedNode.NextNode
            elif (selectedNode.PrevNode == None):
                self.ui.treeView.SelectedNode = selectedNode.Parent
            else:
                self.ui.treeView.SelectedNode = selectedNode.PrevNode
            selectedNode.Remove()
            self.method_19()
            self.activeDocument.method_2(self)
        else:
            treeNode = self.ui.treeView.SelectedNode
            if (treeNode == None):
                return
            if (treeNode.Level == 0):
                return
            if (treeNode.Level > 1):
                treeNode = self.method_10(treeNode, 1)
            if (self.method_10(treeNode, 0) != self.lastSessionNode):
                return
            qARecord = treeNode.Tag
            if (qARecord == None):
                return
            qASession = self.lastSessionNode.Tag
            if (qASession == None):
                return
            if (QMessageBox.warning(self, "Warning", Confirmations.DELETE_SELECTED_ENTRY, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
                if (treeNode.NextNode != None):
                    self.ui.treeView.SelectedNode = treeNode.NextNode
                elif (treeNode.PrevNode == None):
                    self.ui.treeView.SelectedNode = treeNode.Parent
                else:
                    self.ui.treeView.SelectedNode = treeNode.PrevNode
                treeNode.Remove()
                qASession.Children.Remove(qARecord)
                treeNode = self.method_13(qARecord)
                if (treeNode != None):
                    qAReportEntry = treeNode.Tag #as QAReportEntry
                    if (qAReportEntry == None):
                        return
                    if (treeNode.Parent != None):
                        treeNode.Parent.Tag.Children.Remove(qAReportEntry)
                    else:
                        self.activeDocument.ReportEntries.Remove(qAReportEntry)
                    treeNode.Remove()
                self.activeDocument.method_2(self)
                return

    def mniQaExportSST_Click(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.SelectedIndex == 0) else self.ui.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag #as QASnapshot
        if (tag == None):
            qAReportEntry = treeNode.Tag #as QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value #as QASnapshot
            if (tag == None):
                return
        # filter = ""#FileDialogFilters.SAVE_SNAPSHOT
        # if (tag.ImageFormatType == QASnapshotFormat.Gif):
        #     self.sfd.DefaultExt = "png"
        #     self.sfd.FilterIndex = 0
        # }
        # else if (tag.ImageFormatType == QASnapshotFormat.Png)
        # {
        #     self.sfd.DefaultExt = "png"
        #     self.sfd.FilterIndex = 1
        # }
        # else if (tag.ImageFormatType == QASnapshotFormat.Jpeg)
        # {
        #     self.sfd.DefaultExt = "jpg"
        #     self.sfd.FilterIndex = 2
        # }
        # self.sfd.FileName = ""
        # if (self.sfd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
        # {
        #     using (Image image = tag.Image)
        #     {
        #         if (self.sfd.FileName.EndsWith(".gif", StringComparison.OrdinalIgnoreCase))
        #         {
        #             image.Save(self.sfd.FileName, ImageFormat.Gif)
        #         }
        #         else if (self.sfd.FileName.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
        #         {
        #             image.Save(self.sfd.FileName, ImageFormat.Png)
        #         }
        #         else if (self.sfd.FileName.EndsWith(".jpg", StringComparison.OrdinalIgnoreCase) or self.sfd.FileName.EndsWith(".jpeg", StringComparison.OrdinalIgnoreCase))
        #         {
        #             image.Save(self.sfd.FileName, ImageHelper.smethod_2(ImageFormat.Jpeg), ImageHelper.smethod_3(QA.JpegQuality))
        #         }
        #         else if (self.sfd.FileName.EndsWith(".bmp", StringComparison.OrdinalIgnoreCase))
        #         {
        #             image.Save(self.sfd.FileName, ImageFormat.Bmp)
        #         }
        #     }
        #

    def mniQaExportWord_Click(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.SelectedIndex == 0) else self.ui.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag #as QARecord
        if (tag == None):
            qAReportEntry = treeNode.Tag #as QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value
            if (tag == None):
                return
        QA.smethod_3(self, tag)

    def mniQaRestoreView_Click(self):
        treeNode = self.ui.treeView.SelectedNode if(self.ui.tabControl.SelectedIndex == 0) else self.ui.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag #as QASnapshot
        if (tag == None):
            qAReportEntry = treeNode.Tag #as QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value #as QASnapshot
            if (tag == None):
                return
        QA.smethod_5(self, tag)

    def mniRichTextCopy_Click(self):
        self.ui.richBox.copy()

    def mnuEntries_Opening(self):
        flag = False
        flag1 = False
        self.ui.mniFlags.setVisible(self.isFlagAvailable)
        self.ui.mniQaCopy.setVisible(self.isCopyAvailable)
        self.ui.mniQaDelete.setVisible(self.isDeleteAvailable)
        self.ui.mniQaExportWord.setVisible(self.isExportToWordAvailable)
        self.ui.mniQaComment.stVisible(self.isEditCommentAvailable)
        self.ui.mniQaExportSST.setVisible(self.isSnapshotActionAvailable)
        self.ui.mniQaRestoreView.setVisible(self.isSnapshotActionAvailable)
        self.ui.mniCopyToReport.setVisible(self.isCopyEntryToReportAvailable)
        flag2 = self.isFlagAvailable
        flag3 = True if(self.isCopyAvailable) else self.isDeleteAvailable
        flag4 = True if(self.isExportToWordAvailable or self.isEditCommentAvailable) else self.isSnapshotActionAvailable
        flag5 = self.isCopyEntryToReportAvailable
        toolStripSeparator = self.mniQaSep1
        if (not flag2):
            flag = False
        else:
            flag = True if(flag3 or flag4) else flag5
        toolStripSeparator.setVisible(flag)
        toolStripSeparator1 = self.mniQaSep2
        if (not flag3):
            flag1 = False
        else:
            flag1 = True if(flag4) else flag5
        toolStripSeparator1.setVisible(flag1)
        self.mniQaSep3.Visible = False if(not flag4) else flag5

    def mnuFolders_Opening(self):
        pass

    def mnuRichText_Opening(self):
        self.ui.mniRichTextCopy.setEnabled(not String.IsNoneOrEmpty(self.ui.richBox.extraSelections()))

    def picSnapshot_MouseClick(self):
        self.ui.picSnapshot.Focus()

    def picSnapshot_MouseEnter(self):
        self.ui.picSnapshot.Focus()

    def ProcessCmdKey(self, msg, keyData):
        pass
        # if (msg.Msg == 256 or msg.Msg == 260):
        #     cancelEventArg = CancelEventArgs(False)
        #     key = keyData
        #     if (key <= (Keys.RButton | Keys.ShiftKey | Keys.Menu | Keys.B | Keys.P | Keys.R | Keys.Control)):
        #         if (key == (Keys.RButton | Keys.MButton | Keys.XButton2 | Keys.Back | Keys.LineFeed | Keys.Clear | Keys.Space | Keys.Next | Keys.PageDown | Keys.Home | Keys.Up | Keys.Down | Keys.Print | Keys.Snapshot | Keys.PrintScreen | Keys.Delete | Keys.Shift)):
        #             if (self.isDeleteAvailable):
        #                 self.mniQaDelete_Click(self.btnDelete, EventArgs.Empty)
        #             return True, msg
        #         if (key == (Keys.LButton | Keys.RButton | Keys.Cancel | Keys.A | Keys.B | Keys.C | Keys.Control)):
        #             if (self.richBox.Focused and !string.IsNoneOrEmpty(self.richBox.SelectedText)):
        #                 return base.ProcessCmdKey(ref msg, keyData)
        #             if (self.txtHeading.Focused and !string.IsNoneOrEmpty(self.txtHeading.SelectedText)):
        #                 return base.ProcessCmdKey(ref msg, keyData)
        #             if (self.txtComment.Focused and !string.IsNoneOrEmpty(self.txtComment.SelectedText)):
        #                 return base.ProcessCmdKey(ref msg, keyData)
        #             if (self.labelEditInProgress):
        #                 return base.ProcessCmdKey(ref msg, keyData)
        #             self.mniQaCopy_Click(self.btnCopy, EventArgs.Empty)
        #             return True, msg
        #         switch (key)
        #         {
        #             case Keys.LButton | Keys.ShiftKey | Keys.ControlKey | Keys.A | Keys.P | Keys.Q | Keys.Control:
        #             {
        #                 if (self.isExportQaAvailable)
        #                 {
        #                     self.btnExportQA_Click(self.btnExportQA, EventArgs.Empty)
        #                 }
        #                 return True, msg
        #             }
        #             case Keys.RButton | Keys.ShiftKey | Keys.Menu | Keys.B | Keys.P | Keys.R | Keys.Control:
        #             {
        #                 if (self.isExportReportAvailable)
        #                 {
        #                     self.btnExportReport_Click(self.btnExportReport, EventArgs.Empty)
        #                 }
        #                 return True, msg
        #             }
        #         }
        #     }
        #     else if (key > (Keys.LButton | Keys.RButton | Keys.Cancel | Keys.A | Keys.B | Keys.C | Keys.Shift | Keys.Control))
        #     {
        #         if (key == (Keys.RButton | Keys.MButton | Keys.XButton2 | Keys.Back | Keys.LineFeed | Keys.Clear | Keys.B | Keys.D | Keys.F | Keys.H | Keys.J | Keys.L | Keys.N | Keys.Shift | Keys.Control))
        #         {
        #             if (self.loaded and self.tabControl.SelectedIndex == 1)
        #             {
        #                 self.mniNewFolder_Click(self.mniNewFolder, EventArgs.Empty)
        #             }
        #             return True, msg
        #         }
        #         if (key == (Keys.LButton | Keys.RButton | Keys.Cancel | Keys.ShiftKey | Keys.ControlKey | Keys.Menu | Keys.Pause | Keys.Space | Keys.Prior | Keys.PageUp | Keys.Next | Keys.PageDown | Keys.End | Keys.D0 | Keys.D1 | Keys.D2 | Keys.D3 | Keys.A | Keys.B | Keys.C | Keys.P | Keys.Q | Keys.R | Keys.S | Keys.NumPad0 | Keys.NumPad1 | Keys.NumPad2 | Keys.NumPad3 | Keys.F1 | Keys.F2 | Keys.F3 | Keys.F4 | Keys.Alt))
        #         {
        #             self.mniFileClose_Click(self.mniFileClose, EventArgs.Empty)
        #             return True, msg
        #         }
        #     }
        #     else
        #     {
        #         if (key == (Keys.LButton | Keys.RButton | Keys.Cancel | Keys.MButton | Keys.XButton1 | Keys.XButton2 | Keys.ShiftKey | Keys.ControlKey | Keys.Menu | Keys.Pause | Keys.Capital | Keys.CapsLock | Keys.KanaMode | Keys.HanguelMode | Keys.HangulMode | Keys.JunjaMode | Keys.A | Keys.B | Keys.C | Keys.D | Keys.E | Keys.F | Keys.G | Keys.P | Keys.Q | Keys.R | Keys.S | Keys.T | Keys.U | Keys.V | Keys.W | Keys.Control))
        #         {
        #             if (self.isExportToWordAvailable)
        #             {
        #                 self.mniQaExportWord_Click(self.btnExportWord, EventArgs.Empty)
        #             }
        #             return True, msg
        #         }
        #         if (key == (Keys.LButton | Keys.RButton | Keys.Cancel | Keys.A | Keys.B | Keys.C | Keys.Shift | Keys.Control))
        #         {
        #             if (self.isCopyEntryToReportAvailable)
        #             {
        #                 self.mniCopyToReport_Click(self.mniCopyToReport, EventArgs.Empty)
        #             }
        #             return True, msg
        #         }
        #     }
        # }
        # return base.ProcessCmdKey(ref msg, keyData), msg
    # }
    #
    # private void QaWindow_FormClosing(object sender, FormClosingEventArgs e)
    # {
    #     if (e.CloseReason == System.Windows.Forms.CloseReason.UserClosing)
    #     {
    #         e.Cancel = True
    #         base.Hide()
    #     }
    # }
    #
    # private void QaWindow_Layout(object sender, LayoutEventArgs e)
    # {
    #     if (self.loaded and base.WindowState != FormWindowState.Minimized)
    #     {
    #         self.previousState = base.WindowState
    #     }
    # }
    #
    # private void QaWindow_Load(object sender, EventArgs e)
    # {
    #     Application.Idle += new EventHandler(self.method_0)
    #     self.lblDateTime.Font = new System.Drawing.Font(self.Font.FontFamily, self.Font.Size + 1f, System.Drawing.FontStyle.Bold)
    #     self.boldFont = new System.Drawing.Font(self.treeView.Font, System.Drawing.FontStyle.Bold)
    #     base.SetBounds(self.location.X, self.location.Y, self.size.Width, self.size.Height, self.boundsSpecified)
    #     self.loaded = True
    # }
    #
    # private void QaWindow_Move(object sender, EventArgs e)
    # {
    #     if (self.loaded and base.WindowState == FormWindowState.Normal)
    #     {
    #         self.location = base.Location
    #     }
    # }
    #
    # private void QaWindow_Resize(object sender, EventArgs e)
    # {
    #     if (self.loaded and base.WindowState == FormWindowState.Normal)
    #     {
    #         self.size = base.Size
    #     }
    #     self.richBox.RightMargin = self.richBox.ClientRectangle.Width - 4
    # }
    #
    # private void QaWindow_Shown(object sender, EventArgs e)
    # {
    #     if (!self.shown)
    #     {
    #         self.method_1(self.splitterDistance)
    #         self.shown = True
    #     }
    #     self.richBox.RightMargin = self.richBox.ClientRectangle.Width - 4
    #     Screen[] allScreens = Screen.AllScreens
    #     int num = 0
    #     while (True)
    #     {
    #         if (num >= (int)allScreens.Length)
    #         {
    #             Rectangle workingArea = Screen.PrimaryScreen.WorkingArea
    #             self.Location = new Point(Math.Max(10, workingArea.Left + (workingArea.Width - base.Width) / 2), Math.Max(10, workingArea.Top + (int)((double)(workingArea.Height - base.Height) / 2)))
    #             break
    #         }
    #         else if (allScreens[num].WorkingArea.Contains(self.Location))
    #         {
    #             break
    #         }
    #         else
    #         {
    #             num++
    #         }
    #     }
    # }
    #
    # private void richBox_MouseDown(object sender, MouseEventArgs e)
    # {
    #     if (e.Button == System.Windows.Forms.MouseButtons.Right)
    #     {
    #         self.mnuRichText.Show(self.richBox.PointToScreen(e.Location))
    #     }
    # }
    #
    # private void tabControl_SelectedIndexChanged(object sender, EventArgs e)
    # {
    #     if (self.treeView.Nodes.Count > 0)
    #     {
    #         self.method_7()
    #         return
    #     }
    #     self.method_22(None, True)
    # }
    #
    # private void treeView_AfterLabelEdit(object sender, NodeLabelEditEventArgs e)
    # {
    #     if (string.IsNoneOrEmpty(e.Label) or string.IsNoneOrEmpty(e.Label.Trim()))
    #     {
    #         e.CancelEdit = True
    #         self.labelEditInProgress = False
    #         return
    #     }
    #     QARecord tag = (QARecord)e.Node.Tag
    #     if (tag != None and self.method_16())
    #     {
    #         tag.Heading = e.Label
    #         TreeNode label = self.method_13(tag)
    #         if (label != None)
    #         {
    #             label.Text = e.Label
    #         }
    #         self.activeDocument.method_2(self)
    #     }
    #     self.labelEditInProgress = False
    # }
    #
    # private void treeView_AfterSelect(object sender, TreeViewEventArgs e)
    # {
    #     if (e.Node == None)
    #     {
    #         self.method_22(None, True)
    #         return
    #     }
    #     self.activeDocument.SelectedRecord = (QARecord)e.Node.Tag
    #     self.method_7()
    # }
    #
    # private void treeView_BeforeLabelEdit(object sender, NodeLabelEditEventArgs e)
    # {
    #     if (e.Node != None and !self.method_16())
    #     {
    #         e.CancelEdit = True
    #     }
    #     self.labelEditInProgress = !e.CancelEdit
    # }
    #
    # private void treeView_BeforeSelect(object sender, TreeViewCancelEventArgs e)
    # {
    #     self.method_14((sender as TreeView).SelectedNode, False)
    #     self.method_14(e.Node, True)
    # }
    #
    # private void treeView_DragDrop(object sender, DragEventArgs e)
    # {
    #     try
    #     {
    #         TreeNode data = e.Data.GetData(typeof(TreeNode)) as TreeNode
    #         if (self.dragNodeNewIndex != -1999 and data != None and data.Tag is QARecord)
    #         {
    #             QARecord tag = data.Tag as QARecord
    #             int num = (self.dragNodeNewIndex < data.Index ? self.dragNodeNewIndex : self.dragNodeNewIndex - 1)
    #             TreeNode treeNode = self.lastSessionNode
    #             QASession qASession = treeNode.Tag as QASession
    #             treeNode.Nodes.Remove(data)
    #             qASession.Children.Remove(tag)
    #             self.lastSessionNode.Nodes.Insert(num, data)
    #             qASession.Children.Insert(num, tag)
    #             self.treeView.SelectedNode = data
    #             self.activeDocument.method_2(self)
    #         }
    #     }
    #     catch (Exception exception)
    #     {
    #     }
    #     self.method_36(self.treeView)
    # }
    #
    # private void treeView_DragLeave(object sender, EventArgs e)
    # {
    #     self.method_36(self.treeView)
    # }
    #
    # private void treeView_DragOver(object sender, DragEventArgs e)
    # {
    #     try
    #     {
    #         TreeView treeView = (TreeView)sender
    #         e.Effect = DragDropEffects.None
    #         TreeNode data = e.Data.GetData(typeof(TreeNode)) as TreeNode
    #         if (data != None and data.Tag is QARecord)
    #         {
    #             TreeNode nodeAt = treeView.GetNodeAt(treeView.PointToClient(new Point(e.X, e.Y)))
    #             if (nodeAt != None and nodeAt.Level == 1 and self.method_10(nodeAt, 0) == self.lastSessionNode)
    #             {
    #                 Point client = treeView.PointToClient(System.Windows.Forms.Cursor.Position)
    #                 int y = client.Y - nodeAt.Bounds.Top
    #                 self.method_29(nodeAt)
    #                 treeView.CreateGraphics()
    #                 int num = (y < nodeAt.Bounds.Height / 2 ? nodeAt.Index : nodeAt.Index + 1)
    #                 bool flag = True
    #                 if (num >= 0 and num < data.Parent.Nodes.Count)
    #                 {
    #                     TreeNode item = data.Parent.Nodes[num]
    #                     Rectangle bounds = item.Bounds
    #                     Rectangle clientRectangle = item.TreeView.ClientRectangle
    #                     if (bounds.Top < clientRectangle.Top or bounds.Bottom > clientRectangle.Bottom)
    #                     {
    #                         item.EnsureVisible()
    #                         flag = False
    #                     }
    #                 }
    #                 if (nodeAt != data and (nodeAt.Index > data.Index ? num != data.Index + 1 : num != data.Index))
    #                 {
    #                     e.Effect = DragDropEffects.Move
    #                     if (num != self.dragNodeNewIndex or !flag)
    #                     {
    #                         if (y >= nodeAt.Bounds.Height / 2)
    #                         {
    #                             self.method_36(treeView)
    #                             self.method_34(treeView, nodeAt)
    #                         }
    #                         else
    #                         {
    #                             self.method_36(treeView)
    #                             self.method_33(treeView, nodeAt)
    #                         }
    #                         self.dragNodeNewIndex = num
    #                         return
    #                     }
    #                     else
    #                     {
    #                         return
    #                     }
    #                 }
    #             }
    #         }
    #         if (self.dragNodeNewIndex != -1999)
    #         {
    #             self.method_36(treeView)
    #         }
    #     }
    #     catch (Exception exception)
    #     {
    #     }
    # }
    #
    # private void treeView_ItemDrag(object sender, ItemDragEventArgs e)
    # {
    #     TreeNode item = e.Item as TreeNode
    #     if (item != None and item.Level == 1 and self.method_10(item, 0) == self.lastSessionNode)
    #     {
    #         self.treeView.SelectedNode = item
    #         self.treeView.DoDragDrop(item, DragDropEffects.Move)
    #     }
    # }
    #
    # private void treeView_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
    # {
    #     if (e.Button == System.Windows.Forms.MouseButtons.Right)
    #     {
    #         (sender as TreeView).SelectedNode = e.Node
    #         self.mnuEntries.Show(System.Windows.Forms.Cursor.Position)
    #     }
    # }
    #
    # private void treeViewReport_AfterLabelEdit(object sender, NodeLabelEditEventArgs e)
    # {
    #     if (!string.IsNoneOrEmpty(e.Label) and !string.IsNoneOrEmpty(e.Label.Trim()))
    #     {
    #         QAReportEntry tag = e.Node.Tag as QAReportEntry
    #         if (tag != None)
    #         {
    #             tag.Title = e.Label
    #             self.activeDocument.method_2(self)
    #             self.labelEditInProgress = False
    #             return
    #         }
    #     }
    #     e.CancelEdit = True
    #     self.labelEditInProgress = False
    # }
    #
    # private void treeViewReport_AfterSelect(object sender, TreeViewEventArgs e)
    # {
    #     if (e.Node == None)
    #     {
    #         self.method_22(None, True)
    #         return
    #     }
    #     self.activeDocument.SelectedReportEntry = self.method_11(e.Node)
    #     self.method_7()
    # }
    #
    # private void treeViewReport_BeforeLabelEdit(object sender, NodeLabelEditEventArgs e)
    # {
    #     if (e.Node != None and e.Node.Tag is QARecord)
    #     {
    #         e.CancelEdit = True
    #     }
    #     self.labelEditInProgress = !e.CancelEdit
    # }
    #
    # private void treeViewReport_BeforeSelect(object sender, TreeViewCancelEventArgs e)
    # {
    #     self.method_14((sender as TreeView).SelectedNode, False)
    #     self.method_14(e.Node, True)
    # }
    #
    # private void treeViewReport_DragDrop(object sender, DragEventArgs e)
    # {
    #     try
    #     {
    #         TreeNode data = e.Data.GetData(typeof(TreeNode)) as TreeNode
    #         if (self.dragNodeNewIndex != -1999 and data != None and data.Tag is QAReportEntry)
    #         {
    #             QAReportEntry tag = data.Tag as QAReportEntry
    #             int num = self.dragNodeNewIndex
    #             if (data.Parent == self.dragTargetParentNode and self.dragNodeNewIndex >= data.Index)
    #             {
    #                 num = self.dragNodeNewIndex - 1
    #             }
    #             if (data.Parent != None)
    #             {
    #                 (data.Parent.Tag as QAReportEntry).Children.Remove(tag)
    #             }
    #             else
    #             {
    #                 self.activeDocument.ReportEntries.Remove(tag)
    #             }
    #             data.Remove()
    #             if (self.dragTargetParentNode != None)
    #             {
    #                 self.dragTargetParentNode.Nodes.Insert(num, data)
    #                 (self.dragTargetParentNode.Tag as QAReportEntry).Children.Insert(num, tag)
    #             }
    #             else
    #             {
    #                 self.treeViewReport.Nodes.Insert(num, data)
    #                 self.activeDocument.ReportEntries.Insert(num, tag)
    #             }
    #             self.treeViewReport.SelectedNode = data
    #             self.method_19()
    #             self.activeDocument.method_2(self)
    #         }
    #     }
    #     catch (Exception exception)
    #     {
    #     }
    #     self.method_36(self.treeViewReport)
    # }
    #
    # private void treeViewReport_DragLeave(object sender, EventArgs e)
    # {
    #     self.method_36(self.treeViewReport)
    # }
    #
    # private void treeViewReport_DragOver(object sender, DragEventArgs e)
    # {
    #     try
    #     {
    #         TreeView treeView = (TreeView)sender
    #         e.Effect = DragDropEffects.None
    #         TreeNode data = e.Data.GetData(typeof(TreeNode)) as TreeNode
    #         if (data != None and data.Tag is QAReportEntry)
    #         {
    #             TreeNode nodeAt = treeView.GetNodeAt(treeView.PointToClient(new Point(e.X, e.Y)))
    #             if (nodeAt != None and nodeAt.Tag is QAReportEntry)
    #             {
    #                 bool value = (data.Tag as QAReportEntry).Value == None
    #                 bool flag = (nodeAt.Tag as QAReportEntry).Value == None
    #                 bool flag1 = flag
    #                 if (flag)
    #                 {
    #                     nodeAt.Expand()
    #                 }
    #                 if (!value or nodeAt.Parent == None)
    #                 {
    #                     Point client = self.treeViewReport.PointToClient(System.Windows.Forms.Cursor.Position)
    #                     int y = client.Y - nodeAt.Bounds.Top
    #                     bool flag2 = (y < 5 ? False : y <= nodeAt.Bounds.Height - 5)
    #                     if (value and flag1)
    #                     {
    #                         flag2 = False
    #                     }
    #                     int num = (y < nodeAt.Bounds.Height / 2 ? nodeAt.Index : nodeAt.Index + 1)
    #                     if (nodeAt.Parent == data.Parent)
    #                     {
    #                         if (data.NextNode == None and num > data.Index)
    #                         {
    #                             if (self.dragNodeNewIndex != -1999)
    #                             {
    #                                 self.method_36(treeView)
    #                             }
    #                             return
    #                         }
    #                         else if (data.PrevNode == None and num == 0)
    #                         {
    #                             if (self.dragNodeNewIndex != -1999)
    #                             {
    #                                 self.method_36(treeView)
    #                             }
    #                             return
    #                         }
    #                         else if (data.Index == num or data.Index == num - 1)
    #                         {
    #                             if (self.dragNodeNewIndex != -1999)
    #                             {
    #                                 self.method_36(treeView)
    #                             }
    #                             return
    #                         }
    #                     }
    #                     bool flag3 = True
    #                     if (!self.method_30(nodeAt))
    #                     {
    #                         flag3 = False
    #                     }
    #                     if (!self.method_31(nodeAt))
    #                     {
    #                         flag3 = False
    #                     }
    #                     e.Effect = DragDropEffects.Move
    #                     if (flag1 and nodeAt.Nodes.Count == 0 and flag2)
    #                     {
    #                         num = 0
    #                     }
    #                     if (num != self.dragNodeNewIndex or !flag3)
    #                     {
    #                         if (flag1 and nodeAt.Nodes.Count == 0 and flag2)
    #                         {
    #                             self.method_36(treeView)
    #                             self.method_35(treeView, nodeAt)
    #                         }
    #                         else if (y >= nodeAt.Bounds.Height / 2)
    #                         {
    #                             self.method_36(treeView)
    #                             self.method_34(treeView, nodeAt)
    #                         }
    #                         else
    #                         {
    #                             self.method_36(treeView)
    #                             self.method_33(treeView, nodeAt)
    #                         }
    #                         self.dragNodeNewIndex = num
    #                         if (flag1 and nodeAt.Nodes.Count == 0 and flag2)
    #                         {
    #                             self.dragTargetParentNode = nodeAt
    #                         }
    #                         else if (flag1)
    #                         {
    #                             self.dragTargetParentNode = None
    #                         }
    #                         else if (nodeAt.Parent != None)
    #                         {
    #                             self.dragTargetParentNode = nodeAt.Parent
    #                         }
    #                         else
    #                         {
    #                             self.dragTargetParentNode = None
    #                         }
    #                     }
    #                 }
    #                 else if (self.dragNodeNewIndex != -1999)
    #                 {
    #                     self.method_36(treeView)
    #                 }
    #             }
    #             else if (self.dragNodeNewIndex != -1999)
    #             {
    #                 self.method_36(treeView)
    #             }
    #         }
    #         else if (self.dragNodeNewIndex != -1999)
    #         {
    #             self.method_36(treeView)
    #         }
    #     }
    #     catch (Exception exception)
    #     {
    #     }
    # }
    #
    # private void treeViewReport_ItemDrag(object sender, ItemDragEventArgs e)
    # {
    #     TreeNode item = e.Item as TreeNode
    #     if (item == None)
    #     {
    #         return
    #     }
    #     if (!(item.Tag is QAReportEntry))
    #     {
    #         return
    #     }
    #     self.treeViewReport.SelectedNode = item
    #     self.treeViewReport.DoDragDrop(item, DragDropEffects.Move)
    # }
    #
    # private void treeViewReport_MouseUp(object sender, MouseEventArgs e)
    # {
    #     if (self.treeView.Nodes.Count > 0 and e.Button == System.Windows.Forms.MouseButtons.Right and self.treeViewReport.HitTest(e.Location).Node == None)
    #     {
    #         self.mnuFolders.Show(System.Windows.Forms.Cursor.Position)
    #     }
    # }
    #
    # private void treeViewReport_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
    # {
    #     if (e.Button == System.Windows.Forms.MouseButtons.Right)
    #     {
    #         (sender as TreeView).SelectedNode = e.Node
    #         self.mnuEntries.Show(System.Windows.Forms.Cursor.Position)
    #     }
    # }
    #
    # private void txtHeading_TextChanged(object sender, EventArgs e)
    # {
    #     self.method_20()
    # }