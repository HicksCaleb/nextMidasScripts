from ROOT import *
import matplotlib.pyplot as plt
import sys
inFile = sys.argv[1]
a = int(sys.argv[2])
f = TFile.Open(inFile, "read")
datalist = [event.channels[a] for event in f.tree]
plt.plot(datalist[2:])
plt.show()
