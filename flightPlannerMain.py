# -*- coding: UTF-8 -*-

import os
import sys

from subprocess import call

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import QgsApplication

from Type.String import String
from AircraftOperation import AirCraftOperation
import define

appdatadir = None
path = None

if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
    path = path.replace("\\", "/")
    appdatadir = os.environ['LOCALAPPDATA']
    sys.stdout = open(appdatadir + '/my_stdout.log', 'w')
    sys.stderr = open(appdatadir + '/my_stderr.log', 'w')
elif __file__:
    path = os.path.dirname(__file__)
    path = path.replace("\\", "/")
    appdatadir = os.environ['LOCALAPPDATA']
    sys.__stdout__ = open(appdatadir + '/my_stdout.log', 'w')
    sys.__stderr__ = open(appdatadir + '/my_stderr.log', 'w')


# MyWnd depends on define.path
define.appPath = path

# try import clr module before importing MyWnd
# because MyWnd depends on whether clr module is imported

try:
    import clr
except ImportError:
    print "Failed to import module: clr"
    sys.exit(1)

from map.mainWindow import MyWnd

# with Global Assembly Cache, try to load SKGL.dll
call("runas " + define.appPath + "/Resource/dlls/gacutil.exe /i \"SKGL.dll\"")

try:
    clr.AddReference('SKGL')
    from SKGL import Validate, Generate
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except ImportError:
    print "Failed to import module: SKGL"
    sys.exit(1)
except:
    print "Unexpected error:", sys.exc_info()[0]
    sys.exit(1)


def main(argv):

    import _winreg as windowsregistry
    licensekey = None
    localmachinekeyhandle = windowsregistry.ConnectRegistry(None, windowsregistry.HKEY_LOCAL_MACHINE)
    keyhandle = None

    try:
        keyargument = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
        print "*** Reading from", keyargument, "***"
        keyhandle = windowsregistry.OpenKey(localmachinekeyhandle, keyargument)
        try:
            n, v, t = windowsregistry.EnumValue(keyhandle, 0)
            if n == "License":
                licensekey = v
                print licensekey
        except:
            print "no license"
        finally:
            try:
                windowsregistry.CloseKey(keyhandle)
            except:
                pass
    except:
        print "no License trag"
    finally:
        try:
            windowsregistry.CloseKey(localmachinekeyhandle)
        except:
            pass

        # create Qt application
        app = QApplication(argv)

        # Initialize qgis libraries
        QgsApplication.setPrefixPath(".", True)
        QgsApplication.initQgis()

        licenceflag = False

        if licensekey is not None:

            print "Compare Start"
            objvalidate = Validate()
            print "aerodrome$pw3s$Pa$$W0rd"
            objvalidate.secretPhase = "aerodrome$pw3s$Pa$$W0rd"
            objvalidate.Key = String.QString2Str(QString(licensekey)).replace("-", "")
            print objvalidate.Key

            try:
                if objvalidate.IsValid and objvalidate.IsOnRightMachine and objvalidate.SetTime >= objvalidate.DaysLeft:  # and objValidate.IsExpired == False ):
                    licenceflag = True
            except:
                pass

        define._appWidth = QApplication.desktop().screenGeometry().width()
        define._appHeight = QApplication.desktop().screenGeometry().height()

        window = MyWnd()
        window.setWindowState(Qt.WindowMaximized)
        window.show()
        retval = app.exec_()

        AirCraftOperation.g_AppSetting.WriteSettings()

        QgsApplication.exitQgis()
        sys.exit(retval)


if __name__ == "__main__":
    main(sys.argv)


