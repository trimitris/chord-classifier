# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 18:42:50 2018

@author: Demetris
"""

import numpy as np
import time
from notepro import get_fft_freq, get_peaks, fundamental

#main
#-----------------
duration = 2 #seconds
fs = 44100

#error report: (string, fret number, what it should be, what it thinks it is)
errors = []
multiples = [0]*20

print('start')

start = time.time()

for i in range(1,66):
    file_name = 'piano_{}'.format(i)
    myrecording = np.loadtxt(str('../piano/' +file_name))
    signal = myrecording[:,0]
    magn_fourier, freq = get_fft_freq(signal,fs)
    indices, frequencies, rel_ampl = get_peaks(magn_fourier, freq)
    note, num_multiples = fundamental(frequencies)
    #print('note: ', note, 'should be: ', i + first_note)
    if (note != i):
        errors.append((i, note))
    else:
        multiples[num_multiples]+= 1

end = time.time()

print('end')

def report_errors(errors):
    for row in errors:
        print("Piano key: ", row[0], "Classified as: ", row[1])

report_errors(errors)
print('number of multiples of fundamental: ', multiples)
print('timing: ', end - start)
