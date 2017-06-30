#converts input .mid file to a csv where each channel readout is on its own line
#This repeats a lot of data (time, event) but it will be easy to read out one event's channel. 

#June 2017
#Caleb Hicks
#My apologies for this code

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
outputFile.write('event,channel,time,value\n') #header
for line in tempFile:
	if line[0] == '-': #event incrememntation
		event += 1
		channel = -1
	if line[0] == ' ': #channel data
		values = line[10:-2].split(" ")
		for a in values:
			if len(a) > 0:
				try:
					channel += 1
					outputFile.write(str(event)+","+str(channel)+","+  time + "," + a+ "\n")
				except: 
					continue
	if line[0] == "E":
		values = line.split(" ") #need timestamp from this data
		time = datetime.datetime.fromtimestamp(int(values[3][5:-1],16)).strftime('%Y-%m-%d %H:%M:%S')

subprocess.call('rm temp.temp', shell = True) #get rid of the temporary file
outputFile.close()
