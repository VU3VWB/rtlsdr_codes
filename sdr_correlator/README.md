# Correlator based on RTL-SDR

Building a multi-element cross-correlator using RTL-SDRs sharing a common clock. 
Also trying to avoid noise-source based calibration of non-deterministic USB delays, by using POSIX style timestamps for the voltages captured.