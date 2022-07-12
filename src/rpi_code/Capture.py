#!/usr/bin/python3

from Motor import Motor
import os
import numpy as np

def CaptureProcedure(fileName,numFrames,sensorName,nCapEachDirection,configFile):
    m = Motor()
    # R2 => R1 => 0 => L1 => L2
    Qr = 1.165 * 2 / 20 # 10 deg = 1.165
    Ql = 1.45  * 2 / 20 # 10 deg = 2.1 1.85 
    
    
    cap = np.arange(0,nCapEachDirection+1,1).tolist()
    # cap = np.arange(-nCapEachDirection,nCapEachDirection+1,1).tolist()
    cap = [str(x) for x in cap]
    # cap = [x.replace('-','R') for x in cap]
    cap = ['R'+x if(not x.startswith('L')) else x for x in cap]
    j = 0
    for i in range(0,(len(cap)-1)):
        m.MotorMove("R", Qr, 0.5, 1) # - 20 Deg
        print(cap[j])                # R1 => 0 => L1 => L2
        Pyueye_OpenCV.Capture(fileName + "_"+ cap[j],float(numFrames),configFile)
        j = j + 1
    for i in range(0,(len(cap)-1)):        
        m.MotorMove("L", Ql, 0.5, 1) # - 20 Deg
    

from datetime import datetime
import argparse
import Pyueye_OpenCV

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('arg', metavar='N', type=str, nargs='+',
                    help='an integer for the accumulator')

now         = datetime.now()
args = parser.parse_args()
numFrames   = int(args.arg[0])
nCapDirctn  = int(args.arg[1]) if len(args.arg)>=2 else 1
configFile  = args.arg[2] if len(args.arg)>=3 else ""
CaptureTime = args.arg[3] if len(args.arg)>=4 else now.strftime("%H:%M")
fileName    = args.arg[4] if len(args.arg)>=5 else ""

homePath   = '/home/pi/Desktop/'
files      = [f for f in os.listdir(homePath) if os.path.isfile(homePath+f)]
sensorName = [s for s in files if "pi" in s]
sensorName = sensorName[0]
path       = sensorName +"_"+now.strftime("%Y_%m_%d__")+CaptureTime
if len(fileName) == 0:
    fileName = path

print("Capture time: " + CaptureTime)
print("numFrames: "    + str(numFrames))
print("Capture Name: " + fileName)
print("Current time: " + now.strftime("%H:%M"))

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if current_time == CaptureTime:
        print(now.strftime("%H:%M:%S") +" : Capture Started")
        idxFile = '1'
        if os.path.isdir(homePath+path+"_"+idxFile):
            files = [f for f in os.listdir(homePath) if os.path.isdir(homePath+f) and path in f]
            idxFile = str(int(files[-1].split('_')[-1])+1)
        os.mkdir(homePath+path+"_"+idxFile)
        CaptureProcedure(homePath + path+"_"+idxFile+"/"+fileName,numFrames,sensorName,nCapDirctn,configFile)
#         Pyueye_OpenCV.Capture(fileName + ".mp4",numFrames)
        break
    
# f = open("LogFile.txt", "a")
# f.write("Now the file has more content!")
# f.close()