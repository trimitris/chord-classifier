# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 18:42:50 2018

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
multiples = [0]*10

print('start')
#string number, number of frets per string, first_note of string
strings = [(6,20,20),(5,20,25),(4,19,30),(3,19,35),(2,20,39),(1,20,44)]

start = time.time()
for string, frets, first_note in strings:
    for i in range(frets):
        name = str("String_{} Fret_{}".format(string,i))
        #print(name)
        myrecording = np.loadtxt(str('../Guitar_notes_440Hz/' + name))      
        signal = myrecording[:,0]
        magn_fourier, freq = get_fft_freq(signal,fs)
        indices, frequencies, rel_ampl = get_peaks(magn_fourier, freq)
        note, num_multiples = fundamental(frequencies)
        #print('note: ', note, 'should be: ', i + first_note)
        if (note != (i + first_note)):
            errors.append((string, i, i + first_note, note))
        else:
        	multiples[num_multiples]+= 1
end = time.time()

print('end')

def report_errors(errors):
    for row in errors:
        print("String: ", row[0], "fret number: ", row[1], "Correct answer: ", row[2], "Classified as: ", row[3])

report_errors(errors)
print('number of multiples of fundamental: ', multiples)
print('timing: ', end - start)
