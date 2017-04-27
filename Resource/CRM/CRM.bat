@echo off
del CRMF01
del CRMF02
del CRMF03
del CRMF05
del CRMF06
del CRMF07
del CRMF08
del CRMX16
copy %1.obs CRMF05
crmedt
copy CRMF06 %1.prt
crmsort
crmrsk
crmrpt
copy CRMX16 %1.rsk
del CRMF01
del CRMF02
del CRMF03
del CRMF05
del CRMF06
del CRMF07
del CRMF08
del CRMX16