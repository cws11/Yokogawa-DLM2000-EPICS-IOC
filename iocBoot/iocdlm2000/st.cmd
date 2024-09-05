#!../../bin/linux-x86_64/dlm2000

#- You may have to change dlm2000 to something else
#- everywhere it appears in this file

< envPaths

epicsEnvSet("PYTHONPATH", "$(TOP)/python")
epicsEnvSet("EPICS_CA_MAX_ARRAY_BYTES", "10000000")


## Register all support components
dbLoadDatabase "../../dbd/dlm2000.dbd"
dlm2000_registerRecordDeviceDriver(pdbbase) 

## Load record instances
dbLoadRecords("../../db/dlm2000.db","P=TEST, R=TEST, PORT=DLM2000")

pydev("from script import DLM2000")
pydev("dev = DLM2000('192.168.1.1')")
pydev("dev.connect()")
pydev("dev.send('*IDN?')")
pydev("dev.send('WAVEFORM:RANGE?')")
pydev("dev.send('WAVEFORM:OFFSET?')")
pydev("dev.send('WAVEFORM:ALL:SEND? 0')")

iocInit()
