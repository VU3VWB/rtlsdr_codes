import aipy as a
import time
import astropy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from astropy.time import Time
from rtlsdr import * 
from scipy import signal

# configure the rtlsdr
sdr = RtlSdr()
sdr.sample_rate = 2.4e6 # Hz
sdr.center_freq = 100.1e6  # Hz
sdr.gain = 'auto'

SAMP_RATE_GHz = sdr.sample_rate/1e9
FREQ_GHz = (sdr.center_freq - sdr.sample_rate/2)/1e9
NFFT = 1024

my_time = time.gmtime(time.time())
file_name = str(my_time.tm_year)+'_'+str(my_time.tm_mon).zfill(2)+'_'+str(my_time.tm_mday).zfill(2)+'-'+str(my_time.tm_hour).zfill(2)+str(my_time.tm_min).zfill(2)+str(my_time.tm_sec).zfill(2)+".dat"

uv = a.miriad.UV(file_name, 'new')
uv['history'] = 'test file\n'

uv.add_var('latitud','d')
uv.add_var('npol','i')
uv.add_var('nspect', 'i')
uv.add_var('obsdec', 'd')
uv.add_var('vsource', 'r')
uv.add_var('ischan', 'i')
uv.add_var('operator', 'a')
uv.add_var('nants', 'i')
uv.add_var('baseline', 'r')
uv.add_var('sfreq', 'd')
uv.add_var('inttime', 'r')
uv.add_var('source', 'a')
uv.add_var('epoch', 'r')
uv.add_var('version', 'a')
uv.add_var('ra', 'd')
uv.add_var('restfreq', 'd')
uv.add_var('nschan', 'i')
uv.add_var('sdf', 'd')
uv.add_var('corr', 'r')
uv.add_var('freq', 'd')
uv.add_var('longitu', 'd')
uv.add_var('nchan', 'i')
uv.add_var('tscale', 'r')
uv.add_var('antpos', 'd')
uv.add_var('telescop', 'a')
uv.add_var('pol', 'i')
uv.add_var('coord', 'd')
uv.add_var('veldop', 'r')
uv.add_var('lst', 'd')
uv.add_var('time', 'd')
uv.add_var('dec', 'd')
uv.add_var('obsra', 'd')

uv['latitud'] = 13.611111*np.pi/180.0
uv['npol'] = 1
uv['nspect'] = 1
uv['obsdec'] = 0.0 
uv['vsource'] = 0.0
uv['ischan'] = 0
uv['operator'] = 'J'
uv['nants'] = 1
uv['baseline'] = 0.0
uv['sfreq'] = FREQ_GHz 
uv['inttime'] = 1.0
uv['source'] = 'SKY'
uv['epoch'] = 2000.0
uv['version'] = 'A'
uv['ra'] = 0.0
uv['restfreq'] = 0.0
uv['nschan'] = NFFT
uv['sdf'] = SAMP_RATE_GHz/NFFT
uv['corr'] = 0.0 
uv['freq'] = 0.0
uv['longitu'] = 77.516667*np.pi/180.0
uv['nchan'] = NFFT
uv['tscale'] = 0.0
uv['antpos'] = 0.0
uv['telescop'] = 'J'
uv['pol'] = 1
uv['coord'] = 0.0
uv['veldop'] = 0.0
uv['lst'] = 0.0
uv['time'] = 0.0
uv['dec'] = 0.0
uv['obsra'] = 0.0

i = 0
try:
	while True:
		accum_data = np.zeros(shape=NFFT, dtype=np.complex64)
		for k in range(128):		
			samples = sdr.read_samples(1*NFFT)
			sig_f = np.fft.fft(a=samples, n=NFFT)
			sig_fx = sig_f*np.conj(sig_f)
			accum_data = accum_data+sig_fx
		
		aver_data = accum_data/128.0
		data_mask = np.zeros(NFFT)
		uvw = np.array([1,2,3], dtype=np.double)
		ut = Time(datetime.utcnow(), scale='utc')
		preamble = (uvw, ut.jd, (0,1))
		data = np.ma.array(aver_data, mask=data_mask, dtype=np.complex64)
		uv.write(preamble,data)
		print "Writing spectrum #"+str(i)
		i=i+1
		
except KeyboardInterrupt:
    print('Acquisition stopped !')
		
finally:	
	del(uv)
	sdr.close()
	print('Exiting')

