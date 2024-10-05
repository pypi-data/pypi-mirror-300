# EPICS IOC Startup Script generated by https://github.com/epics-containers/ibek

cd "/epics/ioc"

epicsEnvSet Vec0 192

dbLoadDatabase dbd/ioc.dbd
ioc_registerRecordDeviceDriver pdbbase

# global "magic" is 42
# counter "InterruptVector" is now 193
# counter "InterruptVector" is now 194

dbLoadRecords /epics/runtime/ioc.db
iocInit

