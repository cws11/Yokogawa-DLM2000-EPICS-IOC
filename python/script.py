import sys
import vxi11
import threading
import time
import os

sys.path.append("/home/PATH/.local/lib/python3.10/site-packages")

os.environ['EPICS_CA_ADDR_LIST'] = "127.0.0.1"
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"

class DLM2000(object):
    def __init__(self, ip):
        self.ip = ip
        self.instr = ""
        self.idn = ""
        self.waveformArray = [0 for col in range(12500)]
        self.arrayIndex = 0
        self.waveRange = 0
        self.waveOffset = 0
        self.waveform = 0
        self.acqCount = 0
        self.traceNumber = 0
        self.datalen = 0
        self.trace1 = []
        self.trace2 = []
        self.trace3 = []
        self.trace4 = []
        self.trace1_max = 0
        self.trace2_max = 0
        self.trace3_max = 0
        self.trace4_max = 0

    def connect(self):
        self.instr = vxi11.Instrument(self.ip)
        self.instr.write("COMMUNICATE:HEADER OFF")
        self.instr.write("WAVEFORM:FORMAT WORD")
        self.instr.write("WAVEFORM:START 0;END 124999")

    def gethering(self):
        print("Theread start")
        while True:
            try:
                waveform = self.instr.ask_raw(b"WAVEFORM:ALL:SEND? 0")                
                self.traceNumber = waveform[10] + (waveform[11] << 8)
                self.acqCount = waveform[12] + (waveform[13] << 8) + (waveform[14] << 16) + (waveform[15] << 24) \
                    + (waveform[16] << 32) + (waveform[17] << 40) + (waveform[18] << 48) + (waveform[19] << 56)                                   
                self.datalen = waveform[32] + (waveform[33] << 8) + (waveform[34] << 16) + (waveform[35] << 24)

                self.trace1_max = 0
                self.trace2_max = 0
                self.trace3_max = 0
                self.trace4_max = 0

                arrayIndex = 0
                for i in range(36+(self.datalen*0), self.datalen*2+36, 2):            
                    data = ((self.waveRange * (waveform[i] + (waveform[i+1] << 8)) / 3200) + float(self.waveOffset))/1000
                    if(data >= 15):
                        data = 0.1
                    if(arrayIndex < 8):
                        data = 0.1
                    if(self.trace1_max < data):
                        self.trace1_max = data
                    self.waveformArray[arrayIndex] = round(data, 8)
                    arrayIndex += 1
            
                self.trace1 = self.waveformArray
                self.waveformArray = [0 for col in range(12500)]

                arrayIndex = 0
                tindex = self.datalen*2+36
                self.datalen = waveform[tindex+12] + (waveform[tindex+13] << 8) + (waveform[tindex+14] << 16) + (waveform[tindex+15] << 24)            
            
                for i in range((tindex+16), (tindex+16+self.datalen*2), 2):                
                    data = ((self.waveRange * (waveform[i] + (waveform[i+1] << 8)) / 3200) + float(self.waveOffset))/1000
                    if(data >= 15):
                        data = 0.1
                    if(arrayIndex < 8):
                        data = 0.1
                    if(self.trace2_max < data):
                        self.trace2_max = data
                    self.waveformArray[arrayIndex] = round(data, 8)
                    arrayIndex += 1

                self.trace2 = self.waveformArray
                self.waveformArray = [0 for col in range(12500)]


                arrayIndex = 0
                tindex = (12500*4)+36+12
                self.datalen = waveform[tindex+12] + (waveform[tindex+13] << 8) + (waveform[tindex+14] << 16) + (waveform[tindex+15] << 24)            
            
            
                for i in range(50052, 75052, 2):                
                    data = ((self.waveRange * (waveform[i] + (waveform[i+1] << 8)) / 3200) + float(self.waveOffset))/1000
                    if(data >= 15):
                        data = 0.1
                    if(arrayIndex < 8):
                        data = 0.1
                    if(self.trace3_max < data):
                        self.trace3_max = data
                    self.waveformArray[arrayIndex] = round(data, 8)
                    arrayIndex += 1


                self.trace3 = self.waveformArray
                self.waveformArray = [0 for col in range(12500)]

                arrayIndex = 0
            
                for i in range(75070, 100070, 2):                
                    data = ((self.waveRange * (waveform[i] + (waveform[i+1] << 8)) / 3200) + float(self.waveOffset))/1000
                    if(data >= 15):
                        data = 0.1
                    if(arrayIndex < 8):
                        data = 0.1
                    if(self.trace4_max < data):
                        self.trace4_max = data
                    self.waveformArray[arrayIndex] = round(data, 8)
                    arrayIndex += 1
   
                self.trace4 = self.waveformArray
                self.waveformArray = [0 for col in range(12500)]

            except:
                pass

            time.sleep(0.1)

    def send(self, msg):
        if msg == "*IDN?":
            self.idn = self.instr.ask(msg)
        elif msg == "WAVEFORM:RANGE?":
            self.waveRange = float(self.instr.ask(msg))
        elif msg == "WAVEFORM:OFFSET?":
            self.waveOffset = float(self.instr.ask(msg))            
        elif msg == "WAVEFORM:ALL:SEND? 0":
            self.th = threading.Thread(target=self.gethering)
            self.th.start()
