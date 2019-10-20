import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
from rtlsdr import *
import time 

f_s = 2.4e6
freq_start = 98e6
freq_stop = 106e6
NFFT = 128

N_cycles = math.floor((freq_stop-freq_start)/f_s)
N_cycles = int(N_cycles)
print N_cycles

# configure the rtlsdr
sdr = RtlSdr()
sdr.sample_rate = f_s
sdr.center_freq = 900e6
sdr.gain = 4

fig = plt.figure()
ax = plt.axes(ylim=(-20.0, 30)) #xlim=(min(freq), max(freq)), ylim=(0.0, 0.025)
line, = ax.plot([], [], lw=2)
ax.grid()
ax.set_xlabel("Freq")
ax.set_ylabel("Uncalibrated power")

def animate(i):	
	swept_power = np.array([])
	freq = np.linspace(freq_start, freq_start+(N_cycles*f_s), NFFT*N_cycles)	
	for k in range(N_cycles):	
		sdr.center_freq = freq_start + (k+0.5)*f_s
#		print sdr.center_freq
		samples = sdr.read_samples(8*NFFT)
		sig_f = np.fft.fft(a=samples, n=NFFT)
		swept_power = np.append(swept_power, np.abs(np.fft.fftshift(sig_f)))
	
	ax.set_xlim(min(freq), max(freq))
	line.set_data(freq, 10*np.log10(swept_power))
	return line,
	
anim = animation.FuncAnimation(fig, animate, frames=None, interval=1)
plt.show()
sdr.close()
#f.close()

