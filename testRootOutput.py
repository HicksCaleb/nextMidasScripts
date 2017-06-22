from ROOT import *
from array import array
import matplotlib.pyplot as plt
import sys

a = int(sys.argv[1])
f = TFile.Open("run00033Output.root", "read")
datalist = []
for event in f.tree:
    datalist.append(event.channels[a])
plt.plot(datalist[2:])
plt.show()
