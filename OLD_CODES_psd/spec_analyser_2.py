import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.signal import periodogram
from pylab import *
from rtlsdr import *

##########################################################################################
start_freq = 94.3e6 
stop_freq = start_freq+2.4e6
samp_rate = 2.4e6
N_SAMPLE = 256
N_FFT = 256
N_ITER = int((stop_freq-start_freq)/samp_rate)
decim_factor = 1

print "Expected Res BW",samp_rate*1e-6/N_FFT,"MHz"
##########################################################################################

sdr = RtlSdr()
sdr.sample_rate = samp_rate
sdr.gain = 40

P_array = np.array([])
freq_array = np.array([])

for k in range(N_ITER):

	sdr.center_freq = start_freq + k*samp_rate/decim_factor
	
	samples = sdr.read_samples(N_SAMPLE)
	samples = samples - np.mean(samples)
	
	pss, freqs = mlab.psd(x=samples, NFFT=N_FFT, Fs=sdr.sample_rate/1e6)
	freqs += sdr.center_freq/1e6
	
	freqs = freqs[0:len(freqs)/decim_factor]
	pss = pss[0:len(pss)/decim_factor]
	
	P_array = np.append(P_array,pss)
	freq_array = np.append(freq_array, freqs)
  	
#  	plt.figure()
# 	plt.plot(freqs, 10*np.log10(pss))
# 	plt.xlabel('Frequency (MHz)')
# 	plt.ylabel('Relative power (dB)')

plt.figure()
plt.plot(freq_array, 10*np.log10(P_array))
plt.xlabel('Frequency (MHz)')
plt.ylabel('Relative power (dB)')

plt.figure()
plt.plot(freq_array, P_array)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Relative power')

sdr.close()
plt.show()



