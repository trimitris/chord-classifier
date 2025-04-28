# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:07:26 2018

@author: Demetris
"""

import sounddevice as sd
import scipy.io.wavfile
import numpy as np

duration = 2 #seconds
fs = 44100

name = str("String_{} Fret_{}".format(6,1))
myrecording = np.loadtxt(name)
print(type(myrecording))

#convert numpy array into wav file
scipy.io.wavfile.write('String_6_Fret_1', 44100, myrecording)
# for i in range(20):
#     name = str("String_{} Fret_{}".format(6,i))
#     print(name)
#     myrecording = np.loadtxt(name)
#     sd.play(myrecording,fs)
#     print("finish")