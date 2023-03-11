import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
from rtlsdr import *
import time 

f_s = 2.4e6
freq_start = 90e6
freq_stop = 108e6
NFFT = 256

N_cycles = math.floor((freq_stop-freq_start)/f_s)
N_cycles = int(N_cycles)
print N_cycles

freq = np.linspace(freq_start, freq_start+(N_cycles*f_s), NFFT*N_cycles)

# configure the rtlsdr
sdr = RtlSdr()
sdr.sample_rate = f_s
sdr.gain = 4

fig = plt.figure()
ax = plt.axes(xlim=(min(freq), max(freq)), ylim=(-20.0, 30))
line, = ax.plot([], [], lw=2)
ax.grid()
ax.set_xlabel("Freq")
ax.set_ylabel("Uncalibrated power")

def animate(rr):	
	swept_power = np.zeros(NFFT*N_cycles)	
	sdr.center_freq = freq_start - (0.5*f_s)	
	for k in range(N_cycles):
#		plt.figure()	
		sdr.center_freq = sdr.center_freq + f_s
#		print sdr.center_freq
		samples = sdr.read_samples(1024)
		samples = sdr.read_samples(1024)
		sig_f = np.fft.fft(a=samples, n=NFFT)
		swept_power[k*NFFT:(k+1)*NFFT] = np.abs(np.fft.fftshift(sig_f))

	ax.set_xlim(min(freq), max(freq))
	line.set_data(freq, 10*np.log10(swept_power))
#	line.set_data(freq, (swept_power))
	return line,
	
anim = animation.FuncAnimation(fig, animate, frames=None, interval=1)
plt.show()
sdr.close()

