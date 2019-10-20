import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
from rtlsdr import *
import time 

f_s = 2.4e6
c_freq = 92e6
NFFT = 1024
N_aver = 1000
# configure the rtlsdr
sdr = RtlSdr()
sdr.sample_rate = f_s
sdr.center_freq = c_freq
sdr.gain = 10

freq=np.linspace(c_freq-(f_s/2.0), c_freq+(f_s/2.0), NFFT)

#timestr = time.strftime("%Y%m%d-%H%M%S")
#print "Writing out in file "+str(timestr)+" .txt"
#f = open(timestr+".txt",'wb')

#val = np.zeros(1024)
#time_sec = np.zeros(1024)
#tinit = time.time()

fig = plt.figure()
ax = plt.axes(xlim=(min(freq), max(freq)),  ylim=(-20.0, 10)) #xlim=(0, 1024), ylim=(0.0, 0.025)
line, = ax.plot([], [], lw=2)
ax.grid()
ax.set_xlabel("Freq")
ax.set_ylabel("Uncalibrated power")

def animate(i):	
	global val
	global time_sec
	global tinit
	
#	ti = time.time()
	accum_data = np.zeros(shape=NFFT, dtype=np.complex64)	
	for k in range(N_aver):		
		samples = sdr.read_samples(1*NFFT)
		samples = samples
		sig_f = np.fft.fft(a=samples, n=NFFT)
		accum_data = accum_data+sig_f
	
#	ax.set_xlim(min(freq), max(freq))
	accum_data = accum_data/N_aver
	line.set_data(freq,10*np.log10(np.abs(np.fft.fftshift(accum_data))))
	return line,
	
anim = animation.FuncAnimation(fig, animate, frames=None, interval=1)
plt.show()
sdr.close()
#f.close()

