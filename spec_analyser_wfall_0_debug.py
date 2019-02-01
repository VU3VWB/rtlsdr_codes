import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.signal import periodogram
from pylab import *
from rtlsdr import *

##########################################################################################
start_freq = 100e6
stop_freq = start_freq+2.4e6
samp_rate = 2.4e6
N_SAMPLE = 256
N_FFT = N_SAMPLE
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

    sdr.center_freq = start_freq + k*samp_rate
    	
    samples = sdr.read_samples(N_SAMPLE)
    	
    freqs,pss = periodogram(x=samples, fs=sdr.sample_rate/1e6, window=None, nfft=N_FFT, detrend='constant')
    plt.plot(freqs, pss)
    plt.show()
#    freqs += sdr.center_freq/1e6
#    P_array = np.append(P_array,pss)
#    freq_array = np.append(freq_array, freqs)