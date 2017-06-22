#Converts the .mid file into a big table. Hopefully more efficient data format at the expense of easily accessing the information

import sys
import subprocess
import struct
import datetime
from ROOT import *
from array import array

gROOT.ProcessLine(
  "struct EventStruct{\
  Int_t ID;\
  Float_t channels[50];\
  Char_t time[19];\
  };");



inFile = sys.argv[1]
if len(sys.argv) > 2:
  outFile = sys.argv[2] #take the arguments
else:
  outFile = inFile.split(".")[0] + "Output" + ".root"
subprocess.call("rm temp.temp &>/dev/null", shell = True) #make sure we don't have any files left over


command = "mdump -x "
command += inFile
command += " >> temp.temp" #dump the file into a temporary location

subprocess.call(command, shell = True)
command = "touch " + outFile #create the output file
subprocess.call(command, shell = True)
tempFile = open('temp.temp')
outputFile = TFile(outFile, "recreate")
event = EventStruct()
tree = TTree('tree','tree')
tree.Branch('Channels', AddressOf(event,"channels"), 'channels[50]/F')
tree.Branch('ID', AddressOf(event, 'ID'), 'ID/I')
tree.Branch('time', AddressOf(event, 'time'), 'time/C')
eventNum = -1
for line in tempFile:
  if line[0] == '-': #event incrememntation
    eventNum += 1
    tree.Fill()
    event.ID = eventNum
    count = 0
  if line[0] == ' ': #channel data
    values = line[10:-2].split(" ")
    for a in values:
      try:
        f = int(a,16)
        b = struct.unpack('f', struct.pack('>I',f))[0]
        event.channels[count] = b
        count += 1
      except: 
        #print("End of File")
        continue
  if line[0] == "E":
    values = line.split(" ") #need timestamp from this data
    time = datetime.datetime.fromtimestamp(int(values[3][5:-1],16)).strftime('%Y-%m-%d %H:%M:%S')
    event.time = time
subprocess.call('rm temp.temp', shell = True) #get rid of the temporary file

outputFile.Write()
outputFile.Close()