
from PyQt4.QtGui import QDialog, QIntValidator, QDialogButtonBox, QTreeWidgetItem, QIcon, QMessageBox, QFileDialog
from PyQt4.QtCore import QStringList, SIGNAL, Qt, QString, QSettings, QDir, QFileInfo, QLibrary, QVariant
from qgis.core import QgsVectorDataProvider, QGis, QgsVectorFileWriter, QgsProviderRegistry, QgsVectorLayer, QgsField
# from qgis.gui import QgsDebugMsg
from map.CreateVectorLayer.qgsnewvectorlayerdialogbase import Ui_QgsNewVectorLayerDialogBase
from Type.String import String
from Type.switch import switch
from FlightPlanner.QgisHelper import QgisHelper

import define

class QgsNewVectorLayerDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.ui = Ui_QgsNewVectorLayerDialogBase()
        self.ui.setupUi(self)

        # self.ui.mAddAttributeButton.setIcon(QIcon("Resource/images/themes/default/mActionNewAttribute.svg"))
        # self.ui.mRemoveAttributeButton.setIcon(QIcon("Resource/images/themes/default/mActionDeleteAttribute.svg"))
        self.ui.mTypeBox.addItem("Text data", "String")
        self.ui.mTypeBox.addItem("Whole number", "Integer")
        self.ui.mTypeBox.addItem("Decimal number", "Real")
        self.ui.mTypeBox.addItem("Date", "Date")

        self.ui.mWidth.setValidator(QIntValidator( 1, 255, self))
        self.ui.mPrecision.setValidator(QIntValidator( 0, 15, self))

        self.ui.mPointRadioButton.setChecked( True )
        self.ui.mFileFormatComboBox.addItem("ESRI Shapefile", "ESRI Shapefile")

        # self.ui.mFileFormatComboBox.addItem("Comma Separated Value", "Comma Separated Value")
        # self.ui.mFileFormatComboBox.addItem("GML", "GML")
        # self.ui.mFileFormatComboBox.addItem("Mapinfo File", "Mapinfo File")
        #endif

        if ( self.ui.mFileFormatComboBox.count() == 1 ):
            self.ui.mFileFormatComboBox.setVisible( False )
            self.ui.mFileFormatLabel.setVisible( False )

        self.ui.mFileFormatComboBox.setCurrentIndex( 0 )

        self.ui.mFileEncoding.addItems( QgsVectorDataProvider.availableEncodings() )

        # Use default encoding if none supplied
        # enc = QSettings().value( "/UI/encoding", "System" ).toString()

        # The specified decoding is added if not existing alread, and then set current.
        # This should select it.
        # int encindex = self.ui.mFileEncoding.findText( enc )
        # if ( encindex < 0 )
        # {
        # self.ui.mFileEncoding.insertItem( 0, enc )
        # encindex = 0
        # }
        # self.ui.mFileEncoding.setCurrentIndex( encindex )



        self.ui.mAttributeView.addTopLevelItem( QTreeWidgetItem( QStringList(["id", "Integer", "10", ""])))

        # defaultCrs = QgsCRSCache::instance().crsByOgcWmsCrs( settings.value( "/Projections/layerDefaultCrs", GEO_EPSG_CRS_AUTHID ).toString() )
        # defaultCrs.validate()
        if define._units == QGis.Meters:
            defaultCrs = define._xyCrs
        else:
            defaultCrs = define._latLonCrs
        self.ui.mCrsSelector.setCrs( defaultCrs )

        self.connect( self.ui.mNameEdit, SIGNAL("textChanged( QString )"), self.nameChanged)
        self.connect( self.ui.mAttributeView, SIGNAL("itemSelectionChanged()"), self.selectionChanged)

        self.ui.mAddAttributeButton.setEnabled( False )
        self.ui.mRemoveAttributeButton.setEnabled( False )

        self.ui.mAddAttributeButton.clicked.connect(self.mAddAttributeButtonClicked)
        self.ui.mRemoveAttributeButton.clicked.connect(self.mRemoveAttributeButtonClicked)
        self.ui.mTypeBox.currentIndexChanged.connect(self.mTypeBoxCrrentIndexChanged)
        self.ui.mFileFormatComboBox.currentIndexChanged.connect(self.mFileFormatComboBoxCurrentIndexChanged)
#
#
# QgsNewVectorLayerDialog::~QgsNewVectorLayerDialog()
# {
#   QSettings settings
#   settings.setValue( "/Windows/NewVectorLayer/geometry", saveGeometry() )
# }
#
    def mFileFormatComboBoxCurrentIndexChanged(self, index ):
        # Q_UNUSED( index )
        if ( self.ui.mFileFormatComboBox.currentText() == "ESRI Shapefile" ) :
            self.ui.mNameEdit.setMaxLength( 10 )
        else:
            self.ui.mNameEdit.setMaxLength( 32767 )

    def mTypeBoxCrrentIndexChanged(self, index ):
        # FIXME: sync with providers/ogr/qgsogrprovider.cpp
        if isinstance(index, str) or isinstance(index, QString):
            return
        for case in switch ( index ):
            if case(0): # Text data
                if ( int(self.ui.mWidth.text()) < 1 or int(self.ui.mWidth.text()) > 255 ):
                    self.ui.mWidth.setText( "80" )
                self.ui.mPrecision.setEnabled( False )
                self.ui.mWidth.setValidator( QIntValidator( 1, 255, self) )
                break

            elif case(1): # Whole number
                if ( int(self.ui.mWidth.text()) < 1 or int(self.ui.mWidth.text()) > 10 ):
                    self.ui.mWidth.setText( "10" )
                self.ui.mPrecision.setEnabled( False )
                self.ui.mWidth.setValidator( QIntValidator( 1, 10, self) )
                break

            elif case(2): # Decimal number
                if ( int(self.ui.mWidth.text()) < 1 or int(self.ui.mWidth.text()) > 20 ):
                    self.ui.mWidth.setText( "20" )
                self.ui.mPrecision.setEnabled( True )
                self.ui.mWidth.setValidator( QIntValidator( 1, 20, self) )
                break

            else:
                QMessageBox.warning(self, "Warning", "unexpected index" )
                break

    def selectedType(self):
        if ( self.ui.mPointRadioButton.isChecked() ):
            return QGis.Point
        elif ( self.ui.mLineRadioButton.isChecked() ):
            return QGis.Line
        elif ( self.ui.mPolygonRadioButton.isChecked() ):
            return QGis.Polygon
        return QGis.WKBUnknown

    def selectedCrsId(self):
        return self.ui.mCrsSelector.crs().srsid()
    def selectedAuthId(self):
        return self.ui.mCrsSelector.crs().authid()
    def selectedCrs(self):
        return self.ui.mCrsSelector.crs()

    def mAddAttributeButtonClicked(self):
        self.ui.myName = self.ui.mNameEdit.text()
        self.ui.myWidth = self.ui.mWidth.text()
        self.ui.myPrecision = self.ui.mPrecision.text() if(self.ui.mPrecision.isEnabled()) else""
        #use userrole to avoid translated type string
        self.ui.myType = self.ui.mTypeBox.itemData( self.ui.mTypeBox.currentIndex(), Qt.UserRole ).toString()
        self.ui.mAttributeView.addTopLevelItem( QTreeWidgetItem( QStringList([self.ui.myName, self.ui.myType, self.ui.myWidth, self.ui.myPrecision] ) ))
        if ( self.ui.mAttributeView.topLevelItemCount() > 0 ):
            self.ui.mOkButton.setEnabled( True )
        self.ui.mNameEdit.clear()

    def mRemoveAttributeButtonClicked(self):
        # del self.ui.mAttributeView.currentItem()
        self.ui.mAttributeView.takeTopLevelItem(self.ui.mAttributeView.currentIndex().row())
        if ( self.ui.mAttributeView.topLevelItemCount() == 0 ):
            self.ui.mOkButton.setEnabled( False )

    def attributes(self, at ):
        topLevelItemCount = self.ui.mAttributeView.topLevelItemCount()
        # QTreeWidgetItemIterator it( mAttributeView )
        for i in range(topLevelItemCount):
        # while ( *it )
            item = self.ui.mAttributeView.topLevelItem(i)
            type = []
            if item.text(1) == "BitArray":
                type.append(QVariant.BitArray)
            elif item.text(1) == "Bitmap":
                type.append(QVariant.Bitmap)
            elif item.text(1) == "Bool":
                type.append(QVariant.Bool)
            elif item.text(1) == "Brush":
                type.append(QVariant.Brush)
            elif item.text(1) == "ByteArray":
                type.append(QVariant.ByteArray)
            elif item.text(1) == "Char":
                type.append(QVariant.Char)
            elif item.text(1) == "Color":
                type.append(QVariant.Color)
            elif item.text(1) == "Cursor":
                type.append(QVariant.Cursor)
            elif item.text(1) == "Date":
                type.append(QVariant.Date)
            elif item.text(1) == "DateTime":
                type.append(QVariant.DateTime)
            elif item.text(1) == "Double":
                type.append(QVariant.Double)
            elif item.text(1) == "EasingCurve":
                type.append(QVariant.EasingCurve)
            elif item.text(1) == "Font":
                type.append(QVariant.Font)
            elif item.text(1) == "Hash":
                type.append(QVariant.Hash)
            elif item.text(1) == "Icon":
                type.append(QVariant.Icon)
            elif item.text(1) == "Image":
                type.append(QVariant.Image)
            elif item.text(1) == "Int":
                type.append(QVariant.Int)
            elif item.text(1) == "Integer":
                type.append(QVariant.Int)
            elif item.text(1) == "Invalid":
                type.append(QVariant.Invalid)
            elif item.text(1) == "KeySequence":
                type.append(QVariant.KeySequence)
            elif item.text(1) == "Line":
                type.append(QVariant.Line)
            elif item.text(1) == "LineF":
                type.append(QVariant.LineF)
            elif item.text(1) == "List":
                type.append(QVariant.List)
            elif item.text(1) == "Locale":
                type.append(QVariant.Locale)
            elif item.text(1) == "LongLong":
                type.append(QVariant.LongLong)
            elif item.text(1) == "Map":
                type.append(QVariant.Map)
            elif item.text(1) == "Matrix":
                type.append(QVariant.Matrix)
            elif item.text(1) == "Matrix4x4":
                type.append(QVariant.Matrix4x4)
            elif item.text(1) == "Palette":
                type.append(QVariant.Palette)
            elif item.text(1) == "Pen":
                type.append(QVariant.Pen)
            elif item.text(1) == "Pixmap":
                type.append(QVariant.Pixmap)
            elif item.text(1) == "Point":
                type.append(QVariant.Point)
            elif item.text(1) == "PointF":
                type.append(QVariant.PointF)
            elif item.text(1) == "Polygon":
                type.append(QVariant.Polygon)
            elif item.text(1) == "Quaternion":
                type.append(QVariant.Quaternion)
            elif item.text(1) == "Rect":
                type.append(QVariant.Rect)
            elif item.text(1) == "RectF":
                type.append(QVariant.RectF)
            elif item.text(1) == "RegExp":
                type.append(QVariant.RegExp)
            elif item.text(1) == "Region":
                type.append(QVariant.Region)
            elif item.text(1) == "Size":
                type.append(QVariant.Size)
            elif item.text(1) == "SizeF":
                type.append(QVariant.SizeF)
            elif item.text(1) == "SizePolicy":
                type.append(QVariant.SizePolicy)
            elif item.text(1) == "String":
                type.append(QVariant.String)
            elif item.text(1) == "StringList":
                type.append(QVariant.StringList)
            elif item.text(1) == "TextFormat":
                type.append(QVariant.TextFormat)
            elif item.text(1) == "TextLength":
                type.append(QVariant.TextLength)
            elif item.text(1) == "Time":
                type.append(QVariant.Time)
            elif item.text(1) == "Transform":
                type.append(QVariant.Transform)
            elif item.text(1) == "UInt":
                type.append(QVariant.UInt)
            elif item.text(1) == "ULongLong":
                type.append(QVariant.ULongLong)
            elif item.text(1) == "Url":
                type.append(QVariant.Url)
            elif item.text(1) == "UserType":
                type.append(QVariant.UserType)
            elif item.text(1) == "Vector2D":
                type.append(QVariant.Vector2D)
            elif item.text(1) == "Vector3D":
                type.append(QVariant.Vector3D)
            elif item.text(1) == "Vector4D":
                type.append(QVariant.Vector4D)
            type.append(item.text(2))

            # type = QString( "%1%2%3" ).arg( item.text( 1 ), item.text( 2 ), item.text( 3 ) )
            at.__setitem__( item.text( 0 ), type )
            # print( QString( "appending %1#%2" ).arg( item.text( 0 ), type ) )


    def selectedFileFormat(self):
        #use userrole to avoid translated type string
        self.ui.myType = self.ui.mFileFormatComboBox.itemData( self.ui.mFileFormatComboBox.currentIndex(), Qt.UserRole ).toString()
        return self.ui.myType

    def selectedFileEncoding(self):
        return self.ui.mFileEncoding.currentText()

    def nameChanged(self, name):
        self.ui.mAddAttributeButton.setDisabled( String.IsNullOrEmpty(name) or not len(self.ui.mAttributeView.findItems( name, Qt.MatchExactly )) == 0 )
        print name
#
    def selectionChanged(self):
        self.ui.mRemoveAttributeButton.setDisabled( len(self.ui.mAttributeView.selectedItems()) == 0)

    # this is static
    @staticmethod
    def runAndCreateLayer(parent):
        geomDialog = QgsNewVectorLayerDialog( parent )
        if ( geomDialog.exec_() == QDialog.Rejected ):
            return ""

        geometrytype = geomDialog.selectedType()
        fileformat = geomDialog.selectedFileFormat()
        enc = geomDialog.selectedFileEncoding()
        crsId = geomDialog.selectedCrsId()
        print( QString( "New file format will be: %1" ).arg( fileformat ) )

        attributes = dict()
        geomDialog.attributes( attributes )

        settings = QSettings()
        lastUsedDir = settings.value( "/UI/lastVectorFileFilterDir", QDir.homePath() ).toString()
        filterString = QgsVectorFileWriter.filterForDriver( fileformat )
        fileName = QFileDialog.getSaveFileName(parent,  "Save layer as..." , lastUsedDir, filterString )
        if ( fileName.isNull() ):
            return ""

        if ( fileformat == "ESRI Shapefile" and not fileName.endsWith( ".shp", Qt.CaseInsensitive ) ):
            fileName += ".shp"

        settings.setValue( "/UI/lastVectorFileFilterDir", QFileInfo( fileName ).absolutePath() )
        settings.setValue( "/UI/encoding", enc )

        #try to create the new layer with OGRProvider instead of QgsVectorFileWriter
        pReg = QgsProviderRegistry.instance()
        ogrlib = pReg.library( "ogr" )
        # load the data provider
        myLib = QLibrary( ogrlib )
        loaded = myLib.load()

        constructionLineLayer = None
        mapUnits = define._canvas.mapUnits()
        layerName = String.QString2Str(fileName).split("\\")[-1]
        path = "memory"
        selectedCrs = geomDialog.selectedCrs()
        if geometrytype == QGis.Line:
            # if mapUnits == QGis.Meters:
            constructionLineLayer = QgsVectorLayer("linestring?crs=%s"%selectedCrs.authid (), layerName, path)
            # else:
            #     constructionLineLayer = QgsVectorLayer("linestring?crs=%s"%define._latLonCrs.authid (), layerName, path)


        elif geometrytype == QGis.Polygon:
            # if mapUnits == QGis.Meters:
            constructionLineLayer = QgsVectorLayer("polygon?crs=%s"%selectedCrs.authid(), layerName, path)
            # else:
            #     constructionLineLayer = QgsVectorLayer("polygon?crs=%s"%define._latLonCrs.authid (), layerName, path)

        elif geometrytype == QGis.Point:
            # if mapUnits == QGis.Meters:
            constructionLineLayer = QgsVectorLayer("Point?crs=%s"%selectedCrs.authid (), layerName, path)
            # else:
            #     constructionLineLayer = QgsVectorLayer("Point?crs=%s"%define._latLonCrs.authid (), layerName, path)
        fieldList = []
        for key in attributes.iterkeys():
            fieldList.append(QgsField(key, attributes[key][0]))
        constructionLineLayer.startEditing()
        constructionLineLayer.dataProvider().addAttributes(fieldList)
        constructionLineLayer.commitChanges()

        er = QgsVectorFileWriter.writeAsVectorFormat(constructionLineLayer, fileName, "utf-8", constructionLineLayer.crs())
        constructionLineLayer = QgsVectorLayer(fileName, layerName, "ogr")

        QgisHelper.appendToCanvas(define._canvas, [constructionLineLayer], "NewLayers")

        # if ( loaded ):
        #     print( "ogr provider loaded" )
        #
        #     typedef bool ( *createEmptyDataSourceProc )( const QString&, const QString&, const QString&, QGis::WkbType,
        #     const QList< QPair<QString, QString> >&, const QgsCoordinateReferenceSystem * )
        #     createEmptyDataSourceProc createEmptyDataSource = ( createEmptyDataSourceProc ) cast_to_fptr( myLib.resolve( "createEmptyDataSource" ) )
        #     if ( createEmptyDataSource )
        #     {
        #         if ( geometrytype not = QGis::WKBUnknown )
        #         {
        #             QgsCoordinateReferenceSystem srs = QgsCRSCache::instance().crsBySrsId( crsId )
        #             if ( not createEmptyDataSource( fileName, fileformat, enc, geometrytype, attributes, &srs ) )
        #             {
        #                 return QString::null
        #             }
        #         }
        #         else
        #         {
        #             QgsDebugMsg( "geometry type not recognised" )
        #             return QString::null
        #         }
        #     }
        #     else
        #     {
        #         QgsDebugMsg( "Resolving newEmptyDataSource(...) failed" )
        #         return QString::null
        #     }
        # }
        #
        # if ( pEnc )
        # *pEnc = enc

        return fileName