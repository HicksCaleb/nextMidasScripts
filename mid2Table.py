#Converts the .mid file into a big table. Hopefully more efficient data format at the expense of easily accessing the information

import sys
import subprocess
import struct
import datetime
inFile = sys.argv[1]
if len(sys.argv) > 2:
  outFile = sys.argv[2] #take the arguments
else:
  outFile = inFile.split(".")[0] + "Output" + ".csv"
subprocess.call("rm temp.temp &>/dev/null", shell = True) #make sure we don't have any files left over


command = "mdump -x "
command += inFile
command += " >> temp.temp" #dump the file into a temporary location

subprocess.call(command, shell = True)
command = "touch " + outFile #create the output file
subprocess.call(command, shell = True)
tempFile = open('temp.temp')
outputFile = open(outFile, 'w')
event  = -1
channel = -1
outputFile.write('event,time,') #header
for a in range(50):
    outputFile.write('channel' + str(a) + ',')
for line in tempFile:
  if line[0] == '-': #event incrememntation
    event += 1
    outputFile.write("\n"+str(event) + ',')
  if line[0] == ' ': #channel data
    values = line[10:-2].split(" ")
    for a in values:
      channel += 1
      try:
        f = int(a,16)
        b = struct.unpack('f', struct.pack('>I',f))[0]
        #b = struct.unpack('>f',a.decode('hex'))[0]
        #outputFile.write(str(event)+","+str(channel)+","+  time + "," + str(b)+ "\n")
        outputFile.write(str(b) + ',')
      except: 
        #print("End of File")
        continue
  if line[0] == "E":
    values = line.split(" ") #need timestamp from this data
    time = datetime.datetime.fromtimestamp(int(values[3][5:-1],16)).strftime('%Y-%m-%d %H:%M:%S')
    outputFile.write(time + ',')
subprocess.call('rm temp.temp', shell = True) #get rid of the temporary file
outputFile.close()
