TOP=../..

include $(TOP)/configure/CONFIG
include $(PYDEVICE)/configure/CONFIG.PyDevice
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

# build an ioc application

PROD_IOC = dlm2000
# dlm2000.dbd will be created and installed
DBD += dlm2000.dbd

dlm2000_DBD += base.dbd
dlm2000_DBD += pydev.dbd

# dlm2000_registerRecordDeviceDriver.cpp will be created from dlm2000.dbd
dlm2000_SRCS += dlm2000_registerRecordDeviceDriver.cpp
dlm2000_SRCS_DEFAULT += dlm2000Main.cpp
dlm2000_SRCS_vxWorks += -nil-

# Add vxWorks support stuff
#dlm2000_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Add the support libraries needed by this application
dlm2000_LIBS += pydev

# Finally include the libraries from base
dlm2000_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

