import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
from rtlsdr import *
import time 

# configure the rtlsdr
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 100e6
sdr.gain = 20

#timestr = time.strftime("%Y%m%d-%H%M%S")
#print "Writing out in file "+str(timestr)+" .txt"
#f = open(timestr+".txt",'wb')

#val = np.zeros(1024)
#time_sec = np.zeros(1024)
#tinit = time.time()

NFFT = 1024

fig = plt.figure()
ax = plt.axes(xlim=(0, NFFT),  ylim=(0.0, 1000.0)) #xlim=(0, 1024), ylim=(0.0, 0.025)
line, = ax.plot([], [], lw=2)
ax.grid()
ax.set_xlabel("Freq")
ax.set_ylabel("Uncalibrated power")

def animate(i):	
	global val
	global time_sec
	global tinit
	
#	ti = time.time()
		
	samples = sdr.read_samples(1*NFFT)
	sig_f = np.fft.fft(a=samples, n=NFFT)
	sig_fx = sig_f*np.conj(sig_f)
	
#	ax.set_xlim(min(time_sec), max(time_sec))
	line.set_data(range(NFFT),np.abs(sig_fx))
	return line,
	
anim = animation.FuncAnimation(fig, animate, frames=None, interval=1)
plt.show()
sdr.close()
#f.close()

