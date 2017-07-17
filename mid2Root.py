#Converts the .mid file into a big table. Hopefully more efficient data format at the expense of easily accessing the information
#June 2017
#Caleb Hicks
#My Apologies for this Code
import sys
import subprocess
import struct
import datetime
from ROOT import *
from array import array

gROOT.ProcessLine( #Declare struct in c because root needs a c type
  "struct EventStruct{\
  Int_t ID;\
  Float_t channels[23];\
  Int_t time;\
  };");



inFile = sys.argv[1]
if len(sys.argv) > 2:
  outFile = sys.argv[2] #take the arguments
else:
  outFile = inFile[-12:-4] + "Output" + ".root"
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
tree = TTree('tree','tree')#Create root datastructure from c struct
tree.Branch('Channels', AddressOf(event,"channels"), 'channels[23]/F')
tree.Branch('ID', AddressOf(event, 'ID'), 'ID/I')
tree.Branch('time', AddressOf(event, 'time'), 'time/I')
eventNum = -1
for line in tempFile:
  if line[0] == '-': #event incrememntation
    eventNum += 1
    tree.Fill()#at this point the first event is empty, then subsequent events will have full information. Write them to the tree so we can overwrite event with the next event's info
    event.ID = eventNum
    count = 0
  if line[0] == ' ': #channel data
    values = line[7:-2].split(" ")
    for a in values:
      try:
        event.channels[count] = float(a)#see if we have a float
        count += 1
      except: #otherwise pretend like I never asked
	continue
  if line[0] == "E":
    values = line.split(" ") #need timestamp from this data
    time = int(values[3][5:-1],16)
	#time = datetime.datetime.fromtimestamp(int(values[3][5:-1],16)).strftime('%Y-%m-%d %H:%M:%S')
    event.time = time 
subprocess.call('rm temp.temp', shell = True) #get rid of the temporary file

outputFile.Write()
outputFile.Close()
