from ROOT import *
from array import array
import matplotlib.pyplot as plt
import sys
inFile = sys.argv[1]
a = int(sys.argv[2])
f = TFile.Open(inFile, "read")
datalist = []
for event in f.tree:
    datalist.append(event.channels[a])
plt.plot(datalist[2:])
plt.show()
