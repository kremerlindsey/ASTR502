# lomb scargle practice light curve 2

import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle

#------------------------------------------------------# generated with help from ChatGPT 

filepath = "/Users/lindseykremer/Downloads/MAST_2026-01-22T1709/HLSP/hlsp_k2sff_k2_lightcurve_212003686-c05_kepler_v1_llc/use this one.txt"
data = np.genfromtxt(filepath, 
                     delimiter = ',', 
                     skip_header = 1,                  # skips one row (the titles) 
                     usecols = (0,1))                  # ignore the empty third column (column 2)  

#------------------------------------------------------# end

time = data[:, 0]
flux = data[:, 1]

# light curve 

plt.scatter(time, flux, s = 2)
plt.title("Light Curve")
plt.xlabel("BJD - 2454833")
plt.ylabel("Corrected Flux")
plt.show()

# astropy lomb scargle

frequency, power = LombScargle(time, flux).autopower(minimum_frequency = 1/20, maximum_frequency = 0.55)  # just chose frequency range manually

plt.plot(frequency, power)
plt.title("Lomb Scargle Periodogram")
plt.xlabel("frequency")
plt.ylabel("power")
plt.show()

# extracting the period 

max_power_index = np.argmax(power)

max_frequency = frequency[max_power_index]

period = 1 / max_frequency

print("period in days = ", period)

# folding the light curve 

phase = (time % period) / period

plt.scatter(phase, flux, s = 2)
plt.title("Folded Light Curve")
plt.xlabel("Phase")
plt.ylabel("Flux")
plt.show()
