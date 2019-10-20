import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from rtlsdr import *
from time import sleep
import time 

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 195e6
sdr.gain = 50

my_time = time.gmtime(time.time())
file_name = str(my_time.tm_year)+'_'+str(my_time.tm_mon).zfill(2)+'_'+str(my_time.tm_mday).zfill(2)+'-'+str(my_time.tm_hour).zfill(2)+str(my_time.tm_min).zfill(2)+str(my_time.tm_sec).zfill(2)+".sdr_pow"
power_array = np.array([])
try:
    while 1:
           samples = sdr.read_samples(sdr.sample_rate)
           power = np.sum(np.abs(samples)**2)
           print power
           power_array = np.append(power_array,power)
except KeyboardInterrupt:
        sdr.close()
np.savetxt(file_name, np.column_stack([power_array]))
plt.plot(power_array)
plt.show()

