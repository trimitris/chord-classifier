# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 00:46:58 2018

@author: Demetris
"""
'''
Taken from: https://python-sounddevice.readthedocs.io/en/0.3.10/
'''

import sounddevice as sd
import numpy as np

duration = 2 #seconds
fs = 44100


#mass recording!
#for i in range(20):
#    print("start recording", i)
#    myrecording = sd.rec(int(duration*fs), samplerate = fs, channels =2)
#    sd.wait()
#    print("done recording")
#    #save sound
#    name = str("String_{} Fret_{}".format(1,i))
#    np.savetxt(name,myrecording)
#    
#record sound
print("start recording")
myrecording = sd.rec(int(duration*fs), samplerate = fs, channels =2)
sd.wait()
print("done recording")

#save sound
name = str("alarm")
np.savetxt(name,myrecording)

#Play sound
sd.play(myrecording,fs)
print("finish")
print(myrecording.shape)