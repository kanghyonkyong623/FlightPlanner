from PyQt4.QtCore import QCoreApplication, QFileInfo, QSettings, QDir
from PyQt4.QtGui import QDialog, QFileDialog

from qgis.core import QGis
from qgis.core import QgsVectorLayer

import define
from QgisHelper import QgisHelper

from FlightPlanner.ui_AddObstacleLayerDlg import Ui_AddObstacleLayerDlg
from FlightPlanner.types import SurfaceTypes


class AddObstacleLayerDlg(QDialog):
    def __init__(self, parent, canvas):
        QDialog.__init__(self, parent)
        self.ui = Ui_AddObstacleLayerDlg()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.cmbCurrentCrs.addItem("DecimalDegree")
        self.ui.cmbCurrentCrs.addItem("Meter")
        self.ui.cmbDisplayCrs.addItem("DecimalDegree")
        self.ui.cmbDisplayCrs.addItem("Meter")
        self.ui.cmbDisplayCrs.setDisabled(True)
        self.ui.btnBrowse.clicked.connect(self.OpenObstacleFile)

        if define._units == QGis.DecimalDegrees:
            self.ui.cmbDisplayCrs.setCurrentIndex(0)
        else:
            self.ui.cmbDisplayCrs.setCurrentIndex(1)
        
    def OpenObstacleFile(self):
        settings = QSettings()

        lastusedir = settings.value("/UI/lastObstacleVectorFileDir", QDir.homePath()).toString()

        path = QFileDialog.getOpenFileName(self, "Open Obstacle File", lastusedir, "Obstacle files(*.txt *.csv)")

        if path == "":
            return

        self.ui.txtPath.setText(path)

        settings.setValue("/UI/lastObstacleVectorFileDir", path)

    def verify(self):
        if self.ui.txtPath.text() == "":
            return

        filePathDirInfo = QFileInfo(self.ui.txtPath.text())
        sName=filePathDirInfo.fileName() 
        vectorName = sName[:len(sName)-4]
        uri1 = ""

        if self.ui.cmbCurrentCrs.currentText() == self.ui.cmbDisplayCrs.currentText():
            if self.ui.cmbCurrentCrs.currentText() == "DecimalDegree":
                uri1 = "file:" + self.ui.txtPath.text() + "?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName)
            else:
                uri1 = "file:" + self.ui.txtPath.text() + "?delimiter=%s&xField=%s&yField=%s&crs=epsg:32633" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName)

        else:            
            if self.ui.cmbCurrentCrs.currentText() == "DecimalDegree":
                uri1 = "file:" + self.ui.txtPath.text() + "?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName)
            else:
                uri1 = "file:" + self.ui.txtPath.text() + "?delimiter=%s&xField=%s&yField=%s&crs=epsg:32633" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName)
        
    def AddMapLayer(self, uri1, vectorName):
        layer = QgsVectorLayer(uri1, vectorName, "delimitedtext") 
        
        QgisHelper.appendToCanvas(define._canvas, [layer], SurfaceTypes.Obstacles)
        self.canvas.zoomToFullExtent()