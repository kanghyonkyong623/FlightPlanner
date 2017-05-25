import os
from Type.String import String


class AppSetting:
    def __init__(self):
        self.ProjectFolderPath = None
        self.ProjectFolderPath = os.getcwdu()

    def WriteSettings(self):
        import _winreg as wr

        aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
        print "*** Writing to", targ, "***"
        try:
            aKey = wr.OpenKey(aReg, targ, 0, wr.KEY_WRITE)
        except:
            aKey = wr.CreateKey(aReg, targ)
        try:
            try:
                wr.SetValueEx(aKey, "ProjectPath", 0, wr.REG_SZ, String.QString2Str(self.ProjectFolderPath))
            except Exception:
                print "Encountered problems writing into the Registry..."
        except:
            print "NO"
        finally:
            wr.CloseKey(aKey)
            wr.CloseKey(aReg)

    def ReadSettings(self):
        import _winreg as wr
        aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        aKey = None
        try:
            targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
            print "*** Reading from", targ, "***"
            aKey = wr.OpenKey(aReg, targ)
            try:
                n, v, t = wr.EnumValue(aKey, 0)
                if n == "ProjectPath":
                    self.ProjectFolderPath = v
                    print self.ProjectFolderPath
                    return
            except:
                print "no ProjectPath"
            finally:
                try:
                    wr.CloseKey(aKey)
                except:
                    pass
        except:
            print "no ProjectPath trag"
        finally:
            try:
                wr.CloseKey(aReg)
            except:
                pass
