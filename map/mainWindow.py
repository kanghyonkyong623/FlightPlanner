import os

from PyQt4 import QtGui
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl, Qt, SIGNAL, QCoreApplication, QDir, QFileInfo, QSettings, QObject

from PyQt4.QtGui import QMainWindow, QSizePolicy, QWidget, QVBoxLayout, QAction, QColor, QPixmap, QLabel,\
     QIcon, QMessageBox, QFrame, QFileDialog, QFont, QMenu, QDockWidget, QApplication, QToolButton, QCursor, QTabBar
from PyQt4.QtGui import QDialog, QDesktopServices

from qgis.core import QgsRasterLayer, QgsDistanceArea, QgsCoordinateReferenceSystem,\
     QgsRectangle, QgsProject, QgsPluginLayer, QgsLayerTreeNode, \
     QgsLayerTree, QgsMapLayerRegistry, QgsMapLayer, QgsVectorDataProvider, QgsSnapper,\
     QgsTolerance, QgsApplication, QgsLayerTreeModel
from qgis.core import QgsPalLayerSettings, QGis, QgsVectorLayer, QgsFeature,\
     QgsRasterBandStats, QgsRasterShader, QgsColorRampShader, QgsSingleBandPseudoColorRenderer

from qgis.gui import QgsMapCanvas, QgsLayerTreeView, QgsGenericProjectionSelector, QgsMessageBar, QgsMapToolPan, QgsMapToolZoom, \
     QgsExpressionSelectionDialog, QgsLayerTreeMapCanvasBridge, QgsMapOverviewCanvas, QgsScaleComboBox

from map.VectorEditTool.mapToolFeature import QgsMapToolAddFeature, QgsMapToolMoveFeature, QgsMapToolNodeTool, QgsMapToolAddCircularString
from FlightPlanner.AerodromeSurfaces.AerodromeSurfacesDlg import AerodromeSurfacesDlg
from FlightPlanner.Shielding.ShieldingDlg import ShieldingDlg
from FlightPlanner.BaroVNAV.BaroVNAVDlg import BaroVNAVDlg
from FlightPlanner.BasicGNSS.basicGNSSDlg0 import basicGNSSDlg
from FlightPlanner.ApproachAlignmentConstruction.ApproachACDlg import ApproachACDlg
from FlightPlanner.Ils.OasDlg import OasDlg
from FlightPlanner.RnpAR.RnpARDlg import RnpARDlg
from FlightPlanner.PinSVisualSegment.PinSVisualSegmentDep import PinSVisualSegmentDepDlg
from FlightPlanner.PinSVisualSegment.PinSVisualSegmentApp import PinSVisualSegmentAppDlg
from FlightPlanner.PinSVisualSegment.VisualSegmentSurface import VisualSegmentSurfaceDlg
from FlightPlanner.TaaCalculation.TaaCalculationDlg import TaaCalculationDlg
from FlightPlanner.BaseTurnTS.BaseTurnTSDlg import BaseTurnTSDlg 
from FlightPlanner.IIsCrm.CrmDlg import CrmDlg 
from FlightPlanner.Holding.HoldingRnp.HoldingRnpDlg import HoldingRnpDlg 
from FlightPlanner.DepartureNominal.DepartureNominalDlg import DepartureNominalDlg
from FlightPlanner.DepartureRnav.DepartureRnavDlg import DepartureRnavDlg
from FlightPlanner.DepartureStandard.DepartureStandardDlg import DepartureStandardDlg
from FlightPlanner.DepartureOmnidirectional.DepartureOmnidirectionalDlg import DepartureOmnidirectionalDlg  
from FlightPlanner.DmeTolerance.DmeToleranceDlg import DmeToleranceDlg
from FlightPlanner.RnavDmeUpdateArea.RnavDmeUpdateAreaDlg import RnavDmeUpdateAreaDlg
from FlightPlanner.Holding.HoldingRnav.HoldingRnavDlg import HoldingRnavDlg
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import SurfaceTypes
from FlightPlanner.AddObstacleLayerDlg import AddObstacleLayerDlg
from FlightPlanner.AddMeasureToolDlg import AddMeasureToolDlg
from FlightPlanner.AddMeasureAngleDlg import AddMeasureAngleToolDlg
from FlightPlanner.QgisHelper import QgisHelper
from map.AnnotaionTool.QgsMapToolTextAnnotation import QgsMapToolTextAnnotation
from map.QgsAppLayerTreeViewMenuProvider import QgsAppLayerTreeViewMenuProvider
from map.tools import SelectByRect, QgsMapToolSelectFreehand, QgsMapToolSelectPolygon, QgsMapToolSelectRadius
from FlightPlanner.Holding.RnavVorDme.RnavVorDmeDlg import RnavVorDme
from FlightPlanner.Holding.RnavDmeDme.RnavDmeDmeDlg import RnavDmeDme
from FlightPlanner.VisualCircling.VisualCirclingDlg import VisualCirclingDlg
from FlightPlanner.MSA.MSADlg import MSADlg
from FlightPlanner.DataImport.DataImportDlg import DataImportDlg
from FlightPlanner.Holding.HoldingOverHead.HoldingOverHeadDlg import HoldingOverHeadDlg
from FlightPlanner.Holding.HoldingVorDme.HoldingVorDmeDlg import HoldingVorDmeDlg
from FlightPlanner.Holding.HoldingRace_P.HoldingRace_PDlg import HoldingRace_PDlg
from FlightPlanner.Enroute.EnrouteStraight.EnrouteStraightDlg import EnrouteStraightDlg
from FlightPlanner.Enroute.EnrouteTurnOverHead.EnrouteTurnOverHeadDlg import EnrouteTurnOverHeadDlg
from FlightPlanner.RnavStraightSegmentAnalyser.RnavStraightSegmentAnalyserDlg import RnavStraightSegmentAnalyserDlg
from FlightPlanner.RnavTurningSegmentAnalyser.RnavTurningSegmentAnalyserDlg import RnavTurningSegmentAnalyserDlg
from FlightPlanner.TurnProtectionAndObstacleAssessment.TurnProtectionAndObstacleAssessmentDlg import TurnProtectionAndObstacleAssessmentDlg
from FlightPlanner.Radial.RadialDlg import RadialDlg
from FlightPlanner.Ils.IlsBasic.IlsBasicDlg import IlsBasicDlg
from FlightPlanner.IasToTas.IasToTas import IasToTasDlg
from FlightPlanner.GeometryCreate.LineCreate import LineCreateTool
from FlightPlanner.TurnArea.TurnAreaDlg import TurnAreaDlg
from FlightPlanner.FixToleranceArea.FixToleranceAreaDlg import FixToleranceAreaDlg
from FlightPlanner.ObstacleEvaluator.ObstacleEvaluator import ObstacleEvaluatorDlg
from FlightPlanner.RnavNominal.RnavNominalDlg import RnavNominalDlg
from FlightPlanner.GeoDetermine.GeoDetermineDlg import GeoDetermineDlg
from FlightPlanner.PathTerminators.PathTerminatorsDlg import PathTerminatorsDlg
from FlightPlanner.FasDataBlock.FasDataBlockDlg import FasDataBlockDlg
from FlightPlanner.ProcedureExport.ProcedureExportDlg import ProcedureExportDlg
from FlightPlanner.ProfileManager.ProfileManagerDlg import ProfileManagerDlg
from FlightPlanner.DataExport.DataExportDlg import DataExportDlg
from FlightPlanner.ApproachSegment.ApproachSegmentDlg import ApproachSegmentDlg
from FlightPlanner.MASegment.MASegmentDlg import MASegmentDlg
from FlightPlanner.RaceTrackAndHolding.RaceTrackDlg import RaceTrackDlg
from FlightPlanner.ChartingGrid.ChartingGridDlg import ChartingGridDlg
from FlightPlanner.ChartingTemplates.ChartingTemplatesDlg import ChartingTemplatesDlg
from FlightPlanner.PaIls.PaIlsDlg import PaIlsDlg
from FlightPlanner.HeliportSurfaces.HeliportSurfacesDlg import HeliportSurfacesDlg
from Composer.ComposerDlg import ComposerDlg

from FlightPlanner.NpaOnFix.NpaOnFixDlg import NpaOnFixDlg
from FlightPlanner.NpaAtDistanceTime.NpaAtDistanceTimeDlg import NpaAtDistanceTimeDlg

from ProjectManager.LoginForm import LoginForm
from ProjectManager.UserMngForm import UserMngForm
from ProjectManager.RegProjectFolderForm import RegProjectFolderForm
from AircraftOperation import AirCraftOperation
from ProjectManager.ProjectMngForm import ProjectMngForm
from ProjectManager.SubProjectMngForm import SubProjectMngForm
from ProjectManager.WorkspaceMngForm import WorkspaceMngForm
from ProjectManager.ProcedureMngForm import ProcedureMngForm
from ProjectManager.MYUSERINFO import enumUserRight
from ProjectManager.AIPChartMngForm import AIPChartMngForm
from ProjectManager.SelectProcedureForm import SelectProcedureForm

from Type.switch import switch

from FlightPlanner.Dialogs.DlgCrcReadWrite import DlgCrcReadWrite
from Charting.DlgChartingStart import DlgChartingStart
print "Dlg import End"
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Dialogs.DlgCrcCheck import DlgCrcCheck
from Type.String import String
print "DlgLicensing import Before"
from Licensing.DlgLicensing import DlgLicensing
print "OpenlayersPlugin import Before"
from openlayers.openlayers_plugin import OpenlayersPlugin
print "GridZoneGenerator import Before"
from GridZoneGenerator.grid_zone_generator import GridZoneGenerator
from QAD.qad import Qad
from QaWindow.QaWindow import QaWindow

import define
import sys
print "clr import Before"
try:
    import clr
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except:
    print "Unexpected error:", sys.exc_info()[0]
print "SKGL import Before"

try:
    mydll = clr.AddReference('SKGL')
    from SKGL import Validate, Generate
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except:
    print "Unexpected error:", sys.exc_info()[0]
print "MyWnd Import End"


class MyWnd(QMainWindow):
    def __init__(self):
        self.currentDir = os.getcwdu()
        self.rasterLayerList = []
        print self.currentDir
        QMainWindow.__init__(self)
        self.addCircularType = "Point"
        self.circularTool = None
        self.nodeTool = None

        define._mapCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        define._xyCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        define._latLonCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)

        define._messagBar = QgsMessageBar()
        define._messagBar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.canvas = QgsMapCanvas(self)

        define._canvas = self.canvas
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.layersChanged.connect(self.setSnapping)
        meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)

        define._qgsDistanceArea = QgsDistanceArea()
        
        self.canvas.setExtent(QgsRectangle(-180, -90, 180, 90))

        print "Init menu"
        self.initMenus()
        self.setMapUnitsMeter()
        self.initStatusBar()

        self.canvas.scaleChanged.connect(self.showScale)
        define._obstacleLayers = []
        define._surfaceLayers = []

        self.dockWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(define._messagBar)

        self.tabBar = QTabBar(self)
        self.tabBar.addTab("X, Y")
        self.tabBar.addTab("Lat, Lon")
        icon = QIcon("Resource/btnImage/close.png")

        layout.addWidget(self.tabBar)

        self.w1 = QFrame(self)
        self.l = QVBoxLayout()
        self.l.setMargin(0)
        self.l.setSpacing(0)
        self.l.addWidget(define._canvas)
        self.w1.setLayout(self.l)
        layout.addWidget(self.w1)
        self.tabBar.currentChanged.connect(self.tabCtrlGeneral_CurrentChanged)

        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.dockWidget.setLayout(layout)
        self.dockWidget.setContentsMargins(0,0,0,0)        
        self.setCentralWidget(self.dockWidget)

        self.toolbarDigitizingToolsActionActions = []

        self.initLayerTreeView() 
        self.createOverview()
        self.createBaseToolbar()
        self.createFlightPlannerToolbar()

        self.tabCtrlGeneral_CurrentChanged()
        print "Before plugin"
        self.addPlugInsMenu()
        self.addChartingMenu()
        self.addAboutMenu()

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/dlgIcon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        self.setWindowTitle("FlightPlanner")

        self.procedureMenuUserManagementAction.setEnabled(False)
        self.createProcedureToolStripMenuItem.setEnabled(False)

        self.readUserAndProject()

    def readUserAndProject(self):
        AirCraftOperation.ApplicationSetting.ReadSettings()

        AirCraftOperation.userList.SetUserInfoPath(AirCraftOperation.ApplicationSetting.ProjectFolderPath)
        flag = AirCraftOperation.userList.ReadUserInfoFile()

        AirCraftOperation.g_projectList.SetProjectInfoPath(AirCraftOperation.ApplicationSetting.ProjectFolderPath)
        flag = AirCraftOperation.g_projectList.ReadProjectInfoXml()

    def addPlugInsMenu(self):
        menuBar = self.menuBar()
        self.pluginsMenu = menuBar.addMenu("&Plugins")
        self.openLayer = OpenlayersPlugin(self, self.pluginsMenu)
        self.gridZoneGenerator = GridZoneGenerator(self, self.pluginsMenu)
        self.qad = Qad(self)
        self.qad.initGui()

    def pluginMenu(self):
        return self.pluginsMenu

    def addChartingMenu(self):
        menuBar = self.menuBar()
        chartingMenu = menuBar.addMenu("&Charting")
        chartingIACMnu = chartingMenu.addMenu("IAC")
        chartingMenu.aboutToShow.connect(self.chartingMenu_aboutToShow)

        chartingIACNewMnuAction = QgisHelper.createAction(chartingIACMnu, "New...", self.chartingIACNewMnuActionEvent, None, None, None, False)
        chartingIACOpenwMnuAction = QgisHelper.createAction(chartingIACMnu, "Open...", self.chartingIACOpenMnuActionEvent, None, None, None, False)
        chartingIACMnu.addAction(chartingIACNewMnuAction)
        chartingIACMnu.addAction(chartingIACOpenwMnuAction)

    def chartingMenu_aboutToShow(self):
        pass

    def chartingIACOpenMnuActionEvent(self):
        compDlg = ComposerDlg(self, None, None, None, False)
        compDlg.show()

    def chartingIACNewMnuActionEvent(self):
        dlg = DlgChartingStart(self)
        dlg.show()

    def chartingIACMnuActionEvent(self):
        pass

    def chartingLOCMnuActionEvent(self):
        pass

    def addAboutMenu(self):
        menuBar = self.menuBar()
        aboutMenu = menuBar.addMenu("&About")
        licensingMnuAction = QgisHelper.createAction(self, "Licensing", self.licensingMnuActionEvent, None, None, None, False)
        aboutMenu.addAction(licensingMnuAction)

    def licensingMnuActionEvent(self):
        import _winreg as wr
        licenseKey = None
        aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        aKey = None
        try:
            targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
            print "*** Reading from", targ, "***"
            aKey = wr.OpenKey(aReg, targ)
            try:
                n, v, t = wr.EnumValue(aKey, 0)
                if n == "License":
                    licenseKey = v
            except:
                pass
            finally:
                try:
                    wr.CloseKey(aKey)
                except:
                    pass
        except:
            pass
        finally:
            try:
                wr.CloseKey(aReg)
            except:
                pass

            licenceFlag = False
            dlgLicensing = DlgLicensing()

            if licenseKey is not None:
                objValidate = Validate()
                objValidate.secretPhase = "aerodrome$pw3s$Pa$$W0rd"
                objValidate.Key = String.QString2Str(QString(licenseKey)).replace("-", "")

                try:
                    if (objValidate.IsValid and objValidate.IsOnRightMachine and objValidate.IsExpired == False and objValidate.SetTime >= objValidate.DaysLeft):
                        licenceFlag = True
                        dlgLicensing.labelCreatedDate.setText("Created On : " + objValidate.CreationDate.ToString())
                        dlgLicensing.labelRemainingDays.setText("Days left : " + str(objValidate.DaysLeft))
                except:
                    pass

            if not licenceFlag:
                dlgLicensing.frame.setVisible(True)
                dlgLicensing.frame_2.setVisible(False)
            else:
                dlgLicensing.frame.setVisible(False)
                dlgLicensing.frame_2.setVisible(True)

            licenceFlag = dlgLicensing.exec_()

    def tabCtrlGeneral_CurrentChanged(self):
        if self.tabBar.currentIndex() == 1:
            self.setProjectOfCanvas(define._canvas, define._latLonCrs)
            define._crsLabel.setText(define._latLonCrs.authid())
            define._mapCrs = define._latLonCrs
        else:
            self.setProjectOfCanvas(define._canvas, define._xyCrs)
            define._crsLabel.setText(define._xyCrs.authid())
            define._mapCrs = define._xyCrs

    def convertCrsPositionPanel(self, dlgList, inputCrs, outPutCrs):
        if len(dlgList) == 0:
            return

        for dlg in dlgList:
            lstPositionPanel = dlg.findChildren(PositionPanel)
            if len(lstPositionPanel) != 0:
                for positionPanel in lstPositionPanel:
                    point3d0 = positionPanel.Point3d
                    point3d = QgisHelper.CrsTransformPoint(point3d0.get_X(), point3d0.get_Y(), inputCrs, outPutCrs, point3d0.get_Z())
                    positionPanel.Point3d = point3d

    def initStatusBar(self):
        spaceLabel = QLabel(self.statusBar())
        spaceLabel.setObjectName("spaceLabel")
        myFont = QFont("Arial", 9)
        spaceLabel.setFont(myFont)
        spaceLabel.setMinimumWidth(10)
        spaceLabel.setMaximumHeight(25)
        spaceLabel.setMargin(3)
        spaceLabel.setAlignment(Qt.AlignCenter)
        spaceLabel.setFrameStyle(QFrame.NoFrame)
        spaceLabel.setText("                                       ")
        self.statusBar().addPermanentWidget(spaceLabel, 0)

        crsLabel = QLabel(self.statusBar())
        crsLabel.setObjectName("messageLabel")
        myFont = QFont("Arial", 9)
        crsLabel.setFont(myFont)
        crsLabel.setMinimumWidth(10)
        crsLabel.setMaximumHeight(25)
        crsLabel.setMargin(3)
        crsLabel.setAlignment(Qt.AlignCenter)
        crsLabel.setFrameStyle(QFrame.NoFrame)
        crsLabel.setText("")
        crsLabel.setToolTip("Message")
        self.statusBar().addPermanentWidget(crsLabel, 0)
        define._crsLabel = crsLabel

        messageLabel = QLabel(self.statusBar())
        messageLabel.setObjectName("messageLabel")
        myFont = QFont("Arial", 9)
        messageLabel.setFont(myFont)
        messageLabel.setMinimumWidth(10)
        messageLabel.setMaximumHeight(25)
        messageLabel.setMargin(3)
        messageLabel.setAlignment(Qt.AlignCenter)
        messageLabel.setFrameStyle(QFrame.NoFrame)
        messageLabel.setText("")
        messageLabel.setToolTip("Message")
        self.statusBar().addPermanentWidget(messageLabel, 0)
        define._messageLabel = messageLabel
        
        mScaleLabel = QLabel(self.statusBar())
        mScaleLabel.setObjectName("mScaleLable")
        myFont = QFont("Arial", 9)
        mScaleLabel.setFont(myFont)
        mScaleLabel.setMinimumWidth(10)
        mScaleLabel.setMaximumHeight(25)
        mScaleLabel.setMargin(3)
        mScaleLabel.setAlignment(Qt.AlignCenter)
        mScaleLabel.setFrameStyle(QFrame.NoFrame)
        mScaleLabel.setText("Scale ")
        mScaleLabel.setToolTip("Current map scale")
        self.statusBar().addPermanentWidget(mScaleLabel, 0)
    
        self.mScaleEdit = QgsScaleComboBox(self.statusBar())
        self.mScaleEdit.setObjectName("self.mScaleEdit")
        self.mScaleEdit.setFont(myFont)
        self.mScaleEdit.lineEdit().setFont(myFont)
        self.mScaleEdit.setMinimumWidth(30)
        self.mScaleEdit.setMaximumWidth(200)
        self.mScaleEdit.setMaximumHeight(25)
        self.mScaleEdit.setContentsMargins(0, 0, 0, 0)
        self.mScaleEdit.setWhatsThis("Displays the current map scale")
        self.mScaleEdit.setToolTip("Current map scale (formatted as x:y)")
    
        self.statusBar().addPermanentWidget(self.mScaleEdit, 0)
        self.mScaleEdit.scaleChanged.connect(self.userScale)

    def createBaseToolbar(self):           
        actionZoomIn = QAction(self)
        actionZoomIn.setObjectName("ZoomIn")
        icon = QIcon("Resource\\mActionZoomIn.png")
        actionZoomIn.setIcon(icon)
        actionZoomIn.setToolTip("Zoom In")

        actionZoomOut = QAction(self)
        actionZoomOut.setObjectName("ZoomOut")
        icon1 = QIcon(self.currentDir + "/Resource/mActionZoomOut.png")
        actionZoomOut.setIcon(icon1)
        actionZoomOut.setToolTip("Zoom Out")

        self.actionPan = QAction(self)
        self.actionPan.setObjectName("mpActionPan")
        icon2 = QIcon(self.currentDir + "/Resource/mActionPan.png")
        self.actionPan.setIcon(icon2)
        self.actionPan.setToolTip("Pan Map")

        fullExtent = QAction(self)
        icon5 = QIcon(self.currentDir + "/Resource/mActionZoomFullExtent.png")
        fullExtent.setIcon(icon5)
        fullExtent.setToolTip("Zoom Full")

        '''select feature Tool'''
        selectByPolygon = QAction(self)
        icon5 = QIcon(self.currentDir + "/Resource/mActionSelectPolygon.png")
        selectByPolygon.setIcon(icon5)
        selectByPolygon.setToolTip("Select Features by Polygon")
        selectByPolygon.setText("Select by Polygon")

        selectByRect = QAction(self)
        icon5 = QIcon(self.currentDir + "/Resource/mActionSelectRectangle.png")
        selectByRect.setIcon(icon5)
        selectByRect.setToolTip("Select Features by Rectangle")
        selectByRect.setText("Select by Rectangle")

        selectByFreehand = QAction(self)
        icon5 = QIcon(self.currentDir + "/Resource/mActionSelectFreehand.png")
        selectByFreehand.setIcon(icon5)
        selectByFreehand.setToolTip("Select Features by Freehand")
        selectByFreehand.setText("Select by Freehand")

        selectByRadius = QAction(self)
        icon5 = QIcon(self.currentDir + "/Resource/mActionSelectRadius.png")
        selectByRadius.setIcon(icon5)
        selectByRadius.setToolTip("Select Features by Radius")
        selectByRadius.setText("Select by Radius")

        settings = QSettings()
        self.btnSelect = QToolButton()
        self.btnSelect.setPopupMode(QToolButton.MenuButtonPopup)
        self.btnSelect.addAction(selectByRect)
        self.btnSelect.addAction(selectByPolygon)
        self.btnSelect.addAction(selectByFreehand)
        self.btnSelect.addAction(selectByRadius)

        defMeasureAction = selectByRect
        index = settings.value("/UI/selectionFeatureTool", 0).toInt()

        if index == 0:
            defMeasureAction = selectByRect
        elif index == 1:
            defMeasureAction = selectByPolygon
        elif index == 2:
            defMeasureAction = selectByFreehand
        elif index == 3:
            defMeasureAction = selectByRadius
        self.btnSelect.setDefaultAction(defMeasureAction)

        self.actionDeselect = QAction(self)
        self.actionDeselect.setObjectName("mpDeselect")
        icon2 = QIcon(self.currentDir + "/Resource/images/themes/default/mActionUnselectAttributes.png")
        self.actionDeselect.setIcon(icon2)
        self.actionDeselect.setToolTip("Deselect features")

        self.actionAddLine = QAction(self)
        self.actionAddLine.setObjectName("mpAddLine")
        icon2 = QIcon(self.currentDir + "/Resource/lineAdd.png")
        self.actionAddLine.setIcon(icon2)
        self.actionAddLine.setToolTip("Add Line")

        actionExpressionselect = QAction(self)
        actionExpressionselect.setObjectName("mpExpressionselect")
        icon2 = QIcon(self.currentDir + "/Resource/mIconExpressionSelect.png")
        actionExpressionselect.setIcon(icon2)
        actionExpressionselect.setToolTip("Select features using an expression")

        self.measureAction = QAction(self)
        icon6 = QIcon(self.currentDir + "/Resource/measure-length.png")
        self.measureAction.setIcon(icon6)
        self.measureAction.setText("Measure Line")

        self.mActionMeasureAngle = QAction(self)
        icon7 = QIcon(self.currentDir + "/Resource/mActionMeasureAngle.png")
        self.mActionMeasureAngle.setIcon(icon7)
        self.mActionMeasureAngle.setText("Measure Angle")

        settings = QSettings()
        self.btnMeasure = QToolButton()
        self.btnMeasure.setPopupMode(QToolButton.MenuButtonPopup)
        self.btnMeasure.addAction(self.measureAction)
        self.btnMeasure.addAction(self.mActionMeasureAngle)
        defMeasureAction = self.measureAction
        index = settings.value("/UI/measureTool", 0).toInt()

        if index == 0:
            defMeasureAction = self.measureAction
        elif index == 1:
            defMeasureAction = self.mActionMeasureAngle
        self.btnMeasure.setDefaultAction(defMeasureAction)

        self.mpActionAddVectorData = QAction(self)
        icon7 = QIcon(self.currentDir + "/Resource/mActionAddOgrLayer.png")
        self.mpActionAddVectorData.setIcon(icon7)
        self.mpActionAddVectorData.setToolTip("Add Vector Data")

        openProjAction = QAction(self)
        icon8 = QIcon("Resource\\folder.png")
        openProjAction.setIcon(icon8)
        openProjAction.setToolTip("Open")

        saveProjAction = QAction(self)
        icon9 = QIcon("Resource\\filesave.png")
        saveProjAction.setIcon(icon9)
        saveProjAction.setToolTip("Save")

        txtAnnotationAction = QAction(self)
        icon9 = QIcon("Resource\\mActionTextAnnotation.png")
        txtAnnotationAction.setIcon(icon9)
        txtAnnotationAction.setToolTip("Text Annotation")

        geoDetermine = QAction(self)
        geoDetermine.setObjectName("mpGeoDetermine")
        icon5 = QIcon(self.currentDir + "/Resource/GeoDeterminePosition.bmp")
        geoDetermine.setIcon(icon5)
        geoDetermine.setToolTip(SurfaceTypes.GeoDetermine)

        actionOpenObstacleCheckFile = QAction(self)
        actionOpenObstacleCheckFile.setObjectName("mpActionOpenObstacleCheckFile")
        icon11 = QIcon(self.currentDir + "/Resource/openObstacleCheckFile.png")
        actionOpenObstacleCheckFile.setIcon(icon11)
        actionOpenObstacleCheckFile.setToolTip("Open Obstacle Check xml File")

        self.connect(openProjAction, SIGNAL("triggered()"), self.openProj)
        self.connect(saveProjAction, SIGNAL("triggered()"), self.saveProj)
        self.connect(self.measureAction, SIGNAL("triggered()"), self.measureTool)
        self.connect(self.mActionMeasureAngle, SIGNAL("triggered()"), self.measureAngleTool)
        self.connect(actionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        self.connect(actionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        self.connect(self.actionPan, SIGNAL("triggered()"), self.pan)
        self.connect(fullExtent, SIGNAL("triggered()"), self.fullExtent)
        self.connect(self.mpActionAddVectorData, SIGNAL("triggered()"), self.AddVectorLayer)
        self.connect(txtAnnotationAction, SIGNAL("triggered()"), self.txtAnnotationTool)
        self.connect(self.actionDeselect, SIGNAL("triggered()"), self.deselectAll)
        self.connect(self.actionAddLine, SIGNAL("triggered()"), self.addLine)
        self.connect(actionExpressionselect, SIGNAL("triggered()"), self.expressionselect)
        self.connect(geoDetermine, SIGNAL("triggered()"), self.geoDetermineDlgShow)
        self.connect(actionOpenObstacleCheckFile, SIGNAL("triggered()"), self.openObstacleCheckFile)

        selectByRect.triggered.connect(self.setSelectByRectTool)
        selectByPolygon.triggered.connect(self.setSelectByPolygonTool)
        selectByFreehand.triggered.connect(self.setSelectByFreehandTool)
        selectByRadius.triggered.connect(self.setSelectByRadiusTool)
        self.toolbarBaseAction = self.addToolBar("Base actions")

        self.toolbarBaseAction.addAction(openProjAction)
        self.toolbarBaseAction.addAction(saveProjAction)
        self.toolbarBaseAction.addAction(actionZoomIn)
        self.toolbarBaseAction.addAction(actionZoomOut)
        self.toolbarBaseAction.addAction(self.actionPan)
        self.toolbarBaseAction.addAction(fullExtent)
        self.toolbarBaseAction.addAction(self.actionAddLine)
        self.toolbarBaseAction.addAction(txtAnnotationAction)
        selectAct = self.toolbarBaseAction.addWidget(self.btnSelect)
        selectAct.setObjectName("ActionMeasure")
        self.toolbarBaseAction.addAction(self.actionDeselect)
        self.toolbarBaseAction.addAction(actionExpressionselect)
        self.toolbarBaseAction.addAction(geoDetermine)
        self.toolbarBaseAction.addAction(actionOpenObstacleCheckFile)

        self.btnSelect.triggered.connect(self.selectToolButtonActionTriggered)
        measureAct = self.toolbarBaseAction.addWidget(self.btnMeasure)
        measureAct.setObjectName("ActionMeasure")
        self.btnMeasure.triggered.connect(self.toolButtonActionTriggered)

        # create the map tools
        self.toolPan = QgsMapToolPan(define._canvas)
        self.toolPan.setAction(self.actionPan)
        self.toolZoomIn = QgsMapToolZoom(define._canvas, False) # False = in
        self.toolZoomIn.setAction(actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(define._canvas, True) # True = out
        self.toolZoomOut.setAction(actionZoomOut)
        self.toolSelectByRect = SelectByRect(define._canvas)
        self.toolSelectByRect.setAction(selectByRect)
        self.toolSelectByPolygon = QgsMapToolSelectPolygon(define._canvas)
        self.toolSelectByPolygon.setAction(selectByPolygon)
        self.toolSelectByFreehand = QgsMapToolSelectFreehand(define._canvas)
        self.toolSelectByFreehand.setAction(selectByFreehand)
        self.toolSelectByRadius = QgsMapToolSelectRadius(define._canvas)
        self.toolSelectByRadius.setAction(selectByRadius)
        self.pan()

        # legend Tool
        self.mActionRemoveLayer = QAction(self)
        self.mActionRemoveLayer.setIcon(QgsApplication.getThemeIcon("/mActionRemoveLayer.svg"))
        self.connect(self.mActionRemoveLayer, SIGNAL("triggered()"), self.removeLayer)

        self.setMouseTracking(True)
        self.canvas.xyCoordinates.connect(self.mouseMoveHandler)
        self._mLayerTreeView.currentLayerChanged.connect(self.layersChanged)
        self.saveFlag = True
        self.dlgRnpAR = None

        '''edit tools'''
        self.mpActionSaveForSelectedLayers = QAction(self)
        self.mpActionSaveForSelectedLayers.setObjectName("mpSaveForSelectedLayers")
        self.mpActionSaveForSelectedLayers.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionSaveAllEdits.png"))
        self.mpActionSaveForSelectedLayers.setToolTip("Save for Selected Layer(s)")
        self.mpActionSaveForSelectedLayers.setText("Save for Selected Layer(s)")
        self.connect(self.mpActionSaveForSelectedLayers, SIGNAL("triggered()"), self.saveForSelectedLayersFunc)

        self.mpActionRollBackForSelectedLayers = QAction(self)
        self.mpActionRollBackForSelectedLayers.setObjectName("mpRollBackForSelectedLayers")
        self.mpActionRollBackForSelectedLayers.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionRollback.png"))
        self.mpActionRollBackForSelectedLayers.setToolTip("RollBack for Selected Layer(s)")
        self.mpActionRollBackForSelectedLayers.setText("RollBack for Selected Layer(s)")
        self.connect(self.mpActionRollBackForSelectedLayers, SIGNAL("triggered()"), self.rollBackForSelectedLayersFunc)

        self.mpActionCancelForSelectedLayers = QAction(self)
        self.mpActionCancelForSelectedLayers.setObjectName("mpCancelForSelectedLayers")
        self.mpActionCancelForSelectedLayers.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCancelEdits.png"))
        self.mpActionCancelForSelectedLayers.setToolTip("Cancel for Selected Layer(s)")
        self.mpActionCancelForSelectedLayers.setText("Cancel for Selected Layer(s)")
        self.connect(self.mpActionCancelForSelectedLayers, SIGNAL("triggered()"), self.cancelForSelectedLayersFunc)

        separator = QAction(self)
        separator.setSeparator(True)
        separator.setObjectName("separator")

        self.mpActionSaveForAllLayers = QAction(self)
        self.mpActionSaveForAllLayers.setObjectName("mpSaveForAllLayers")
        self.mpActionSaveForAllLayers.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionSaveAllEdits.png"))
        self.mpActionSaveForAllLayers.setToolTip("Save for All Layers")
        self.mpActionSaveForAllLayers.setText("Save for All Layers")
        self.connect(self.mpActionSaveForAllLayers, SIGNAL("triggered()"), self.saveForAllLayersFunc)

        self.mpActionRollBackForAllLayers = QAction(self)
        self.mpActionRollBackForAllLayers.setObjectName("mpRollBackForAllLayers")
        self.mpActionRollBackForAllLayers.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionRollback.png"))
        self.mpActionRollBackForAllLayers.setToolTip("RollBack for All Layers")
        self.mpActionRollBackForAllLayers.setText("RollBack for All Layers")
        self.connect(self.mpActionRollBackForAllLayers, SIGNAL("triggered()"), self.rollBackForAllLayersFunc)

        self.mpActionCancelForAllLayers = QAction(self)
        self.mpActionCancelForAllLayers.setObjectName("mpCancelForAllLayers")
        self.mpActionCancelForAllLayers.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCancelEdits.png"))
        self.mpActionCancelForAllLayers.setToolTip("Cancel for All Layers")
        self.mpActionCancelForAllLayers.setText("Cancel for All Layers")
        self.connect(self.mpActionCancelForAllLayers, SIGNAL("triggered()"), self.cancelForAllLayersFunc)

        self.btnCurrentEdits = QToolButton()
        self.btnCurrentEdits.setPopupMode(QToolButton.InstantPopup)
        mnu = QMenu()
        mnu.addAction(self.mpActionSaveForSelectedLayers)
        mnu.addAction(self.mpActionRollBackForSelectedLayers)
        mnu.addAction(self.mpActionCancelForSelectedLayers)
        mnu.addAction(separator)
        mnu.addAction(self.mpActionSaveForAllLayers)
        mnu.addAction(self.mpActionRollBackForAllLayers)
        mnu.addAction(self.mpActionCancelForAllLayers)
        self.btnCurrentEdits.setMenu(mnu)
        self.btnCurrentEdits.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCurrentEdits.png"))

        mnu.aboutToShow.connect(self.currentEditsToolButtonActionTriggered)

        self.toolbarBaseAction.addWidget(self.btnCurrentEdits)

        self.btnCurrentEdits.setEnabled(False)

        self.mpActionToggleEditing = QAction(self)
        self.mpActionToggleEditing.setObjectName("mpEditStart")
        self.mpActionToggleEditing.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionToggleEditing.png"))
        self.mpActionToggleEditing.setToolTip("Toggle Editing")
        self.mpActionToggleEditing.setCheckable(True)
        self.connect(self.mpActionToggleEditing, SIGNAL("triggered()"), self.toggleEditingFunc)
        self.toolbarBaseAction.addAction(self.mpActionToggleEditing)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionToggleEditing)

        self.mpActionEditSave = QAction(self)
        self.mpActionEditSave.setObjectName("mpEditSave")
        self.mpActionEditSave.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditSave.png"))
        self.mpActionEditSave.setToolTip("Save Layer Edits")
        self.mpActionEditSave.setCheckable(False)
        self.mpActionEditSave.setEnabled(False)
        self.connect(self.mpActionEditSave, SIGNAL("triggered()"), self.editSaveFunc)
        self.toolbarBaseAction.addAction(self.mpActionEditSave)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionEditSave)

        self.mpActionAddFeature = QAction(self)
        self.mpActionAddFeature.setObjectName("mpAddFeature")
        self.mpActionAddFeature.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCapturePoint.png"))
        self.mpActionAddFeature.setToolTip("Add Feature")
        self.mpActionAddFeature.setCheckable(True)
        self.mpActionAddFeature.setEnabled(False)
        self.connect(self.mpActionAddFeature, SIGNAL("triggered()"), self.addFeatureFunc)
        self.toolbarBaseAction.addAction(self.mpActionAddFeature)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionAddFeature)

        self.actionCircularStringPoint = QAction(self)
        self.actionCircularStringPoint.setObjectName("actionCircularStringPoint")
        self.actionCircularStringPoint.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCircularStringCurvePoint.png"))
        self.actionCircularStringPoint.setToolTip("Add Circular String Point")
        self.actionCircularStringPoint.setText("Add Circular String Curve Point")
        self.actionCircularStringPoint.setCheckable(False)
        self.actionCircularStringPoint.setEnabled(False)
        self.connect(self.actionCircularStringPoint, SIGNAL("triggered()"), self.addCircularStringPoint)
        self.toolbarDigitizingToolsActionActions.append(self.actionCircularStringPoint)

        self.actionCircularStringRadius = QAction(self)
        self.actionCircularStringRadius.setObjectName("actionCircularStringRadius")
        self.actionCircularStringRadius.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCircularStringRadius.png"))
        self.actionCircularStringRadius.setToolTip("Add Circular String Radius")
        self.actionCircularStringRadius.setText("Add Circular String Radius")
        self.actionCircularStringRadius.setCheckable(False)
        self.actionCircularStringRadius.setEnabled(False)
        self.connect(self.actionCircularStringRadius, SIGNAL("triggered()"), self.addCircularStringRadius)
        self.toolbarDigitizingToolsActionActions.append(self.actionCircularStringRadius)

        settings = QSettings()
        self.btnCircularString = QToolButton()
        self.btnCircularString.setPopupMode(QToolButton.MenuButtonPopup)
        self.btnCircularString.addAction(self.actionCircularStringPoint)
        self.btnCircularString.addAction(self.actionCircularStringRadius)

        defCircularStringAction = self.actionCircularStringPoint
        defCircularStringAction.setEnabled(False)
        index = settings.value("/UI/addCircularTool", 0).toInt()

        if index == 0:
            defCircularStringAction = self.actionCircularStringPoint
        elif index == 1:
            defCircularStringAction = self.actionCircularStringRadius

        self.btnCircularString.setDefaultAction(defCircularStringAction)
        self.btnCircularString.triggered.connect(self.circularStringToolButtonActionTriggered)
        circularToolButtonAction = self.toolbarBaseAction.addWidget(self.btnCircularString)
        circularToolButtonAction.setObjectName("CircularToolButton")
        circularToolButtonAction.setToolTip("Add Circular String")
        self.btnCircularString.setEnabled(False)

        self.mpActionMoveFeatures = QAction(self)
        self.mpActionMoveFeatures.setObjectName("mpMoveFeatures")
        self.mpActionMoveFeatures.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionMoveFeature.png"))
        self.mpActionMoveFeatures.setToolTip("Move Features")
        self.mpActionMoveFeatures.setCheckable(True)
        self.mpActionMoveFeatures.setEnabled(False)
        self.connect(self.mpActionMoveFeatures, SIGNAL("triggered()"), self.moveFeaturesFunc)
        self.toolbarBaseAction.addAction(self.mpActionMoveFeatures)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionMoveFeatures)

        self.mpActionNodeTool = QAction(self)
        self.mpActionNodeTool.setObjectName("mpNodeTool")
        self.mpActionNodeTool.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionNodeTool.png"))
        self.mpActionNodeTool.setToolTip("Node Tool")
        self.mpActionNodeTool.setCheckable(True)
        self.mpActionNodeTool.setEnabled(False)
        self.connect(self.mpActionNodeTool, SIGNAL("triggered()"), self.nodeToolFunc)
        self.toolbarBaseAction.addAction(self.mpActionNodeTool)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionNodeTool)

        self.mpActionDeleteSelected = QAction(self)
        self.mpActionDeleteSelected.setObjectName("mpDeleteSelected")
        self.mpActionDeleteSelected.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionDeleteSelected.png"))
        self.mpActionDeleteSelected.setToolTip("Delete Selected")
        self.mpActionDeleteSelected.setCheckable(True)
        self.mpActionDeleteSelected.setEnabled(False)
        self.connect(self.mpActionDeleteSelected, SIGNAL("triggered()"), self.deleteSelectedFunc)
        self.toolbarBaseAction.addAction(self.mpActionDeleteSelected)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionDeleteSelected)

        self.mpActionEditCut = QAction(self)
        self.mpActionEditCut.setObjectName("mpEditCut")
        self.mpActionEditCut.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditCut.png"))
        self.mpActionEditCut.setToolTip("Cut Features")
        self.mpActionEditCut.setCheckable(True)
        self.mpActionEditCut.setEnabled(False)
        self.connect(self.mpActionEditCut, SIGNAL("triggered()"), self.editCutFunc)
        self.toolbarBaseAction.addAction(self.mpActionEditCut)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionEditCut)

        self.mpActionEditCopy = QAction(self)
        self.mpActionEditCopy.setObjectName("mpEditCopy")
        self.mpActionEditCopy.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditCopy.png"))
        self.mpActionEditCopy.setToolTip("Copy Features")
        self.mpActionEditCopy.setCheckable(True)
        self.mpActionEditCopy.setEnabled(False)
        self.connect(self.mpActionEditCopy, SIGNAL("triggered()"), self.editCopyFunc)
        self.toolbarBaseAction.addAction(self.mpActionEditCopy)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionEditCopy)

        self.mpActionEditPaste = QAction(self)
        self.mpActionEditPaste.setObjectName("mpEditPaste")
        self.mpActionEditPaste.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditPaste.png"))
        self.mpActionEditPaste.setToolTip("Paste Features")
        self.mpActionEditPaste.setCheckable(False)
        self.mpActionEditPaste.setEnabled(False)
        self.connect(self.mpActionEditPaste, SIGNAL("triggered()"), self.editPasteFunc)
        self.toolbarBaseAction.addAction(self.mpActionEditPaste)
        self.toolbarDigitizingToolsActionActions.append(self.mpActionEditPaste)

        self.addToolBarBreak()

    def cancelForSelectedLayersFunc(self):
        layerList = self._mLayerTreeView.selectedLayers()

        if len(layerList) <= 0:
            return

        if QMessageBox.information(self, "Current edits", "Cancel current changes for all layer(s)?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        else:
            for layer in layerList:
                if layer.isEditable():
                    layer.rollBack()
            self.mpActionToggleEditing.setChecked(False)
            self.toggleEditingFunc()

    def rollBackForSelectedLayersFunc(self):
        layerList = self._mLayerTreeView.selectedLayers()

        if len(layerList) <= 0:
            return

        if QMessageBox.information(self, "Current edits", "Rollback current changes for all layer(s)?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        else:
            for layer in layerList:
                if layer.isEditable():
                    layer.rollBack()
                    layer.startEditing()

    def saveForSelectedLayersFunc(self):
        layerList = self._mLayerTreeView.selectedLayers()

        if len(layerList) <= 0:
            return

        if QMessageBox.information(self, "Current edits", "Save current changes for all layer(s)?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        else:
            for layer in layerList:
                if layer.isEditable():
                    layer.commitChanges()
                    layer.startEditing()

    def cancelForAllLayersFunc(self):
        layerList = self.canvas.layers()

        if len(layerList) <= 0:
            return

        if QMessageBox.information(self, "Current edits", "Cancel current changes for all layer(s)?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        else:
            for layer in layerList:
                if layer.isEditable():
                    layer.rollBack()
            self.mpActionToggleEditing.setChecked(False)
            self.toggleEditingFunc()

    def rollBackForAllLayersFunc(self):
        layerList = self.canvas.layers()

        if len(layerList) <= 0:
            return

        if QMessageBox.information(self, "Current edits", "Rollback current changes for all layer(s)?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        else:
            for layer in layerList:
                if layer.isEditable():
                    layer.rollBack()
                    layer.startEditing()

    def saveForAllLayersFunc(self):
        layerList = self.canvas.layers()

        if len(layerList) <= 0:
            return

        if QMessageBox.information(self, "Current edits", "Save current changes for all layer(s)?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        else:
            for layer in layerList:
                if layer.isEditable():
                    layer.commitChanges()
                    layer.startEditing()

    def currentEditsToolButtonActionTriggered(self):
        layerList = self.canvas.layers()

        if len(layerList) <= 0:
            return

        modifiedFlag = False

        for layer in layerList:
            if layer.isModified():
                modifiedFlag = True
                break

        if modifiedFlag:
            self.mpActionSaveForAllLayers.setEnabled(True)
            self.mpActionSaveForSelectedLayers.setEnabled(True)
            self.mpActionRollBackForSelectedLayers.setEnabled(True)
            self.mpActionRollBackForAllLayers.setEnabled(True)
        else:
            self.mpActionSaveForAllLayers.setEnabled(False)
            self.mpActionSaveForSelectedLayers.setEnabled(False)
            self.mpActionRollBackForSelectedLayers.setEnabled(False)
            self.mpActionRollBackForAllLayers.setEnabled(False)

    def addCircularString(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        if self.mpActionAddCircularString.isChecked():
            self.currentDigitizingLayer = self.canvas.currentLayer()

            if not self.currentDigitizingLayer.isEditable():
                childActions = self.toolbarDigitizingToolsActionActions
                if len(childActions) != 0:
                    for action in childActions:
                        if action.objectName() != "mpEditStart":
                            action.setChecked(False)
                return

            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setChecked(False)

            self.circularTool = QgsMapToolAddCircularString(self.currentDigitizingLayer, self.addCircularType)
            self.canvas.setMapTool(self.circularTool)
        else:
            self.canvas.setMapTool(QgsMapToolPan(define._canvas))

    def addCircularStringPoint(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.currentDigitizingLayer = self.canvas.currentLayer()

        if not self.currentDigitizingLayer.isEditable():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setChecked(False)
            return

        childActions = self.toolbarDigitizingToolsActionActions

        if len(childActions) != 0:
            for action in childActions:
                if action.objectName() != "mpEditStart":
                    action.setChecked(False)
        self.circularTool = QgsMapToolAddCircularString(self.currentDigitizingLayer, "Point")
        self.canvas.setMapTool(self.circularTool)

    def addCircularStringRadius(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.currentDigitizingLayer = self.canvas.currentLayer()

        if not self.currentDigitizingLayer.isEditable():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setChecked(False)
            return

        childActions = self.toolbarDigitizingToolsActionActions
        if len(childActions) != 0:
            for action in childActions:
                if action.objectName() != "mpEditStart" and action.objectName() != "mpAddCircularString":
                    action.setChecked(False)

        self.circularTool = QgsMapToolAddCircularString(self.currentDigitizingLayer, "Radius")
        self.canvas.setMapTool(self.circularTool)

    def editSaveFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.mpActionEditSave.setEnabled(True)

        layer = self.canvas.currentLayer()

        if not layer.isEditable():
            return

        layer.commitChanges()
        layer.startEditing()

    def deleteSelectedFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        if self.mpActionDeleteSelected.isChecked():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart" and action.objectName() != "mpDeleteSelected":
                        action.setChecked(False)

            toolSelectByRect0 = SelectByRect(define._canvas)
            self.canvas.setMapTool(toolSelectByRect0)
            self.connect(toolSelectByRect0, SIGNAL("getSelectedFeatures"), self.deleteSelecetedFeatures)
        else:
            self.canvas.setMapTool(QgsMapToolPan(define._canvas))

    def deleteSelecetedFeatures(self, selectedFeatures):
        if selectedFeatures is None or len(selectedFeatures) == 0:
            return

        layer =self.canvas.currentLayer()

        if not layer.isEditable():
            return

        layer.deleteSelectedFeatures()

    def addFeatureFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.currentDigitizingLayer = self.canvas.currentLayer()
        childActions = self.toolbarDigitizingToolsActionActions

        if len(childActions) != 0:
            for action in childActions:
                if action.objectName() != "mpEditStart" and action.objectName() != "mpAddFeature":
                    action.setChecked(False)

        addTool = QgsMapToolAddFeature(self.currentDigitizingLayer)
        self.canvas.setMapTool(addTool)

    def moveFeaturesFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.currentDigitizingLayer = self.canvas.currentLayer()

        if not self.currentDigitizingLayer.isEditable():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setChecked(False)
            return

        childActions = self.toolbarDigitizingToolsActionActions

        if len(childActions) != 0:
            for action in childActions:
                if action.objectName() != "mpEditStart" and action.objectName() != "mpMoveFeature":
                    action.setChecked(False)

        moveTool = QgsMapToolMoveFeature(self.currentDigitizingLayer)
        self.canvas.setMapTool(moveTool)

    def nodeToolFunc(self):
        self.mpActionAddFeature.setChecked(False)
        self.mpActionMoveFeatures.setChecked(False)
        self.mpActionNodeTool.setChecked(True)

        childActions = self.toolbarDigitizingToolsActionActions
        if len(childActions) != 0:
            for action in childActions:
                if action.objectName() != "mpEditStart" and action.objectName() != "mpNodeTool":
                    action.setChecked(False)

        self.currentDigitizingLayer = self.canvas.currentLayer()

        if not self.currentDigitizingLayer.isEditable():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setChecked(False)
            return

        self.nodeTool = QgsMapToolNodeTool(define._canvas.currentLayer())
        self.canvas.setMapTool(self.nodeTool)

    def editCutFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.mpActionEditCut.setEnabled(True)
        self.mpActionDeleteSelected.setChecked(False)

        if self.mpActionEditCut.isChecked():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart" and action.objectName() != "mpEditCut":
                        action.setChecked(False)

            toolSelectByRect0 = SelectByRect(define._canvas)
            self.canvas.setMapTool(toolSelectByRect0)
            self.connect(toolSelectByRect0, SIGNAL("getSelectedFeatures"), self.cutSelecetedFeatures)
        else:
            self.canvas.setMapTool(QgsMapToolPan(define._canvas))

    def cutSelecetedFeatures(self, selectedFeatures):
        if selectedFeatures is None or len(selectedFeatures) == 0:
            return

        layer = self.canvas.currentLayer()

        if not layer.isEditable():
            return

        define._deletedFeatures = []
        for feat in selectedFeatures:
            define._deletedFeatures.append(feat)

        layer.deleteSelectedFeatures()
        self.mpActionEditCut.setChecked(False)
        self.editCutFunc()

    def editCopyFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        self.mpActionEditCopy.setEnabled(True)

        if self.mpActionEditCopy.isChecked():
            childActions = self.toolbarDigitizingToolsActionActions

            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart" and action.objectName() != "mpEditCopy":
                        action.setChecked(False)

            toolSelectByRect0 = SelectByRect(define._canvas)
            self.canvas.setMapTool(toolSelectByRect0)
            self.connect(toolSelectByRect0, SIGNAL("getSelectedFeatures"), self.copySelecetedFeatures)
        else:
            self.canvas.setMapTool(QgsMapToolPan(define._canvas))

    def copySelecetedFeatures(self, selectedFeatures):
        if selectedFeatures is None or len(selectedFeatures) == 0:
            return

        layer = self.canvas.currentLayer()

        if not layer.isEditable():
            return

        define._deletedFeatures = []

        for feat in selectedFeatures:
            define._deletedFeatures.append(feat)

        self.mpActionEditCopy.setChecked(False)
        self.editCopyFunc()

    def editPasteFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []
        self.mpActionEditPaste.setEnabled(True)
        layer = self.canvas.currentLayer()

        if not layer.isEditable():
            childActions = self.toolbarDigitizingToolsActionActions
            if len(childActions) != 0:
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setChecked(False)
            return

        if define._deletedFeatures is None or len(define._deletedFeatures) == 0:
            return

        for feat in define._deletedFeatures:
            newFeature = QgsFeature(layer.pendingFields(), 0)
            newFeature.setGeometry(feat.geometry())
            pr = layer.dataProvider()
            pr.addFeatures([newFeature])
            pass
        self.canvas.refresh()

    def toggleEditingFunc(self):
        if self.nodeTool is not None:
            if len(self.nodeTool.pointBubberBandList) > 0:
                QgisHelper.ClearRubberBandInCanvas(define._canvas, self.nodeTool.pointBubberBandList)
                self.nodeTool.pointBubberBandList = []

        if self.mpActionToggleEditing.isChecked():
            self.currentDigitizingLayer = self.canvas.currentLayer()
            if self.currentDigitizingLayer is not None and self.currentDigitizingLayer.type() == QgsMapLayer.VectorLayer:
                if self.currentDigitizingLayer.geometryType() == QGis.Line:
                    self.mpActionAddFeature.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCaptureLine.png"))
                elif self.currentDigitizingLayer.geometryType() == QGis.Polygon:
                    self.mpActionAddFeature.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCapturePolygon.png"))
                else:
                    self.mpActionAddFeature.setIcon(QIcon(self.currentDir + "/Resource/images/themes/default/mActionCapturePoint.png"))

                self.currentDigitizingLayer.startEditing()
                childActions = self.toolbarDigitizingToolsActionActions

                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setEnabled(True)
                if self.currentDigitizingLayer.geometryType() != QGis.Point:
                    self.btnCircularString.setEnabled(True)
                else:
                    self.btnCircularString.setEnabled(False)

                self.btnCurrentEdits.setEnabled(True)
            else:
                self.mpActionToggleEditing.setChecked(False)
                childActions = self.toolbarDigitizingToolsActionActions
                for action in childActions:
                    if action.objectName() != "mpEditStart":
                        action.setEnabled(False)
                self.btnCircularString.setEnabled(False)
                self.btnCurrentEdits.setEnabled(False)
            self.canvas.refresh()
        else:
            self.currentDigitizingLayer = self.canvas.currentLayer()

            if self.currentDigitizingLayer is not None and isinstance(self.currentDigitizingLayer, QgsVectorLayer):
                if self.currentDigitizingLayer.isModified():
                    result = QMessageBox.information(self, "Stop editing" ,"Do you want to save the changes to layer %s"%self.currentDigitizingLayer.name(),QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                    if result == QMessageBox.Yes:
                        self.canvas.setMapTool(QgsMapToolPan(define._canvas))
                        self.currentDigitizingLayer.commitChanges()
                        self.currentDigitizingLayer.triggerRepaint()
                    elif result == QMessageBox.No:
                        self.canvas.setMapTool(QgsMapToolPan(define._canvas))
                        self.canvas.freeze(True)
                        self.currentDigitizingLayer.rollBack()
                        self.canvas.freeze(False)
                        self.currentDigitizingLayer.triggerRepaint()
                    else:
                        self.mpActionToggleEditing.setChecked(True)
                        return

            if self.currentDigitizingLayer.isEditable():
                self.currentDigitizingLayer.commitChanges()

            childActions = self.toolbarDigitizingToolsActionActions

            if len(childActions) != 0:
                for action in childActions:
                    action.setChecked(False)
                    if action.objectName() != "mpEditStart":
                        action.setEnabled(False)
                self.btnCurrentEdits.setEnabled(False)
                self.btnCircularString.setEnabled(False)

    def openObstacleCheckFile(self):
        filePathDir = QFileDialog.getOpenFileName(self, "Open Input Data",QCoreApplication.applicationDirPath(),"Xml Files(*.xml)")

        if filePathDir == "":
            return

        result = DlgCrcCheck.smethod_0(self, filePathDir)

        if not result:
            return

        path = filePathDir
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def createFlightPlannerToolbar(self):
        mpObstacleLayer = QAction(self)
        mpObstacleLayer.setObjectName("mpObstacleLayer")        
        icon3 = QIcon(self.currentDir + "/Resource/addObstacle.png") 
        mpObstacleLayer.setIcon(icon3)
        mpObstacleLayer.setToolTip("Add Obstacle Points Layer") 

        mpActionTurnArea = QAction(self)
        mpActionTurnArea.setObjectName("mpTurnArea")
        mpActionTurnArea.setIcon(QIcon(self.currentDir + "/Resource/TurnArea.bmp"))
        mpActionTurnArea.setToolTip(SurfaceTypes.TurnArea)

        mpActionAerodromeSurfaces = QAction(self)
        mpActionAerodromeSurfaces.setObjectName("mpActionAerodromeSurfaces")
        mpActionAerodromeSurfaces.setIcon(QIcon(self.currentDir + "/Resource/AerodromeSurfaces.bmp"))
        mpActionAerodromeSurfaces.setToolTip(SurfaceTypes.AerodromeSurfaces)

        mpActionShielding = QAction(self)
        mpActionShielding.setObjectName("mpActionShielding")
        mpActionShielding.setIcon(QIcon(self.currentDir + "/Resource/Shielding.bmp"))
        mpActionShielding.setToolTip(SurfaceTypes.Shielding)
        
        mpActionHeliportSurfaces = QAction(self)
        mpActionHeliportSurfaces.setObjectName("mpActionBaroVnav")
        mpActionHeliportSurfaces.setIcon(QIcon(self.currentDir + "/Resource/HeliportSurfaces.bmp"))
        mpActionHeliportSurfaces.setToolTip(SurfaceTypes.HeliportSurfaces)

        mpActionBaroVnav = QAction(self)
        mpActionBaroVnav.setObjectName("mpActionBaroVnav")
        mpActionBaroVnav.setIcon(QIcon(self.currentDir + "/Resource/BaroVNAV.png"))
        mpActionBaroVnav.setToolTip("BaroVnavSurfaces")
        
        mpActionBasicGNSS = QAction(self)
        mpActionBasicGNSS.setObjectName("mpBasicGNSSAnalyser")
        mpActionBasicGNSS.setIcon(QIcon(self.currentDir + "/Resource/BasicGnssApproachObstacleAnalyser.bmp"))
        mpActionBasicGNSS.setToolTip("NON-Precision with T- or Y-Bar")
        
        mpActionApproachAlignment = QAction(self)
        mpActionApproachAlignment.setObjectName("mpmpActionApproachAlignmentAnalyser")
        mpActionApproachAlignment.setIcon(QIcon(self.currentDir + "/Resource/ApproachAlignment.bmp"))
        mpActionApproachAlignment.setToolTip("Approach Alignment")
        
        mpActionIlsOsa = QAction(self)
        mpActionIlsOsa.setObjectName("mpIlsOSA")
        mpActionIlsOsa.setIcon(QIcon(self.currentDir + "/Resource/IlsOas.bmp"))
        mpActionIlsOsa.setToolTip("Obstacle Assessment Surfaces (ILS OAS)")

        mpActionIlsOsaSbas = QAction(self)
        mpActionIlsOsaSbas.setObjectName("mpIlsOSASbas")
        mpActionIlsOsaSbas.setIcon(QIcon(self.currentDir + "/Resource/IlsOas.bmp"))
        mpActionIlsOsaSbas.setToolTip("Obstacle Assessment Surfaces (SBAS OAS)")
        
        mpActionRnpAr = QAction(self)
        mpActionRnpAr.setObjectName("mpRnpAr")
        mpActionRnpAr.setIcon(QIcon(self.currentDir + "/Resource/RnpAR.bmp"))
        mpActionRnpAr.setToolTip("RNP AR Obstacle Analyser")
        
        mpActionPinsDep = QAction(self)
        mpActionPinsDep.setObjectName("mpPinsDep")
        mpActionPinsDep.setIcon(QIcon(self.currentDir + "/Resource/PinSVisualSegmentDep.bmp"))
        mpActionPinsDep.setToolTip("PinS Visual Segment for Departures")
        
        mpActionPinsApp = QAction(self)
        mpActionPinsApp.setObjectName("mpPinsApp")
        mpActionPinsApp.setIcon(QIcon(self.currentDir + "/Resource/PinSVisualSegmentApp.bmp"))
        mpActionPinsApp.setToolTip("PinS Visual Segment for Approach")
        
        mpActionVSS = QAction(self)
        mpActionVSS.setObjectName("mpVSS")
        mpActionVSS.setIcon(QIcon(self.currentDir + "/Resource/VisualSegmentSurface.bmp"))
        mpActionVSS.setToolTip("Visual Segment Surface")
        
        mpActionTAA = QAction(self)
        mpActionTAA.setObjectName("mpTAA")
        mpActionTAA.setIcon(QIcon(self.currentDir + "/Resource/TaaCalculation.bmp"))
        mpActionTAA.setToolTip("Terminal Arrival Altitudes(TAA)")
        
        mpActionObstacleRasterLayer = QAction(self)
        mpActionObstacleRasterLayer.setObjectName("mpObstacleRasterLayer")
        mpActionObstacleRasterLayer.setIcon(QIcon(self.currentDir + "/Resource/mActionAddRasterLayer.png"))
        mpActionObstacleRasterLayer.setToolTip("Add Obstacle Raster Layer")
        
        mpActionBaseTurn = QAction(self)
        mpActionBaseTurn.setObjectName("mpBaseTurn")
        mpActionBaseTurn.setIcon(QIcon(self.currentDir + "/Resource/HoldingBase.bmp"))
        mpActionBaseTurn.setToolTip("Base Turn Template Construction")
        
        mpActionCrm = QAction(self)
        mpActionCrm.setObjectName("mpCrm")
        mpActionCrm.setIcon(QIcon(self.currentDir + "/Resource/IlsCrm.bmp"))
        mpActionCrm.setToolTip("Collision Risk Model Obstacle File Creation")
        
        mpActionHoldingRnp = QAction(self)
        mpActionHoldingRnp.setObjectName("mpHoldingRnp")
        mpActionHoldingRnp.setIcon(QIcon(self.currentDir + "/Resource/HoldingRnp.bmp"))
        mpActionHoldingRnp.setToolTip("RNP Holding")
        
        
        mpActionHoldingRace_P = QAction(self)
        mpActionHoldingRace_P.setObjectName("mpHoldingRace_P")
        mpActionHoldingRace_P.setIcon(QIcon(self.currentDir + "/Resource/HoldingRace.bmp"))
        mpActionHoldingRace_P.setToolTip("Holding Pattern Template Construction")
        
        mpActionHoldingOverHead = QAction(self)
        mpActionHoldingOverHead.setObjectName("mpHoldingOverHead")
        mpActionHoldingOverHead.setIcon(QIcon(self.currentDir + "/Resource/HoldingOverHead.bmp"))
        mpActionHoldingOverHead.setToolTip("Over-head Holding / Racetrack")
        
        mpActionHoldingVorDme = QAction(self)
        mpActionHoldingVorDme.setObjectName("mpHoldingVorDme")
        mpActionHoldingVorDme.setIcon(QIcon(self.currentDir + "/Resource/HoldingVorDme.bmp"))
        mpActionHoldingVorDme.setToolTip("VOR/DME Holding / Racetrack")
        
        mpActionDmeTolerance = QAction(self)
        mpActionDmeTolerance.setObjectName("mpDmeTolerance")
        mpActionDmeTolerance.setIcon(QIcon(self.currentDir + "/Resource/DmeTolerance.bmp"))
        mpActionDmeTolerance.setToolTip("DME Tolerance and Slant Range")
        
        mpActionDepartureNominal = QAction(self)
        mpActionDepartureNominal.setObjectName("mpCrm")
        mpActionDepartureNominal.setIcon(QIcon(self.currentDir + "/Resource/DepartureNominal.bmp"))
        mpActionDepartureNominal.setToolTip("Departure Average Flight Path Construction")
        
        mpActionDmeUpdateArea = QAction(self)
        mpActionDmeUpdateArea.setObjectName("mpDmeUpdateArea")
        mpActionDmeUpdateArea.setIcon(QIcon(self.currentDir + "/Resource/RnavDmeUpdateArea.bmp"))
        mpActionDmeUpdateArea.setToolTip("DME Update Area Construction")
        
        mpActionRnavHolding = QAction(self)
        mpActionRnavHolding.setObjectName("mpRnavHolding")
        mpActionRnavHolding.setIcon(QIcon(self.currentDir + "/Resource/HoldingRnav.bmp"))
        mpActionRnavHolding.setToolTip("RNAV Holding")
        
        mpActionRnavVorDme = QAction(self)
        mpActionRnavVorDme.setObjectName("mpRnavVorDme")
        mpActionRnavVorDme.setIcon(QIcon(self.currentDir + "/Resource/RnavVorDme.bmp"))
        mpActionRnavVorDme.setToolTip("RNAV Protection Area (VOR/DME)")
        
        mpActionRnavDmeDme = QAction(self)
        mpActionRnavDmeDme.setObjectName("mpRnavDmeDme")
        mpActionRnavDmeDme.setIcon(QIcon(self.currentDir + "/Resource/RnavDmeDme.bmp"))
        mpActionRnavDmeDme.setToolTip("RNAV Protection Area (DME/DME)")
        
        mpActionVisualCircling = QAction(self)
        mpActionVisualCircling.setObjectName("mpVisualCircling")
        mpActionVisualCircling.setIcon(QIcon(self.currentDir + "/Resource/VisualCircling.bmp"))
        mpActionVisualCircling.setToolTip(SurfaceTypes.VisualCircling)
        
        mpActionMSA = QAction(self)
        mpActionMSA.setObjectName("mpMSA")
        mpActionMSA.setIcon(QIcon(self.currentDir + "/Resource/MsaCalculation.bmp"))
        mpActionMSA.setToolTip(SurfaceTypes.MSA)
        
        mpActionDataImport = QAction(self)
        mpActionDataImport.setObjectName("mpDataImport")
        mpActionDataImport.setIcon(QIcon(self.currentDir + "/Resource/DataImport.bmp"))
        mpActionDataImport.setToolTip(SurfaceTypes.DataImport)
        
        mpActionEnrouteStraight = QAction(self)
        mpActionEnrouteStraight.setObjectName("mpEnrouteStraight")
        mpActionEnrouteStraight.setIcon(QIcon(self.currentDir + "/Resource/EnrouteStraight.bmp"))
        mpActionEnrouteStraight.setToolTip(SurfaceTypes.EnrouteStraight)
        
        mpActionEnrouteTurnOverHead = QAction(self)
        mpActionEnrouteTurnOverHead.setObjectName("mpEnrouteTurnOverHead")
        mpActionEnrouteTurnOverHead.setIcon(QIcon(self.currentDir + "/Resource/EnrouteTurnOverHead.bmp"))
        mpActionEnrouteTurnOverHead.setToolTip(SurfaceTypes.EnrouteTurnOverHead)

        mpActionDepartureRnav= QAction(self)
        mpActionDepartureRnav.setObjectName("mpDepartureRnav")
        mpActionDepartureRnav.setIcon(QIcon(self.currentDir + "/Resource/DepartureRnav.bmp"))
        mpActionDepartureRnav.setToolTip(SurfaceTypes.DepartureRnav)
        
        mpActionDepartureStandard = QAction(self)
        mpActionDepartureStandard.setObjectName("mpDepartureStandard")
        mpActionDepartureStandard.setIcon(QIcon(self.currentDir + "/Resource/DepartureStandard.bmp"))
        mpActionDepartureStandard.setToolTip(SurfaceTypes.DepartureStandard)
                
        mpActionDepartureOmnidirectional = QAction(self)
        mpActionDepartureOmnidirectional.setObjectName("mpDepartureOmnidirectional")
        mpActionDepartureOmnidirectional.setIcon(QIcon(self.currentDir + "/Resource/DepartureOmnidirectional.bmp"))
        mpActionDepartureOmnidirectional.setToolTip(SurfaceTypes.DepartureOmnidirectional)

        mpActionRnavStraightSegmentAnalyser = QAction(self)
        mpActionRnavStraightSegmentAnalyser.setObjectName("mpRnavStraightSegmentAnalyser")
        mpActionRnavStraightSegmentAnalyser.setIcon(QIcon(self.currentDir + "/Resource/RnavStraightSegmentAnalyser.bmp"))
        mpActionRnavStraightSegmentAnalyser.setToolTip(SurfaceTypes.RnavStraightSegmentAnalyser)

        mpActionRnavTurningSegmentAnalyser = QAction(self)
        mpActionRnavTurningSegmentAnalyser.setObjectName("mpRnavTurningSegmentAnalyser")
        mpActionRnavTurningSegmentAnalyser.setIcon(QIcon(self.currentDir + "/Resource/RnavTurningSegmentAnalyser.bmp"))
        mpActionRnavTurningSegmentAnalyser.setToolTip(SurfaceTypes.RnavTurningSegmentAnalyser)

        mpActionTurnProtectionAndObstacleAssessment = QAction(self)
        mpActionTurnProtectionAndObstacleAssessment.setObjectName("mpTurnProtectionAndObstacleAssessment")
        mpActionTurnProtectionAndObstacleAssessment.setIcon(QIcon(self.currentDir + "/Resource/RnavTurningSegmentAnalyser.bmp"))
        mpActionTurnProtectionAndObstacleAssessment.setToolTip(SurfaceTypes.TurnProtectionAndObstacleAssessment)
        
        mpActionRadial = QAction(self)
        mpActionRadial.setObjectName("mpRadial")
        mpActionRadial.setIcon(QIcon(self.currentDir + "/Resource/Radial.bmp"))
        mpActionRadial.setToolTip(SurfaceTypes.Radial)

        mpActionIlsBasic = QAction(self)
        mpActionIlsBasic.setObjectName("mpIlsBasic")
        mpActionIlsBasic.setIcon(QIcon(self.currentDir + "/Resource/IlsBasic.bmp"))
        mpActionIlsBasic.setToolTip(SurfaceTypes.IlsBasic)

        mpActionIasToTas = QAction(self)
        mpActionIasToTas.setObjectName("mpIasToTas")
        mpActionIasToTas.setIcon(QIcon(self.currentDir + "/Resource/IasToTas.bmp"))
        mpActionIasToTas.setToolTip(SurfaceTypes.IasToTas)

        mpActionFixToleranceArea = QAction(self)
        mpActionFixToleranceArea.setObjectName("mpFixToleranceArea")
        mpActionFixToleranceArea.setIcon(QIcon(self.currentDir + "/Resource/OverheadTolerance.bmp"))
        mpActionFixToleranceArea.setToolTip(SurfaceTypes.FixToleranceArea)

        mpActionFixConstruction = QAction(self)
        mpActionFixConstruction.setObjectName("mpFixConstruction")
        mpActionFixConstruction.setIcon(QIcon(self.currentDir + "/Resource/FixConstruction.bmp"))
        mpActionFixConstruction.setToolTip(SurfaceTypes.FixConstruction)

        mpActionRnavNominal = QAction(self)
        mpActionRnavNominal.setObjectName("mpRnavNominal")
        mpActionRnavNominal.setIcon(QIcon(self.currentDir + "/Resource/RnavNominal.bmp"))
        mpActionRnavNominal.setToolTip(SurfaceTypes.RnavNominal)

        mpActionObstacleEvaluator = QAction(self)
        mpActionObstacleEvaluator.setObjectName("mpObstacleEvaluator")
        mpActionObstacleEvaluator.setIcon(QIcon(self.currentDir + "/Resource/SecondaryMoc.bmp"))
        mpActionObstacleEvaluator.setToolTip(SurfaceTypes.ObstacleEvaluator)

        mpActionPathTerminators = QAction(self)
        mpActionPathTerminators.setObjectName("mpPathTerminators")
        mpActionPathTerminators.setIcon(QIcon(self.currentDir + "/Resource/PathTerminators.bmp"))
        mpActionPathTerminators.setToolTip(SurfaceTypes.PathTerminators)

        mpActionFasDataBlock = QAction(self)
        mpActionFasDataBlock.setObjectName("mpFasDataBlock")
        mpActionFasDataBlock.setIcon(QIcon(self.currentDir + "/Resource/FasDataBlock.bmp"))
        mpActionFasDataBlock.setToolTip(SurfaceTypes.FasDataBlock)

        mpActionProcedureExport= QAction(self)
        mpActionProcedureExport.setObjectName("mpProcedureExport")
        mpActionProcedureExport.setIcon(QIcon(self.currentDir + "/Resource/ProcedureExport.bmp"))
        mpActionProcedureExport.setToolTip(SurfaceTypes.ProcedureExport)

        mpActionProfileManager= QAction(self)
        mpActionProfileManager.setObjectName("mpProfileManager")
        mpActionProfileManager.setIcon(QIcon(self.currentDir + "/Resource/ProfileManager.bmp"))
        mpActionProfileManager.setToolTip(SurfaceTypes.ProfileManager)

        mpActionDataExport = QAction(self)
        mpActionDataExport.setObjectName("mpDataExport")
        mpActionDataExport.setIcon(QIcon(self.currentDir + "/Resource/DataExport.bmp"))
        mpActionDataExport.setToolTip(SurfaceTypes.DataExport)

        mpActionApproachSegment = QAction(self)
        mpActionApproachSegment.setObjectName("mpApproachSegment")
        mpActionApproachSegment.setIcon(QIcon(self.currentDir + "/Resource/ApproachSegment.bmp"))
        mpActionApproachSegment.setToolTip(SurfaceTypes.ApproachSegment)

        mpActionMASegment = QAction(self)
        mpActionMASegment.setObjectName("mpMASegment")
        mpActionMASegment.setIcon(QIcon(self.currentDir + "/Resource/MASegment.bmp"))
        mpActionMASegment.setToolTip(SurfaceTypes.MASegment)

        mpActionHolding = QAction(self)
        mpActionHolding.setObjectName("mpHolding")
        mpActionHolding.setIcon(QIcon(self.currentDir + "/Resource/HoldingCmd.bmp"))
        mpActionHolding.setToolTip(SurfaceTypes.Holding)

        mpActionChatingGrid = QAction(self)
        mpActionChatingGrid.setObjectName("mpActionChatingGrid")
        mpActionChatingGrid.setIcon(QIcon(self.currentDir + "/Resource/ChartingGrid.bmp"))
        mpActionChatingGrid.setToolTip(SurfaceTypes.ChartingGrid)

        mpActionChatingTemplates = QAction(self)
        mpActionChatingTemplates.setObjectName("mpActionChatingTemplates")
        mpActionChatingTemplates.setIcon(QIcon(self.currentDir + "/Resource/ChartingTemplates.bmp"))
        mpActionChatingTemplates.setToolTip(SurfaceTypes.ChartingTemplates)

        mpActionRaceTrackNavAid = QAction(self)
        mpActionRaceTrackNavAid.setObjectName("mpRaceTrackNavAid")
        mpActionRaceTrackNavAid.setToolTip(SurfaceTypes.RaceTrackNavAid)
        mpActionRaceTrackNavAid.setText(SurfaceTypes.RaceTrackNavAid)
        self.connect(mpActionRaceTrackNavAid, SIGNAL("triggered()"), self.mpActionRaceTrackNavAid_Func)

        mpActionRaceTrackFix = QAction(self)
        mpActionRaceTrackFix.setObjectName("mpRaceTrackFix")
        mpActionRaceTrackFix.setToolTip(SurfaceTypes.RaceTrackFix)
        mpActionRaceTrackFix.setText(SurfaceTypes.RaceTrackFix)
        self.connect(mpActionRaceTrackFix, SIGNAL("triggered()"), self.mpActionRaceTrackFix_Func)

        self.btnRaceTrack = QToolButton()
        self.btnRaceTrack.setPopupMode(QToolButton.InstantPopup)
        mnu = QMenu()
        mnu.addAction(mpActionRaceTrackNavAid)
        mnu.addAction(mpActionRaceTrackFix)
        self.btnRaceTrack.setMenu(mnu)
        self.btnRaceTrack.setToolTip("Race Track")
        self.btnRaceTrack.setIcon(QIcon(self.currentDir + "/Resource/RaceTrackCmd.bmp"))

        self.connect(mpObstacleLayer, SIGNAL("triggered()"), self.addObstacleLayer)
        self.connect(mpActionObstacleRasterLayer, SIGNAL("triggered()"), self.addObstacleRasterLayer)
        self.connect(mpActionAerodromeSurfaces, SIGNAL("triggered()"), self.aerodromeSurfacesShow)
        self.connect(mpActionShielding, SIGNAL("triggered()"), self.shieldingShow)
        self.connect(mpActionHeliportSurfaces, SIGNAL("triggered()"), self.heliportSurfacesShow)
        self.connect(mpActionBaroVnav, SIGNAL("triggered()"), self.baroVnavSurfaces)
        self.connect(mpActionBasicGNSS, SIGNAL("triggered()"), self.basicGNSS)
        self.connect(mpActionApproachAlignment, SIGNAL("triggered()"), self.approachAlignment)
        self.connect(mpActionIlsOsa, SIGNAL("triggered()"), self.IlsOsa)
        self.connect(mpActionIlsOsaSbas, SIGNAL("triggered()"), self.IlsOsaSbas)
        self.connect(mpActionRnpAr, SIGNAL("triggered()"), self.RnpAr)   
        self.connect(mpActionPinsDep, SIGNAL("triggered()"), self.PinSVisualSegmentDep) 
        self.connect(mpActionPinsApp, SIGNAL("triggered()"), self.PinSVisualSegmentApp) 
        self.connect(mpActionVSS, SIGNAL("triggered()"), self.VisualSegmentSurface) 
        self.connect(mpActionBaseTurn, SIGNAL("triggered()"), self.BaseTurnTC)
        self.connect(mpActionCrm, SIGNAL("triggered()"), self.CrmShow)
        self.connect(mpActionDepartureNominal, SIGNAL("triggered()"), self.DepartureNominalShow)
        self.connect(mpActionTAA, SIGNAL("triggered()"), self.TaaShow)
        self.connect(mpActionDmeTolerance, SIGNAL("triggered()"), self.DmeToleranceShow)
        self.connect(mpActionDmeUpdateArea, SIGNAL("triggered()"), self.DmeUpdateAreaShow)
        self.connect(mpActionRnavHolding, SIGNAL("triggered()"), self.HoldingRnavShow)
        self.connect(mpActionHoldingRnp, SIGNAL("triggered()"), self.HoldingRnpDlgShow)
        self.connect(mpActionRnavVorDme, SIGNAL("triggered()"), self.RnavVorDmeShow)
        self.connect(mpActionRnavDmeDme, SIGNAL("triggered()"), self.RnavDmeDmeShow)
        self.connect(mpActionVisualCircling, SIGNAL("triggered()"), self.VisualCirclingShow)
        self.connect(mpActionMSA, SIGNAL("triggered()"), self.MSAShow)
        self.connect(mpActionDataImport, SIGNAL("triggered()"), self.DataImportShow)
        self.connect(mpActionHoldingOverHead, SIGNAL("triggered()"), self.HoldingOverHeadDlgShow)
        self.connect(mpActionHoldingVorDme, SIGNAL("triggered()"), self.HoldingVorDmeShow)
        self.connect(mpActionEnrouteStraight, SIGNAL("triggered()"), self.EnrouteStraightShow)
        self.connect(mpActionEnrouteTurnOverHead, SIGNAL("triggered()"), self.EnrouteTurnOverHeadShow)
        self.connect(mpActionHoldingRace_P, SIGNAL("triggered()"), self.HoldingRace_PShow)
        self.connect(mpActionDepartureRnav, SIGNAL("triggered()"), self.DepartureRnavShow)
        self.connect(mpActionDepartureOmnidirectional, SIGNAL("triggered()"), self.DepartureOmnidirectionalShow)
        self.connect(mpActionDepartureStandard, SIGNAL("triggered()"), self.DepartureStandardShow)
        self.connect(mpActionRnavStraightSegmentAnalyser, SIGNAL("triggered()"), self.RnavStraightSegmentAnalyserShow)
        self.connect(mpActionRnavTurningSegmentAnalyser, SIGNAL("triggered()"), self.RnavTurningSegmentAnalyserShow)
        self.connect(mpActionTurnProtectionAndObstacleAssessment, SIGNAL("triggered()"), self.TurnProtectionAndObstacleAssessmentShow)
        self.connect(mpActionRadial, SIGNAL("triggered()"), self.RadialShow)
        self.connect(mpActionIlsBasic, SIGNAL("triggered()"), self.IlsBasicShow)
        self.connect(mpActionIasToTas, SIGNAL("triggered()"), self.IasToTasShow)
        self.connect(mpActionTurnArea, SIGNAL("triggered()"), self.TurnAreaShow)
        self.connect(mpActionFixToleranceArea, SIGNAL("triggered()"), self.FixToleranceAreaShow)
        self.connect(mpActionRnavNominal, SIGNAL("triggered()"), self.RnavNominalShow)
        self.connect(mpActionObstacleEvaluator, SIGNAL("triggered()"), self.ObstacleEvaluatorShow)
        self.connect(mpActionPathTerminators, SIGNAL("triggered()"), self.PathTerminatorsShow)
        self.connect(mpActionFasDataBlock, SIGNAL("triggered()"), self.FasDataBlockShow)
        self.connect(mpActionProcedureExport, SIGNAL("triggered()"), self.ProcedureExportShow)
        self.connect(mpActionProfileManager, SIGNAL("triggered()"), self.ProfileManagerShow)
        self.connect(mpActionDataExport, SIGNAL("triggered()"), self.DataExportShow)
        self.connect(mpActionApproachSegment, SIGNAL("triggered()"), self.ApproachSegmentShow)
        self.connect(mpActionMASegment, SIGNAL("triggered()"), self.MASegmentShow)
        self.connect(mpActionHolding, SIGNAL("triggered()"), self.HoldingShow)
        self.connect(mpActionChatingGrid, SIGNAL("triggered()"), self.ChartingGridDlgShow)
        self.connect(mpActionChatingTemplates, SIGNAL("triggered()"), self.ChartingTemplatesDlgShow)

        self.toolbarFlightPlannerImportExportToolsAction = self.addToolBar("Import / Export Tools")
        self.toolbarFlightPlannerImportExportToolsAction.addAction(mpObstacleLayer)
        self.toolbarFlightPlannerImportExportToolsAction.addAction(mpActionObstacleRasterLayer)
        self.toolbarFlightPlannerImportExportToolsAction.addAction(self.mpActionAddVectorData)
        self.toolbarFlightPlannerImportExportToolsAction.addAction(mpActionDataImport)
        self.toolbarFlightPlannerImportExportToolsAction.addAction(mpActionDataExport)
        self.toolbarFlightPlannerImportExportToolsAction.addAction(mpActionPathTerminators)
        self.toolbarFlightPlannerImportExportToolsAction.addAction(mpActionProcedureExport)
        self.viewMenu.addAction(self.toolbarFlightPlannerImportExportToolsAction.toggleViewAction())

        self.toolbarFlightPlannerOlsSurfaces = self.addToolBar("OLS Surfaces")
        self.toolbarFlightPlannerOlsSurfaces.addAction(mpActionAerodromeSurfaces)
        self.toolbarFlightPlannerOlsSurfaces.addAction(mpActionHeliportSurfaces)
        self.toolbarFlightPlannerOlsSurfaces.addAction(mpActionShielding)

        self.toolbarFlightPlannerConventionalApproachToolsAction = self.addToolBar("Conventional Approach Tools")
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionCrm)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionIlsOsa)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionIlsBasic)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionHolding)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addWidget(self.btnRaceTrack)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionHoldingOverHead)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionHoldingVorDme)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionBaseTurn)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionApproachSegment)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionMASegment)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionVisualCircling)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionMSA)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionApproachAlignment)
        self.toolbarFlightPlannerConventionalApproachToolsAction.addAction(mpActionVSS)

        self.viewMenu.addAction(self.toolbarFlightPlannerConventionalApproachToolsAction.toggleViewAction())

        self.toolbarFlightPlannerConventionalDepartureToolsAction = self.addToolBar("Conventional Departure Tools")
        self.toolbarFlightPlannerConventionalDepartureToolsAction.addAction(mpActionDepartureNominal)
        self.toolbarFlightPlannerConventionalDepartureToolsAction.addAction(mpActionDmeTolerance)
        self.toolbarFlightPlannerConventionalDepartureToolsAction.addAction(mpActionDepartureOmnidirectional)
        self.toolbarFlightPlannerConventionalDepartureToolsAction.addAction(mpActionDepartureStandard)
        self.viewMenu.addAction(self.toolbarFlightPlannerConventionalDepartureToolsAction.toggleViewAction())

        self.toolbarFlightPlannerConventionalEnrouteToolsAction = self.addToolBar("Conventional Enroute Tools")
        self.toolbarFlightPlannerConventionalEnrouteToolsAction.addAction(mpActionEnrouteStraight)
        self.toolbarFlightPlannerConventionalEnrouteToolsAction.addAction(mpActionEnrouteTurnOverHead)
        self.viewMenu.addAction(self.toolbarFlightPlannerConventionalEnrouteToolsAction.toggleViewAction())

        self.toolbarFlightPlannerPBNToolsAction = self.addToolBar("PBN Tools")
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnavNominal)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionBaroVnav)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionBasicGNSS)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionIlsOsaSbas)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionFasDataBlock)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnpAr)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnavHolding)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionHoldingRnp)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionTAA)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnavStraightSegmentAnalyser)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnavTurningSegmentAnalyser)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionTurnProtectionAndObstacleAssessment)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionDmeUpdateArea)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnavVorDme)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionRnavDmeDme)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionDepartureRnav)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionPinsDep)
        self.toolbarFlightPlannerPBNToolsAction.addAction(mpActionPinsApp)
        self.viewMenu.addAction(self.toolbarFlightPlannerPBNToolsAction.toggleViewAction())

        self.toolbarFlightPlannerPansOpsToolsAction = self.addToolBar("PANS OPS Tools")
        self.toolbarFlightPlannerPansOpsToolsAction.addAction(mpActionRadial)
        self.toolbarFlightPlannerPansOpsToolsAction.addAction(mpActionIasToTas)
        self.toolbarFlightPlannerPansOpsToolsAction.addAction(mpActionTurnArea)
        self.toolbarFlightPlannerPansOpsToolsAction.addAction(mpActionFixToleranceArea)
        self.toolbarFlightPlannerPansOpsToolsAction.addAction(mpActionObstacleEvaluator)
        self.viewMenu.addAction(self.toolbarFlightPlannerPansOpsToolsAction.toggleViewAction())

        self.toolbarFlightPlannerChartingToolsAction = self.addToolBar("Charting Tools")
        self.toolbarFlightPlannerChartingToolsAction.addAction(mpActionProfileManager)
        self.toolbarFlightPlannerChartingToolsAction.addAction(mpActionChatingGrid)
        self.viewMenu.addAction(self.toolbarFlightPlannerChartingToolsAction.toggleViewAction())

        # Add on Menu
        menuBar = self.menuBar()
        mnuImportExportTools = menuBar.addMenu("&Import / Export Tools")
        mpObstacleLayer.setText("Add Obstacle Points Layer")
        mpActionObstacleRasterLayer.setText("Add Obstacle Raster Layer")
        mpActionDataImport.setText(SurfaceTypes.DataImport)
        mpActionDataExport.setText(SurfaceTypes.DataExport)
        mpActionPathTerminators.setText(SurfaceTypes.PathTerminators)
        mpActionProcedureExport.setText(SurfaceTypes.ProcedureExport)
        self.mpActionAddVectorData.setText("Add Vector Data")

        mnuImportExportTools.addAction(mpObstacleLayer)
        mnuImportExportTools.addAction(mpActionObstacleRasterLayer)
        mnuImportExportTools.addAction(self.mpActionAddVectorData)
        mnuImportExportTools.addAction(mpActionDataImport)
        mnuImportExportTools.addAction(mpActionDataExport)
        mnuImportExportTools.addAction(mpActionPathTerminators)
        mnuImportExportTools.addAction(mpActionProcedureExport)

        mnuOlsSurfaces = menuBar.addMenu("&OLS Surfaces")
        mpActionAerodromeSurfaces.setText(SurfaceTypes.AerodromeSurfaces)
        mnuOlsSurfaces.addAction(mpActionAerodromeSurfaces)
        
        mpActionHeliportSurfaces.setText(SurfaceTypes.HeliportSurfaces)
        mnuOlsSurfaces.addAction(mpActionHeliportSurfaces)

        mpActionShielding.setText(SurfaceTypes.Shielding)
        mnuOlsSurfaces.addAction(mpActionShielding)

        mnuConventionalApproachTools = menuBar.addMenu("&Conventional Approach Tools")
        mpActionCrm.setText(SurfaceTypes.CRM)
        mpActionIlsOsa.setText(SurfaceTypes.IlsOas)
        mpActionIlsBasic.setText(SurfaceTypes.IlsBasic)
        mpActionHoldingOverHead.setText(SurfaceTypes.HoldingOverHead)
        mpActionHoldingVorDme.setText(SurfaceTypes.HoldingVorDme)
        mpActionBaseTurn.setText(SurfaceTypes.BaseTurnTC)
        mpActionApproachSegment.setText(SurfaceTypes.ApproachSegment)
        mpActionMASegment.setText(SurfaceTypes.MASegment)
        mpActionVisualCircling.setText(SurfaceTypes.VisualCircling)
        mpActionMSA.setText(SurfaceTypes.MSA)
        mpActionApproachAlignment.setText(SurfaceTypes.ApproachAlignment)
        mpActionVSS.setText(SurfaceTypes.VisualSegmentSurface)
        
        mnuConventionalApproachTools.addAction(mpActionCrm)
        mnuConventionalApproachTools.addAction(mpActionIlsOsa)
        mnuConventionalApproachTools.addAction(mpActionIlsBasic)
        mnuConventionalApproachTools.addAction(mpActionHoldingOverHead)
        mnuConventionalApproachTools.addAction(mpActionHoldingVorDme)
        mnuConventionalApproachTools.addAction(mpActionBaseTurn)
        mnuConventionalApproachTools.addAction(mpActionApproachSegment)
        mnuConventionalApproachTools.addAction(mpActionMASegment)
        mnuConventionalApproachTools.addAction(mpActionVisualCircling)
        mnuConventionalApproachTools.addAction(mpActionMSA)
        mnuConventionalApproachTools.addAction(mpActionApproachAlignment)
        mnuConventionalApproachTools.addAction(mpActionVSS)
        
        mnuConventionalDepartureTools = menuBar.addMenu("&Conventional Departure Tools")
        mpActionDepartureNominal.setText(SurfaceTypes.DepartureNominal)
        mpActionDmeTolerance.setText(SurfaceTypes.DmeTolerance)
        mpActionDepartureOmnidirectional.setText(SurfaceTypes.DepartureOmnidirectional)
        mpActionDepartureStandard.setText(SurfaceTypes.DepartureStandard)

        mnuConventionalDepartureTools.addAction(mpActionDepartureNominal)
        mnuConventionalDepartureTools.addAction(mpActionDmeTolerance)
        mnuConventionalDepartureTools.addAction(mpActionDepartureOmnidirectional)
        mnuConventionalDepartureTools.addAction(mpActionDepartureStandard)
        
        mnuConventionalEnrouteTools = menuBar.addMenu("&Conventional Enroute Tools")
        mpActionEnrouteStraight.setText(SurfaceTypes.EnrouteStraight)
        mpActionEnrouteTurnOverHead.setText(SurfaceTypes.EnrouteTurnOverHead)
        
        mnuConventionalEnrouteTools.addAction(mpActionEnrouteStraight)
        mnuConventionalEnrouteTools.addAction(mpActionEnrouteTurnOverHead)
        
        mnuPBNTools = menuBar.addMenu("&PBN Tools")
        mpActionRnavNominal.setText(SurfaceTypes.RnavNominal)
        mpActionBaroVnav.setText(SurfaceTypes.BaroVNAV)
        mpActionBasicGNSS.setText(SurfaceTypes.BasicGNSS)
        mpActionIlsOsaSbas.setText(SurfaceTypes.SbasOas)
        mpActionFasDataBlock.setText(SurfaceTypes.FasDataBlock)
        mpActionRnpAr.setText(SurfaceTypes.RnpAR)
        mpActionRnavHolding.setText(SurfaceTypes.HoldingRnav)
        mpActionHoldingRnp.setText(SurfaceTypes.HoldingRnp)
        mpActionTAA.setText(SurfaceTypes.TaaCalculation)
        mpActionRnavStraightSegmentAnalyser.setText(SurfaceTypes.RnavStraightSegmentAnalyser)
        mpActionRnavTurningSegmentAnalyser.setText(SurfaceTypes.RnavTurningSegmentAnalyser)
        mpActionTurnProtectionAndObstacleAssessment.setText(SurfaceTypes.TurnProtectionAndObstacleAssessment)
        mpActionDmeUpdateArea.setText(SurfaceTypes.DmeUpdateArea)
        mpActionRnavVorDme.setText(SurfaceTypes.RnavVorDme)
        mpActionRnavDmeDme.setText(SurfaceTypes.RnavDmeDme)
        mpActionDepartureRnav.setText(SurfaceTypes.DepartureRnav)
        mpActionPinsDep.setText(SurfaceTypes.PinSVisualSegmentDep)
        mpActionPinsApp.setText(SurfaceTypes.PinSVisualSegmentApp)

        mnuPBNTools.addAction(mpActionRnavNominal)
        mnuPBNTools.addAction(mpActionBaroVnav)
        mnuPBNTools.addAction(mpActionBasicGNSS)
        mnuPBNTools.addAction(mpActionIlsOsaSbas)
        mnuPBNTools.addAction(mpActionFasDataBlock)
        mnuPBNTools.addAction(mpActionRnpAr)
        mnuPBNTools.addAction(mpActionRnavHolding)
        mnuPBNTools.addAction(mpActionHoldingRnp)
        mnuPBNTools.addAction(mpActionTAA)
        mnuPBNTools.addAction(mpActionRnavStraightSegmentAnalyser)
        mnuPBNTools.addAction(mpActionRnavTurningSegmentAnalyser)
        mnuPBNTools.addAction(mpActionTurnProtectionAndObstacleAssessment)
        mnuPBNTools.addAction(mpActionDmeUpdateArea)
        mnuPBNTools.addAction(mpActionRnavVorDme)
        mnuPBNTools.addAction(mpActionRnavDmeDme)
        mnuPBNTools.addAction(mpActionDepartureRnav)
        mnuPBNTools.addAction(mpActionPinsDep)
        mnuPBNTools.addAction(mpActionPinsApp)

        mnuPANSOPSTools = menuBar.addMenu("&PANS OPS Tools")
        mpActionRadial.setText(SurfaceTypes.Radial)
        mpActionIasToTas.setText(SurfaceTypes.IasToTas)
        mpActionTurnArea.setText(SurfaceTypes.TurnArea)
        mpActionFixToleranceArea.setText(SurfaceTypes.FixToleranceArea)
        mpActionObstacleEvaluator.setText(SurfaceTypes.ObstacleEvaluator)

        mnuPANSOPSTools.addAction(mpActionRadial)
        mnuPANSOPSTools.addAction(mpActionIasToTas)
        mnuPANSOPSTools.addAction(mpActionTurnArea)
        mnuPANSOPSTools.addAction(mpActionFixToleranceArea)
        mnuPANSOPSTools.addAction(mpActionObstacleEvaluator)

        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC = mnuPANSOPSTools.addMenu("DA/MAPt Position & Calculation of SOC")
        # Add mnuDAMAPtPositionAndCalculationOfSOC within menu
        mpActionPaIls = QAction(self)
        mpActionPaIls.setObjectName("mpActionPaIls")
        mpActionPaIls.setToolTip(SurfaceTypes.PaIls)
        mpActionPaIls.setText(SurfaceTypes.PaIls)
        self.connect(mpActionPaIls, SIGNAL("triggered()"), self.PaIlsDlgShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionPaIls)

        mpActionPaGbas = QAction(self)
        mpActionPaGbas.setObjectName("mpActionPaGbas")
        mpActionPaGbas.setToolTip(SurfaceTypes.PaGbas)
        mpActionPaGbas.setText(SurfaceTypes.PaGbas)
        self.connect(mpActionPaGbas, SIGNAL("triggered()"), self.PaGbasDlgShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionPaGbas)

        mpActionBARO_VNAV = QAction(self)
        mpActionBARO_VNAV.setObjectName("mpActionBARO_VNAV")
        mpActionBARO_VNAV.setToolTip(SurfaceTypes.BARO_VNAV)
        mpActionBARO_VNAV.setText(SurfaceTypes.BARO_VNAV)
        self.connect(mpActionBARO_VNAV, SIGNAL("triggered()"), self.BARO_VNAVShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionBARO_VNAV)

        mpActionSBAS = QAction(self)
        mpActionSBAS.setObjectName("mpActionSBAS")
        mpActionSBAS.setToolTip(SurfaceTypes.SBAS)
        mpActionSBAS.setText(SurfaceTypes.SBAS)
        self.connect(mpActionSBAS, SIGNAL("triggered()"), self.SBASShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionSBAS)

        mpActionNpaOnFix = QAction(self)
        mpActionNpaOnFix.setObjectName("mpActionNpaOnFix")
        mpActionNpaOnFix.setToolTip(SurfaceTypes.NpaOnFix)
        mpActionNpaOnFix.setText(SurfaceTypes.NpaOnFix)
        self.connect(mpActionNpaOnFix, SIGNAL("triggered()"), self.NpaOnFixDlgShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionNpaOnFix)

        mpActionNpaOverheadingNavaid = QAction(self)
        mpActionNpaOverheadingNavaid.setObjectName("mpActionNpaOverheadingNavaid")
        mpActionNpaOverheadingNavaid.setToolTip(SurfaceTypes.NpaOverheadingNavaid)
        mpActionNpaOverheadingNavaid.setText(SurfaceTypes.NpaOverheadingNavaid)
        self.connect(mpActionNpaOverheadingNavaid, SIGNAL("triggered()"), self.NpaOverheadingNavaidDlgShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionNpaOverheadingNavaid)

        mpActionNpaAtDistanceTime = QAction(self)
        mpActionNpaAtDistanceTime.setObjectName("mpActionNpaAtDistanceTime")
        mpActionNpaAtDistanceTime.setToolTip(SurfaceTypes.NpaAtDistanceTime)
        mpActionNpaAtDistanceTime.setText(SurfaceTypes.NpaAtDistanceTime)
        self.connect(mpActionNpaAtDistanceTime, SIGNAL("triggered()"), self.NpaAtDistanceTimeDlgShow)
        mnuPANSOPSToolsDAMAPtPositionAndCalculationOfSOC.addAction(mpActionNpaAtDistanceTime)

        self.btnDAMAPtPositionAndCalculationOfSOC = QToolButton()
        self.btnDAMAPtPositionAndCalculationOfSOC.setPopupMode(QToolButton.InstantPopup)
        mnuDAMAPtPositionAndCalculationOfSOC = QMenu()
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionPaIls)
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionPaGbas)
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionBARO_VNAV)
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionSBAS)
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionNpaOnFix)
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionNpaOverheadingNavaid)
        mnuDAMAPtPositionAndCalculationOfSOC.addAction(mpActionNpaAtDistanceTime)

        #Add mnuDAMAPtPositionAndCalculationOfSOC within toolbar
        self.btnDAMAPtPositionAndCalculationOfSOC.setMenu(mnuDAMAPtPositionAndCalculationOfSOC)
        self.btnDAMAPtPositionAndCalculationOfSOC.setToolTip("DA/MAPt Position & Calculation of SOC")
        self.btnDAMAPtPositionAndCalculationOfSOC.setIcon(QIcon(self.currentDir + "/Resource/RaceTrackCmd.bmp"))
        self.toolbarFlightPlannerPansOpsToolsAction.addWidget(self.btnDAMAPtPositionAndCalculationOfSOC)

    def PaIlsDlgShow(self):
        dlg = PaIlsDlg(self, SurfaceTypes.PaIls)
        dlg.show()

    def PaGbasDlgShow(self):
        dlg = PaIlsDlg(self, SurfaceTypes.PaGbas)
        dlg.show()

    def BARO_VNAVShow(self):
        dlg = PaIlsDlg(self, SurfaceTypes.BARO_VNAV)
        dlg.show()

    def SBASShow(self):
        dlg = PaIlsDlg(self, SurfaceTypes.SBAS)
        dlg.show()

    def NpaOnFixDlgShow(self):
        dlg = NpaOnFixDlg(self, "NpaOnFix")
        dlg.show()

    def NpaOverheadingNavaidDlgShow(self):
        dlg = NpaOnFixDlg(self, "NpaOverheadingNavaid")
        dlg.show()

    def NpaAtDistanceTimeDlgShow(self):
        dlg = NpaAtDistanceTimeDlg(self)
        dlg.show()

    def mpActionRaceTrackNavAid_Func(self):
        dlg = RaceTrackDlg(self, "NavAid")
        dlg.show()

    def mpActionRaceTrackFix_Func(self):
        dlg = RaceTrackDlg(self, "Fix")
        dlg.show()

    def addObstacleRasterLayer(self):
        filePathDirs = QFileDialog.getOpenFileNames(self, "Open Obstacle Raster File", QCoreApplication.applicationDirPath(), "Obstacle Raster Files(*.dem *.tif)")

        if len(filePathDirs) == 0:
            return

        layerList =[]

        for filePathDir in filePathDirs:            
            filePathDirInfo= QFileInfo(filePathDir)
            m = filePathDirInfo.fileName()
            rasterLayer = QgsRasterLayer(filePathDir, m, "gdal")

            if rasterLayer.crs() is None:
                rasterLayer.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))

            rasterBandStats = rasterLayer.dataProvider().bandStatistics(1, QgsRasterBandStats.Min | QgsRasterBandStats.Max)
            myMin = rasterBandStats.minimumValue
            myMax = rasterBandStats.maximumValue
            val = (myMax - myMin) / 6
            rasterShader = QgsRasterShader()
            colorRampShader = QgsColorRampShader()
            colorRampShader.setClip(False)

            # iterate through mColormapTreeWidget and set colormap info of layer
            colorRampItems = []

            newColorRampItem = QgsColorRampShader.ColorRampItem()
            newColorRampItem.value = myMin + val
            newColorRampItem.color = QColor(255, 245, 240)
            newColorRampItem.label = QString(str(int(myMin + val)))
            colorRampItems.append(newColorRampItem)

            newColorRampItem1 = QgsColorRampShader.ColorRampItem()
            newColorRampItem1.value = myMin + val * 2
            newColorRampItem1.color = QColor(252, 189, 164)
            newColorRampItem1.label = QString(str(int(myMin + val * 2)))
            colorRampItems.append(newColorRampItem1)

            newColorRampItem2 = QgsColorRampShader.ColorRampItem()
            newColorRampItem2.value = myMin + val * 3
            newColorRampItem2.color = QColor(251, 112, 80)
            newColorRampItem2.label = QString(str(int(myMin + val * 3)))
            colorRampItems.append(newColorRampItem2)

            newColorRampItem3 = QgsColorRampShader.ColorRampItem()
            newColorRampItem3.value = myMin + val * 4
            newColorRampItem3.color = QColor(211, 32, 32)
            newColorRampItem3.label = QString(str(int(myMin + val * 4)))
            colorRampItems.append(newColorRampItem3)

            newColorRampItem4 = QgsColorRampShader.ColorRampItem()
            newColorRampItem4.value = myMax
            newColorRampItem4.color = QColor(103, 0, 13)
            newColorRampItem4.label = QString(str(int(myMax)))
            colorRampItems.append(newColorRampItem4)

            colorRampShader.setColorRampItemList(colorRampItems)
            colorRampShader.setColorRampType(QgsColorRampShader.INTERPOLATED)

            rasterShader.setRasterShaderFunction(colorRampShader)

            bandNumber = 1
            renderer = QgsSingleBandPseudoColorRenderer(rasterLayer.dataProvider(), bandNumber, rasterShader)

            renderer.setClassificationMin(myMin)
            renderer.setClassificationMax(myMax)

            rasterLayer.setRenderer(renderer)

            layerList.append(rasterLayer)

        QgisHelper.appendToCanvas(define._canvas, layerList, SurfaceTypes.DEM)
        self.canvas.zoomToFullExtent()

    def setSelectByRectTool(self):
        self.canvas.setMapTool(self.toolSelectByRect)

    def setSelectByPolygonTool(self):
        self.canvas.setMapTool(self.toolSelectByPolygon)

    def setSelectByFreehandTool(self):
        self.canvas.setMapTool(self.toolSelectByFreehand)

    def setSelectByRadiusTool(self):
        self.canvas.setMapTool(self.toolSelectByRadius)

    def addLine(self):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        lineCreateTool = LineCreateTool(define._canvas)
        self.canvas.setMapTool(lineCreateTool)
        QObject.connect(lineCreateTool, SIGNAL("resultLineCreate"), self.resultLineCreate)

    def resultLineCreate(self, geom):
        if define._userLayers is None:
            constructionLayer = AcadHelper.createVectorLayer("Lines")
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, geom.asPolyline())

            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(constructionLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.Line
            palSetting.placementFlags = QgsPalLayerSettings.AboveLine
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
            palSetting.writeToLayer(constructionLayer)
            QgisHelper.appendToCanvas(define._canvas,[constructionLayer], "Users layer")
            define._userLayers = constructionLayer
        else:
            constructionLayer = define._userLayers

            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, geom.asPolyline())

            palSetting = QgsPalLayerSettings()
            palSetting.readFromLayer(constructionLayer)
            palSetting.enabled = True
            palSetting.fieldName = "Caption"
            palSetting.isExpression = True
            palSetting.placement = QgsPalLayerSettings.Line
            palSetting.placementFlags = QgsPalLayerSettings.AboveLine
            palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
            palSetting.writeToLayer(constructionLayer)
            define._userLayers = constructionLayer
            self.canvas.refresh()

    def mouseMoveHandler(self, point):
        statusBar = self.statusBar()

        if define._mapCrs is None:
            if self.canvas.mapUnits() == QGis.DecimalDegrees:
                unitString = "DecimalDegrees"
            else:
                unitString = "Meters"
        else:
            if define._mapCrs.mapUnits() == QGis.DecimalDegrees:
                unitString = "DecimalDegrees"
            else:
                unitString = "Meters"

        statusBar.showMessage("\tX:\t" + str(point.x()) + "\t\tY:\t" + str(point.y()) + "\t\t\tUnit:\t" + unitString)

    def baroVnavSurfaces(self):
        dlg = BaroVNAVDlg(self)
        dlg.show()

    def addObstacleLayer(self):
        dlg = AddObstacleLayerDlg(self,self.canvas)
        dlg.exec_()

    def measureTool(self):
        dlg = AddMeasureToolDlg(self,self.canvas)
        dlg.show()
        
    def measureAngleTool(self):
        dlg = AddMeasureAngleToolDlg(self, self.canvas)
        dlg.show()
        
    def fullExtent(self):
       self.canvas.zoomToFullExtent()

    def zoomIn(self):
       self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
       self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
       self.canvas.setMapTool(self.toolPan)
        
    def AddVectorLayer(self):
        settings = QSettings()

        lastusedir = settings.value("/UI/lastVectorFileFilterDir", QDir.homePath()).toString()

        filenames = QFileDialog.getOpenFileNames(self, "Open ESRI Shapefiles", lastusedir, "ESRI Shapefiles(*.shp *.SHP)")

        # filenames 's type is QStringList

        if filenames.__len__() == 0:
            return

        layerList =[]
      
        for file in filenames:           
            filePathDirInfo = QFileInfo(file)
            m = filePathDirInfo.fileName()

            layer = QgsVectorLayer(file, m, "ogr")

            crs = layer.crs()

            if crs is None:
                layer.setCrs(QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId))

            layerList.append(layer)

        QgisHelper.appendToCanvas(define._canvas, layerList)
        self.canvas.zoomToFullExtent()

        # Save last used directory

        firstfilename = filenames.first()
        fi = QFileInfo(firstfilename)
        path = fi.path()
        settings.setValue("/UI/lastVectorFileFilterDir", path)

    def setMapUnits(self, unit):
        if unit == QGis.DecimalDegrees:
            latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        elif unit == QGis.Meters: # WGS 84 / UTM zone 60N
            meterCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
            latCrs = meterCrs

        define._units = unit
        myRenderer = self.canvas.mapRenderer()
        self.canvas.freeze()
        myRenderer.setProjectionsEnabled(True)
        myRenderer.setDestinationCrs(latCrs)
        myRenderer.setMapUnits(unit)
        self.canvas.freeze(False)
        self.canvas.refresh()
        self.canvas.zoomToFullExtent()
        QgisHelper.convertMeasureUnits(unit)
        self.emit(SIGNAL("mapUnitChanged()"))
        
    def setMapUnitsDegree(self):
        self.setMapUnits(QGis.DecimalDegrees)
        define._units = QGis.DecimalDegrees
        self.actionMapunitsMeter.setChecked(False)
        self.actionMapunitsDegree.setChecked(True)

    def setMapUnitsMeter(self):
        self.setMapUnits(QGis.Meters)
        define._units = QGis.Meters
        self.actionMapunitsMeter.setChecked(True)
        self.actionMapunitsDegree.setChecked(False)

    def settingProj(self):
        mySelector = QgsGenericProjectionSelector(self)

        if mySelector.exec_() != QDialog.Accepted:
            return

        crs = QgsCoordinateReferenceSystem(mySelector.selectedCrsId(), QgsCoordinateReferenceSystem.InternalCrsId)
        self.setProjectOfCanvas(define._canvas, crs)

    def setProjectOfCanvas(self, canvas, crs):
        unit = crs.mapUnits()

        define._units = unit
        define._mapCrs = crs
        myRenderer =self.canvas.mapRenderer()
        self.canvas.freeze()
        myRenderer.setProjectionsEnabled(True)
        myRenderer.setDestinationCrs(crs)
        myRenderer.setMapUnits(unit)
        canvas.freeze(False)
        canvas.refresh()
        canvas.zoomToFullExtent()
        
        QgisHelper.convertMeasureUnits(unit)

        authID = crs.authid()

        define._crsLabel.setText(authID)

        if unit == QGis.Meters:
            define._xyCrs = crs
            self.tabBar.setCurrentIndex(0)
            define._mapCrs = crs
        elif unit == QGis.Degrees:
            define._latLonCrs = crs
            self.tabBar.setCurrentIndex(1)
            define._mapCrs = crs
        
        self.emit(SIGNAL("mapUnitChanged()"))

    def setTrees(self):
        if self.actionTrees.isChecked():
            trees, dlgResult = QtGui.QInputDialog.getDouble(self, "Input vertical tolerance value", "Vertical Tolerance Value", 30.0)
            if dlgResult:
                define._trees = trees
            else:
                self.actionTrees.setChecked(False)
        else:
            define._trees = 0.0

    def setTreesDEM(self):
        if self.actionTreesDEM.isChecked():
            trees, dlgResult = QtGui.QInputDialog.getDouble(self, "Input vertical tolerance value(DEM)", "Vertical Tolerance Value(DEM)", 30.0)
            if dlgResult:
                define._treesDEM = trees
            else:
                self.actionTreesDEM.setChecked(False)
        else:
            define._treesDEM = 0.0

    def fileMenuPrintActionEvent(self):
        pass

    def fileMenuExitActionEvent(self):
        self.close()

    def userLogin(self):
        loginForm = LoginForm(self)
        result = loginForm.exec_()

        if result == QDialog.Accepted:
            userTypeStr = ""

            for case in switch(AirCraftOperation.loginedUser.Right):
                if case(enumUserRight.ur_Admin):
                    userTypeStr = "Administrator"
                elif case(enumUserRight.ur_SuperUser):
                    userTypeStr = "Super User"
                elif case(enumUserRight.ur_ReadWrite):
                    userTypeStr = "Read/Write user"
                else:
                    userTypeStr = "Read Only user"

            QMessageBox.warning(self, "Information", "You have successfully logged in as the " + userTypeStr + ".")
            self.ResetProject()

    def ResetProject(self):
        loginedRole = AirCraftOperation.loginedUser.Right

        for case in switch (loginedRole):
            if case(enumUserRight.ur_Admin):
                self.procedureMenuUserManagementAction.setEnabled(True)
                self.createProcedureToolStripMenuItem.setEnabled(True)
            elif case(enumUserRight.ur_SuperUser):
                self.procedureMenuUserManagementAction.setEnabled(False)
                self.createProcedureToolStripMenuItem.setEnabled(True)
                break
            elif case(enumUserRight.ur_ReadWrite):
                self.procedureMenuUserManagementAction.setEnabled(False)
                self.createProcedureToolStripMenuItem.setEnabled(False)
                break
            elif case(enumUserRight.ur_ReadOnly):
                self.procedureMenuUserManagementAction.setEnabled(False)
                self.createProcedureToolStripMenuItem.setEnabled(False)
                break

    def userManagement(self):
        userMngForm = UserMngForm(self)
        result = userMngForm.exec_()

    def isLogin(self):
        if AirCraftOperation.loginedUser is None:
            QMessageBox.warning(self, "Warning", "Please login as a valid user!")
            return False
        else:
            return True

    def projectToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        projectMngForm = ProjectMngForm(self)
        projectMngForm.exec_()

    def subprojectToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        subprojectMngForm = SubProjectMngForm(self)
        subprojectMngForm.exec_()

    def workspaceToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        workspaceMngForm = WorkspaceMngForm(self)
        workspaceMngForm.exec_()

    def procedureFileToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        procedureMngForm = ProcedureMngForm(self)
        procedureMngForm.exec_()

    def selectProjectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select project directory", define.projectManageDir)

        if folder is not None and folder != "":
            define.projectManageDir = folder

            if AirCraftOperation.ApplicationSetting.ProjectFolderPath == folder:
                return

            AirCraftOperation.SelectProjectFolder(folder)
            self.setWindowTitle("FlightPlanner(" + folder.replace("\\", "/") + ")")

    def registerProjectFolder(self):
        regProjectFolderForm = RegProjectFolderForm(self)
        regProjectFolderForm.exec_()

    def registerAIPChartToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        aipChartMngForm = AIPChartMngForm(self)
        aipChartMngForm.exec_()

    def createProcedureToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        procedureForm = SelectProcedureForm(self)
        procedureForm.setWindowTitle("Create Procedure")
        result = procedureForm.exec_()

        if result:
            try:
                define.obstaclePath = AirCraftOperation.currentProcedure.Path
                self.toolbarFlightPlannerImportExportToolsAction.setEnabled(True)
                self.toolbarFlightPlannerOlsSurfaces.setEnabled(True)
                self.toolbarFlightPlannerConventionalApproachToolsAction.setEnabled(True)
                self.toolbarFlightPlannerConventionalDepartureToolsAction.setEnabled(True)
                self.toolbarFlightPlannerConventionalEnrouteToolsAction.setEnabled(True)
                self.toolbarFlightPlannerPBNToolsAction.setEnabled(True)
                self.toolbarFlightPlannerPansOpsToolsAction.setEnabled(True)
                self.toolbarFlightPlannerChartingToolsAction.setEnabled(True)
                self.qad.toolBar.setEnabled(True)
                self.qad.dimToolBar.setEnabled(True)

                self.setWindowTitle("FlightPlanner(" + AirCraftOperation.currentAIP.Path.replace("\\", "/") + ")")

                QgsProject.instance().read(QFileInfo(AirCraftOperation.currentAIP.Path))
                self.saveFlag = False
            except:
                pass

    def openProcedureToolStripMenuItem_Click(self):
        if not self.isLogin():
            return

        procedureForm = SelectProcedureForm(self)
        result = procedureForm.exec_()

        if result:
            try:
                define.obstaclePath = AirCraftOperation.currentProcedure.Path
                self.toolbarFlightPlannerImportExportToolsAction.setEnabled(True)
                self.toolbarFlightPlannerOlsSurfaces.setEnabled(True)
                self.toolbarFlightPlannerConventionalApproachToolsAction.setEnabled(True)
                self.toolbarFlightPlannerConventionalDepartureToolsAction.setEnabled(True)
                self.toolbarFlightPlannerConventionalEnrouteToolsAction.setEnabled(True)
                self.toolbarFlightPlannerPBNToolsAction.setEnabled(True)
                self.toolbarFlightPlannerPansOpsToolsAction.setEnabled(True)
                self.toolbarFlightPlannerChartingToolsAction.setEnabled(True)
                self.qad.toolBar.setEnabled(True)
                self.qad.dimToolBar.setEnabled(True)

                self.setWindowTitle("FlightPlanner(" + AirCraftOperation.currentAIP.Path.replace("\\", "/") + ")")

                QgsProject.instance().read(QFileInfo(AirCraftOperation.currentAIP.Path))
                self.saveFlag = False
            except:
                pass

    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        fileMenuOpenAction = QgisHelper.createAction(self, "Open...", self.openProj, None, "opens", None, False)
        fileMenu.addAction(fileMenuOpenAction)

        fileMenuSaveAction = QgisHelper.createAction(self, "Save...", self.saveProj, None, "saves", None, False)
        fileMenu.addAction(fileMenuSaveAction)

        fileMenuSaveAsAction = QgisHelper.createAction(self, "Save As...", self.saveAsProj, None, "saveass", None, False)
        fileMenu.addAction(fileMenuSaveAsAction)

        fileMenuPrintAction = QgisHelper.createAction(self, "Print...", self.fileMenuPrintActionEvent, None, "prints", None, False)
        fileMenu.addAction(fileMenuPrintAction)

        fileMenuExitAction = QgisHelper.createAction(self, "Exit", self.fileMenuExitActionEvent, None, "closes", None, False)
        fileMenu.addAction(fileMenuExitAction)

        # Procedure Manager menu
        procedureMenu = menuBar.addMenu("&Procedure Manager")

        # create "Project Folder" sub menu.
        procedureMenuProjectFolderMenu = procedureMenu.addMenu("Project Folder")

        projectFolderMenuOpenAction = QgisHelper.createAction(self, "Select Project Folder...", self.selectProjectFolder, None, "Select Project Folder", None, False)
        procedureMenuProjectFolderMenu.addAction(projectFolderMenuOpenAction)

        projectFolderMenuRecentAction = QgisHelper.createAction(self, "Recent Project Folder", self.selectProjectFolder, None, "Recent Project Folders", None, False)
        procedureMenuProjectFolderMenu.addAction(projectFolderMenuRecentAction)

        projectFolderMenuRegisterAction = QgisHelper.createAction(self, "Register Project Folder...", self.registerProjectFolder, None, "Register Project Folder", None, False)
        procedureMenuProjectFolderMenu.addAction(projectFolderMenuRegisterAction)

        procedureMenuUserManagementMenu = procedureMenu.addMenu("User")
        procedureMenuUserLodinAction = QgisHelper.createAction(self, "Login", self.userLogin, None, "Login", None, False)
        procedureMenuUserManagementMenu.addAction(procedureMenuUserLodinAction)
        self.procedureMenuUserManagementAction = QgisHelper.createAction(self, "User Management", self.userManagement, None, "User Management", None, False)
        procedureMenuUserManagementMenu.addAction(self.procedureMenuUserManagementAction)

        registerAIPChartToolStripMenuItem = QgisHelper.createAction(self, "Register AIP Chart", self.registerAIPChartToolStripMenuItem_Click, None, "Register AIP Chart", None, False)
        procedureMenu.addAction(registerAIPChartToolStripMenuItem)

        projectToolStripMenuItem = QgisHelper.createAction(self, "Project", self.projectToolStripMenuItem_Click, None, "project", None, False)
        procedureMenu.addAction(projectToolStripMenuItem)

        subprojectToolStripMenuItem = QgisHelper.createAction(self, "Sub-Project", self.subprojectToolStripMenuItem_Click, None, "sub project", None, False)
        procedureMenu.addAction(subprojectToolStripMenuItem)

        workspaceToolStripMenuItem = QgisHelper.createAction(self, "Workspace", self.workspaceToolStripMenuItem_Click, None, "workspace", None, False)
        procedureMenu.addAction(workspaceToolStripMenuItem)

        procedureFileToolStripMenuItem = QgisHelper.createAction(self, "Procedure File", self.procedureFileToolStripMenuItem_Click, None, "procedure file", None, False)
        procedureMenu.addAction(procedureFileToolStripMenuItem)

        self.createProcedureToolStripMenuItem = QgisHelper.createAction(self, "Create Procedure", self.createProcedureToolStripMenuItem_Click, None, "Create Procedure", None, False)
        procedureMenu.addAction(self.createProcedureToolStripMenuItem)

        openProcedureToolStripMenuItem = QgisHelper.createAction(self, "Open Procedure", self.openProcedureToolStripMenuItem_Click, None, "Open Procedure", None, False)
        procedureMenu.addAction(openProcedureToolStripMenuItem)

        self.viewMenu = menuBar.addMenu("&View")
        optionsMenu = menuBar.addMenu("&Options")   
        self.setProject = QgisHelper.createAction(self, "Set Projection", self.settingProj, None, None, None, False)
        optionsMenu.addAction(self.setProject)

        self.actionMapunitsDegree = QgisHelper.createAction(self, "DecimalDegrees", self.setMapUnitsDegree, None, None, None, True)
        self.actionMapunitsMeter = QgisHelper.createAction(self, "Meters", self.setMapUnitsMeter, None, None, None, True)
        self.actionMapunitsDegree.setChecked(True)

        self.actionTrees = QgisHelper.createAction(self, "Obstacle Vertical Tolerance", self.setTrees, None, None, None, True)
        optionsMenu.addAction(self.actionTrees)
        
        self.actionTolerance = QgisHelper.createAction(self, "Obstacle Horizental Tolerance", self.setTolerance, None, None, None, True)
        optionsMenu.addAction(self.actionTolerance)
        
        self.actionTreesDEM = QgisHelper.createAction(self, "DEM Vertical Tolerance", self.setTreesDEM, None, None, None, True)
        optionsMenu.addAction(self.actionTreesDEM)
        
        self.actionToleranceDEM = QgisHelper.createAction(self, "DEM Horizental Tolerance", self.setToleranceDEM, None, None, None, True)
        optionsMenu.addAction(self.actionToleranceDEM)

        self.actionNumberSavingObstacles = QgisHelper.createAction(self, "Number of saving obstacles/dem points", self.setNumberSavingObstacles, None, None, None, True)
        optionsMenu.addAction(self.actionNumberSavingObstacles)
    
        self.actionSnapping = QgisHelper.createAction(self, "Snapping", self.setSnapping, None, None, None, True)
        self.actionSnapping.setChecked(True)
        optionsMenu.addAction(self.actionSnapping)

        crcMenu = menuBar.addMenu("&CRC")
        self.actionCrcReader = QgisHelper.createAction(self, "CRC Reader", self.crcReaderFunc, None, None, None, True)
        self.actionCrcReader.setCheckable(False)
        crcMenu.addAction(self.actionCrcReader)

        self.actionCrcWriter = QgisHelper.createAction(self, "CRC Writer", self.crcWriterFunc, None, None, None, True)
        self.actionCrcWriter.setCheckable(False)
        crcMenu.addAction(self.actionCrcWriter)

        qaWndMenu = menuBar.addAction("&QaWindow")
        qaWndMenu.triggered.connect(self.qaWndMenuTriggered)

    def qaWndMenuTriggered(self):
        self.qaWnd = QaWindow(self)
        self.qaWnd.show()

    def crcReaderFunc(self):
        dlg = DlgCrcReadWrite(self, "r")
        dlg.exec_()

    def crcWriterFunc(self):
        dlg = DlgCrcReadWrite(self, "w")
        dlg.exec_()

    def setNumberSavingObstacles(self):
        numberSavingObstacles, dlgResult = QtGui.QInputDialog.getInt(self, "Input number of saving obstacles/dem points", "Number of saving obstacles/dem points", 30)
        if dlgResult:
            define._numberSavingObstacles = numberSavingObstacles

    def setTolerance(self):
        if self.actionTolerance.isChecked():
            tolerance, dlgResult = QtGui.QInputDialog.getDouble(self, "Input horizental tolerance value", "Horizental Tolerance Value", 20.0)
            if dlgResult:
                define._tolerance = tolerance
            else:
                self.actionTolerance.setChecked(False)
        else:
            define._tolerance = 0.0

    def setToleranceDEM(self):
        if self.actionToleranceDEM.isChecked():
            tolerance, dlgResult = QtGui.QInputDialog.getDouble(self, "Input horizental tolerance value(DEM)", "Horizental Tolerance Value(DEM)", 20.0)
            if dlgResult:
                define._toleranceDEM = tolerance
            else:
                self.actionToleranceDEM.setChecked(False)
        else:
            define._toleranceDEM = 0.0

    def setSnapping(self):
        if self.actionSnapping.isChecked():
            define._snapping = True
            qgsProject = QgsProject.instance()
            for layer in self.canvas.layers():
                if not isinstance(layer, QgsVectorLayer):
                    continue
                qgsProject.setSnapSettingsForLayer(layer.id(), True, QgsSnapper.SnapToVertexAndSegment\
                                                   , QgsTolerance.Pixels, 10, False)
        else:
            define._snapping = False

    def createOverview(self):
        canvasOverview = QgsMapOverviewCanvas(None, self.canvas)
        canvasOverview.setWhatsThis("Map overview canvas. This canvas can be used to display a locator map that shows the current extent of the map canvas. The current extent is shown as a red rectangle. Any layer on the map can be added to the overview canvas.")

        mOverviewMapCursor = QCursor(QPixmap("Resource/mActionPan.png"))
        canvasOverview.setCursor(mOverviewMapCursor)
        
        mOverviewDock = QDockWidget("Overview", self)
        mOverviewDock.setObjectName("Overview")
        mOverviewDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        mOverviewDock.setWidget(canvasOverview)
        self.addDockWidget(Qt.LeftDockWidgetArea, mOverviewDock)

        # add to the Panel submenu
        self.viewMenu.addAction(mOverviewDock.toggleViewAction())
        self.canvas.enableOverviewMode(canvasOverview)
        # moved here to set anti aliasing to both map canvas and overview
        mySettings = QSettings()

        #Anti Aliasing enabled by default as of QGIS 1.7
        self.canvas.enableAntiAliasing(mySettings.value("/qgis/enable_anti_aliasing", True).toBool())
        action = mySettings.value("/qgis/wheel_action", 2).toInt()
        zoomFactor = mySettings.value("/qgis/zoom_factor", 1.5).toDouble()
        self.canvas.setWheelAction(QgsMapCanvas.WheelZoomToMouseCursor, zoomFactor[0])
        self.canvas.setCachingEnabled(mySettings.value("/qgis/enable_render_caching", True).toBool())
        self.canvas.setParallelRenderingEnabled(mySettings.value("/qgis/parallel_rendering", False).toBool())
        k = mySettings.value("/qgis/map_update_interval", 250).toInt()
        self.canvas.setMapUpdateInterval(k[0])
        mOverviewDock.hide()

    def layerTreeView(self):
        return self._mLayerTreeView

    def layers(self):
        layertreelayerlist = self._mLayerTreeView.layerTreeModel().rootGroup().findLayers()

        layerlist = []

        for layertreelayer in layertreelayerlist:
            if layertreelayer.layer() is not None:
                layerlist.append(layertreelayer.layer())

        return layerlist

    def initLayerTreeView(self):
        mLegend = QDockWidget("Layers", self)

        mLegend.setObjectName("Layers")
        mLegend.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._mLayerTreeView = QgsLayerTreeView(mLegend)
        define._mLayerTreeView = self._mLayerTreeView
        self._mLayerTreeView.setObjectName("theLayerTreeView")
        
        model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        model.setAutoCollapseSymbologyNodes(10)
        
        self._mLayerTreeView.setModel(model)
        self._mLayerTreeView.setMenuProvider(QgsAppLayerTreeViewMenuProvider(self._mLayerTreeView))
        self.setupLayerTreeViewFromSettings()

        self._mLayerTreeView.selectionModel().selectionChanged.connect(self.legendLayerSelectionChanged)
        self._mLayerTreeView.layerTreeModel().rootGroup().addedChildren.connect(self.markDirty)
        self._mLayerTreeView.layerTreeModel().rootGroup().addedChildren.connect(self.updateNewLayerInsertionPoint)
        self._mLayerTreeView.layerTreeModel().rootGroup().removedChildren.connect(self.markDirty)
        self._mLayerTreeView.layerTreeModel().rootGroup().removedChildren.connect(self.updateNewLayerInsertionPoint)
        self._mLayerTreeView.layerTreeModel().rootGroup().visibilityChanged.connect(self.markDirty)
        self._mLayerTreeView.layerTreeModel().rootGroup().customPropertyChanged.connect(self.markDirty)

        self._mLayerTreeView.currentLayerChanged.connect(self.activeLayerChanged)
        self._mLayerTreeView.selectionModel().currentChanged.connect(self.updateNewLayerInsertionPoint)

        vboxLayout = QVBoxLayout()
        vboxLayout.setMargin(0)
        vboxLayout.addWidget(self._mLayerTreeView)
        w = QWidget(mLegend)
        w.setLayout(vboxLayout)
        mLegend.setWidget(w)

        self.addDockWidget(Qt.LeftDockWidgetArea, mLegend)

        mLayerTreeCanvasBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.canvas, self)

        otfTransformAutoEnable = QSettings().value("/Projections/otfTransformAutoEnable", True).toBool()
        mLayerTreeCanvasBridge.setAutoEnableCrsTransform(otfTransformAutoEnable)

        self.viewMenu.addAction(mLegend.toggleViewAction())

    def setupLayerTreeViewFromSettings(self):
        st = QSettings()
        
        model = self._mLayerTreeView.layerTreeModel()

        fontLayer = QFont()
        fontGroup = QFont()
        fontLayer.setBold(st.value("/qgis/legendLayersBold", True).toBool())
        fontGroup.setBold(st.value("/qgis/legendGroupsBold", False).toBool())
        model.setLayerTreeNodeFont(QgsLayerTreeNode.NodeLayer, fontLayer)
        model.setLayerTreeNodeFont(QgsLayerTreeNode.NodeGroup, fontGroup)

    def activeLayerChanged(self, layer):        
        self.canvas.setCurrentLayer(layer)

    def updateNewLayerInsertionPoint(self):
        parentGroup = self._mLayerTreeView.layerTreeModel().rootGroup()
        index = 0
        current = self._mLayerTreeView.currentIndex()
        
        if current.isValid():
            currentNode = self._mLayerTreeView.currentNode()

            if currentNode is not None:
                if QgsLayerTree.isGroup(currentNode):
                    QgsProject.instance().layerTreeRegistryBridge().setLayerInsertionPoint(currentNode, 0)
                    return        
                    #otherwise just set the insertion point in front of the current node
                parentNode = currentNode.parent()

            index = current.row()        
        QgsProject.instance().layerTreeRegistryBridge().setLayerInsertionPoint(parentGroup, index)

    def legendLayerSelectionChanged(self):
        selectedLayers = self._mLayerTreeView.selectedLayerNodes()

        if len(selectedLayers) > 0:
            self.mActionRemoveLayer.setEnabled(True)
        else:
            self.mActionRemoveLayer.setEnabled(False)

    def removeLayer(self):
        if self._mLayerTreeView is None:
            return

        selectedNodes = self._mLayerTreeView.selectedNodes(True)

        if selectedNodes.isEmpty():
            return

        if QMessageBox.warning(self, "Remove layers and groups", "Remove %i legend entries?"%selectedNodes.count(), QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel:
            return      
    
        for node in selectedNodes:
            parentGroup = node.parent()

            if parentGroup is not None:
                parentGroup.removeChildNode(node)

        self.canvas.refresh()
        
        for layer in define._surfaceLayers:
            try:
                QgsMapLayerRegistry.instance().mapLayer(layer.id())
            except RuntimeError:
                define._surfaceLayers.pop(define._surfaceLayers.index(layer))
        for layer in define._obstacleLayers:
            try:
                QgsMapLayerRegistry.instance().mapLayer(layer.id())
            except RuntimeError:
                define._obstacleLayers.pop(define._obstacleLayers.index(layer))

    def markDirty(self):
        QgsProject.instance().dirty(True)

    def layersChanged(self):
        layer = self.canvas.currentLayer()

        if isinstance(layer, QgsPluginLayer):
            return

        if layer is not None:
            if not layer.isEditable():
                self.mpActionToggleEditing.setChecked(False)
            else:
                self.mpActionToggleEditing.setChecked(True)
            self.toggleEditingFunc()

        pass

    def basicGNSS(self):
        dlg = basicGNSSDlg(self)
        dlg.setWindowTitle("NON-Precision with T- or Y-Bar")           
        dlg.show()

    def approachAlignment(self):
        dlg = ApproachACDlg(self)
        dlg.setWindowTitle("Approach Alignment")           
        dlg.show()

    def geoDetermineDlgShow(self):
        dlg = GeoDetermineDlg(self)
        dlg.show()

    def IlsOsa(self):
        dlg = OasDlg(self)
        dlg.show()

    def IlsOsaSbas(self):
        dlg = OasDlg(self, "SBAS")
        dlg.show()
        
    def IlsBasicShow(self):
        dlg = IlsBasicDlg(self)
        dlg.show()
        
    def IasToTasShow(self):
        dlg = IasToTasDlg(self)
        dlg.show()
        
    def RnpAr(self):
        dlgRnpAR = RnpARDlg(self)
        dlgRnpAR.show()
        
    def PathTerminatorsShow(self):
        dlg = PathTerminatorsDlg(self)
        dlg.show()

    def HoldingShow(self):
        dlg = RaceTrackDlg(self, "Holding")
        dlg.show()

    def ChartingGridDlgShow(self):
        dlg = ChartingGridDlg(self)
        dlg.show()

    def ChartingTemplatesDlgShow(self):
        dlg = ChartingTemplatesDlg(self)
        dlg.show()

    def FasDataBlockShow(self):
        dlg = FasDataBlockDlg(self)
        dlg.show()

    def ProcedureExportShow(self):
        dlg = ProcedureExportDlg(self)
        dlg.show()

    def ProfileManagerShow(self):
        dlg = ProfileManagerDlg(self)
        dlg.show()

    def DataExportShow(self):
        dlg = DataExportDlg(self)
        dlg.show()

    def PinSVisualSegmentDep(self):
        dlg = PinSVisualSegmentDepDlg(self)
        dlg.show()

    def PinSVisualSegmentApp(self):
        dlg = PinSVisualSegmentAppDlg(self)
        dlg.show()

    def VisualSegmentSurface(self):
        dlg = VisualSegmentSurfaceDlg(self)
        dlg.show()

    def TaaShow(self):
        dlg = TaaCalculationDlg(self)
        dlg.show()

    def ObstacleEvaluatorShow(self):
        dlg = ObstacleEvaluatorDlg(self)
        dlg.show()

    def DmeToleranceShow(self):
        dlg = DmeToleranceDlg(self)
        dlg.show()

    def HoldingRnpDlgShow(self):
        dlg = HoldingRnpDlg(self)
        dlg.show()

    def RnavVorDmeShow(self):
        dlg = RnavVorDme(self)
        dlg.show()

    def RnavDmeDmeShow(self):
        dlg = RnavDmeDme(self)
        dlg.show()

    def aerodromeSurfacesShow(self):
        dlg = AerodromeSurfacesDlg(self)
        dlg.show()

    def shieldingShow(self):
        dlg = ShieldingDlg(self)
        dlg.show()

    def heliportSurfacesShow(self):
        dlg = HeliportSurfacesDlg(self)
        dlg.show()

    def BaseTurnTC(self):
        dlg = BaseTurnTSDlg(self)
        dlg.show()
        
    def CrmShow(self):
        dlg = CrmDlg(self)
        dlg.show()

    def TurnAreaShow(self):
        dlg = TurnAreaDlg(self)
        dlg.show()
        
    def VisualCirclingShow(self):
        dlg = VisualCirclingDlg(self)
        dlg.show()
        
    def DepartureRnavShow(self):
        dlg = DepartureRnavDlg(self)
        dlg.show()
        
    def DepartureStandardShow(self):
        dlg = DepartureStandardDlg(self)
        dlg.show()
        
    def DepartureNominalShow(self):
        dlg = DepartureNominalDlg(self)
        dlg.show()
        
    def DepartureOmnidirectionalShow(self):
        dlg = DepartureOmnidirectionalDlg(self)
        dlg.show()
        
    def RnavNominalShow(self):
        dlg = RnavNominalDlg(self)
        dlg.show()
        
    def RnavStraightSegmentAnalyserShow(self):
        dlg = RnavStraightSegmentAnalyserDlg(self)
        dlg.show()
        
    def RnavTurningSegmentAnalyserShow(self):
        dlg = RnavTurningSegmentAnalyserDlg(self)
        dlg.show()

    def TurnProtectionAndObstacleAssessmentShow(self):
        dlg = TurnProtectionAndObstacleAssessmentDlg(self)
        dlg.show()

    def DmeUpdateAreaShow(self):
        dlg = RnavDmeUpdateAreaDlg(self)
        dlg.show()

    def HoldingOverHeadDlgShow(self):
        dlg = HoldingOverHeadDlg(self)
        dlg.show()

    def HoldingRnavShow(self):
        dlg = HoldingRnavDlg(self)
        dlg.show()
        
    def HoldingRace_PShow(self):
        dlg = HoldingRace_PDlg(self)
        dlg.show()
        
    def HoldingVorDmeShow(self):
        dlg = HoldingVorDmeDlg(self)
        dlg.show()

    def ApproachSegmentShow(self):
        dlg = ApproachSegmentDlg(self)
        dlg.show()

    def MASegmentShow(self):
        dlg = MASegmentDlg(self)
        dlg.show()
        
    def EnrouteStraightShow(self):
        dlg = EnrouteStraightDlg(self)
        dlg.show()
        
    def RadialShow(self):
        dlg = RadialDlg(self)
        dlg.show()
        
    def FixToleranceAreaShow(self):
        dlg = FixToleranceAreaDlg(self)
        dlg.show()

    def EnrouteTurnOverHeadShow(self):
        dlg = EnrouteTurnOverHeadDlg(self)
        dlg.show()
        
    def MSAShow(self):
        dlg = MSADlg(self)
        dlg.show()
        
    def DataImportShow(self):
        dlg = DataImportDlg(self)
        dlg.show()
        
    def openProj(self):
        filename = QFileDialog.getOpenFileName(self, "Choose a QGIS project file to open",QCoreApplication.applicationDirPath (),"QGIS files(*.qgs *.QGS)")

        if filename == "":
            return

        QgsProject.instance().read(QFileInfo(filename))
        self.saveFlag = False

    def saveProj(self):
        if self.saveFlag:
            self.saveFileName = QFileDialog.getSaveFileName(self, "Choose a file name to save the QGIS project file",QCoreApplication.applicationDirPath (),"QGIS files(*.qgs *.QGS)")
            if self.saveFileName == "":
                return
            QgsProject.instance().write(QFileInfo(self.saveFileName))
            self.saveFlag = False
        else:
            self.saveFileName = QgsProject.instance().fileName()
            QgsProject.instance().write(QFileInfo(QgsProject.instance().fileName()))

    def saveAsProj(self):
        self.saveFileName = QFileDialog.getSaveFileName(self, "Choose a file name to save the QGIS project file",QCoreApplication.applicationDirPath (),"QGIS files(*.qgs *.QGS)")
        if self.saveFileName == "":
            return

        QgsProject.instance().write(QFileInfo(self.saveFileName))

    def toolButtonActionTriggered(self, action): 
        settings = QSettings()

        if action == self.measureAction:
            settings.setValue("/UI/measureTool", 0)
        elif action == self.mActionMeasureAngle:
            settings.setValue("/UI/measureTool", 1)
        self.btnMeasure.setDefaultAction(action)

    def circularStringToolButtonActionTriggered(self, action):
        settings = QSettings()

        if action == self.actionCircularStringPoint:
            settings.setValue("/UI/addCircularTool", 0)
        elif action == self.actionCircularStringRadius:
            settings.setValue("/UI/addCircularTool", 1)
        self.btnCircularString.setDefaultAction(action)
        
    def selectToolButtonActionTriggered(self, action):
        settings = QSettings()

        if action == self.measureAction:
            settings.setValue("/UI/selectTool", 0)
        elif action == self.mActionMeasureAngle:
            settings.setValue("/UI/selectTool", 1)
        elif action == self.mActionMeasureAngle:
            settings.setValue("/UI/selectTool", 2)
        self.btnSelect.setDefaultAction(action)

    def toggleEditing(self):
        currentLayer = self._mLayerTreeView.currentLayer()

        if currentLayer is not None and currentLayer.type() == QgsMapLayer.VectorLayer:
            currentLayer.startEditing()
            self.toggleEditing1(currentLayer, True)
        else:
            self.mpActionToggleEditing.setChecked(False)

    def toggleEditing1(self, layer, allowCancel):
        res = True

        if layer.isEditable() and not layer.isReadOnly():
            if not (layer.dataProvider().capabilities() & QgsVectorDataProvider.EditingCapabilities):
                return False

            layer.startEditing()
            settings = QSettings()
            markerType = settings.value("/qgis/digitizing/marker_style", "Cross").toString()
            markSelectedOnly = settings.value("/qgis/digitizing/marker_only_for_selected", False).toBool()
            
            # redraw only if markers will be drawn
            if (not markSelectedOnly or layer.selectedFeatureCount() > 0) and (markerType == "Cross" or markerType == "SemiTransparentCircle"):
                layer.triggerRepaint()
        elif layer.isModified():
            buttons = QMessageBox.Save | QMessageBox.Discard
            if allowCancel:
                buttons |= QMessageBox.Cancel
                result = QMessageBox.information(0, "Stop editing" ,"Do you want to save the changes to layer %s"%layer.name(),buttons)
                if result == QMessageBox.Cancel:
                    res = False
                elif result == QMessageBox.Save:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    if not layer.commitChanges():
                        res = False
                    layer.triggerRepaint()
                    QApplication.restoreOverrideCursor()
                elif result == QMessageBox.Discard:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    self.canvas.freeze(True)

                    if layer.rollBack():
                        res = False

                    self.canvas.freeze(False)
                    layer.triggerRepaint()
                    QApplication.restoreOverrideCursor()
            else:
                self.canvas.freeze(True)
                layer.rollBack()
                self.canvas.freeze(False)
                res = True
                layer.triggerRepaint()
        return res
    
    def saveActiveLayerEdits(self):
        self.saveEdits(self._mLayerTreeView.currentLayer(), True, True)
    
    def saveEdits(self, layer, leaveEditable, triggerRepaint):
        if layer is None or not layer.isEditable() or not layer.isModified():
            return

        if layer == self._mLayerTreeView.currentLayer():
            mSaveRollbackInProgress = True

        if not layer.commitChanges():
            mSaveRollbackInProgress = False

        if leaveEditable:
            layer.startEditing()

        if triggerRepaint:
            layer.triggerRepaint()

    def cancelEdits(self, layer, leaveEditable, triggerRepaint):
        if layer is None or not layer.isEditable():
            return

        if layer == self._mLayerTreeView.currentLayer() and leaveEditable:
            mSaveRollbackInProgress = True

        self.canvas.freeze(True)
        self.canvas.freeze(False)

        if leaveEditable:
            layer.startEditing()

        if triggerRepaint:
            layer.triggerRepaint()
            
    def userScale(self):
        # To avoid ZeroDivisionError
        if float(self.mScaleEdit.scale()) == 0.0:
            self.canvas.updateScale()
            return

        self.canvas.zoomScale(1.0 / float(self.mScaleEdit.scale()))

    def setScale(self, scale):
        self.mScaleEdit.blockSignals(True)
        self.mScaleEdit.setScale(scale)
        self.mScaleEdit.blockSignals(False)

    def showScale(self, theScale):
        self.setScale(1.0 / float(theScale))
        if self.mScaleEdit.width() > self.mScaleEdit.minimumWidth():
            self.mScaleEdit.setMinimumWidth(self.mScaleEdit.width())
            
    def txtAnnotationTool(self):
        txtAnnoTool = QgsMapToolTextAnnotation(define._canvas)
        self.canvas.setMapTool(txtAnnoTool)

    def deselectAll(self):
        renderFlagState =self.canvas.renderFlag()
        if renderFlagState:
            self.canvas.setRenderFlag(False)
        layers = QgsMapLayerRegistry.instance().mapLayers()
        for it in layers:
            vl = layers[it]
            vl._class_ = QgsVectorLayer()
            if not isinstance(vl, QgsVectorLayer):
                continue
            vl.removeSelection()
            
        # Turn on rendering (if it was on previously)
        if renderFlagState:
            self.canvas.setRenderFlag(True)

    def mapCanvas(self):
        return self.canvas

    def setActiveLayer(self, layer):
        self.canvas.setCurrentLayer(layer)

    def expressionselect(self):
        vlayer = self.canvas.currentLayer()

        if vlayer is None:
            QMessageBox.warning(None, "Information", "Please select layer!")
            return

        vlayer._class_ = QgsVectorLayer()
        if not isinstance(vlayer, QgsVectorLayer):
            define._messagBar.pushMessage("No active vector layer" ,"To select features, choose a vector layer in the legend",
                                          QgsMessageBar.INFO, 3)
            return
            
        dlg = QgsExpressionSelectionDialog(vlayer)
        dlg.setAttribute(Qt.WA_DeleteOnClose)
        dlg.exec_()