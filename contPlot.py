import sys
import matplotlib.pyplot as plt
import subprocess
import numpy as np
channel = [0]
plotRange = 100
scale = ['x']*23
for ca,a in enumerate(sys.argv):
	if a == '-c':
		channel = [int(b) for b in sys.argv[ca+1].split(',')]
	if a == '-r':
		plotRange = int(sys.argv[ca+1])
	if a == '-q':
		scale[int(sys.argv[ca+1])] = sys.argv[ca+2]
	if a == '-h':
		print('Help Menu')
		print('code\t|\tsyntax\t\t|\tusage')
		print('-c\t|\t-c \'a,b,c,...\'\t|\tchannels to plot on same axes')
		print('-r\t|\t-r n\t\t|\tplots last n event. 0 to disable moving.')
		print('-q\t|\t-q c \'a*x+b\'\t|\tscales c\'th channel input by a then adds b. Any equation works as long as it only uses * and + operators. e.g. -q 1 \'3*x+2\' would scale input 1 in the channel select aray by 3 then add 2.')
		print('-h\t|\t-h\t\t|\tprints this incredibly helpful advice')
		sys.exit()
channelValues = [[] for a in range(23)]
times = []
plt.ion()
fig = plt.figure()
plt.axis([0,1,0,1])
parse = lambda x: sum(np.product([float(j) for j in i.split('*')]) for i in x.split('+'))
while True:
	subprocess.call("rm temp",shell = True)
	subprocess.call("mdump >> temp", shell=True)
	temp = open("temp")
	values = [None]*23
	count = -1
	for line in temp:
		if line[0] == ' ' and line[4] != ' ':
			for a in line[7:-2].split(' '):
				if len(a) > 0:
					try:
						count += 1
						values[count] = float(a)
					except:
						continue
		if line[0] == 'E':
			time = int(line.split(' ')[3][5:-1],16)
	plt.color = 0,255,0
	plt.clf()
	times.append(time)
	for ca,a in enumerate(values):
		channelValues[ca].append(a)
	for ca,a in enumerate(channel):
		if len(channelValues[a]) > plotRange:
			yvals = [parse(scale[ca].replace('x',str(b))) for b in channelValues[a][-plotRange:]]
		else:
			yvals = [parse(scale[ca].replace('x',str(b))) for b in channelValues[a]]
		if len(times) > plotRange:
			plt.plot([x-times[0] for x in times][-plotRange:], yvals)
		else:
			plt.plot([x-times[0] for x in times], yvals)
	plt.draw()
