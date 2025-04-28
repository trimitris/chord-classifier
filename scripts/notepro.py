    # -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 00:22:25 2018

@author: Demetris
"""

# import sounddevice as sd
import numpy as np
import math

def get_peaks(magn_fft, freq):
    '''
    input:
        -magn_fft: amplitude of fft
        -freq: array of frequencies of fft
        -min_height: min amplitude the peaks should have to be considered peaks
    returns:
        -array with indices of peaks of the spectrum of magn_fft
        -array with frequencies of peaks
        -array with relative amplitudes of peaks
        -record a bunch of notes
        -write function to name the chords e.g. 49 --> A4
    '''
    indices = []
    frequencies = []
    relative_ampl = []
    initial_idx = 0
    last_idx = 0
    close_to_peak = False
    thresh = 15 #threshold about how far apart the indices of max peaks should be so as not to considered the same peak
    last_peak_idx = 0
    min_height = max(magn_fft)/10 #normalize the min_height

    for i,ampl in enumerate(magn_fft):
        if (ampl > min_height):
            close_to_peak = True
            last_idx = i
        else:
            if (close_to_peak):
                k = np.argmax(magn_fft[initial_idx:last_idx])
                idx = initial_idx + k

                try:
                    last_peak_idx = indices[-1]
                    if (abs(idx - last_peak_idx) < thresh): #handle case when the indices are very close
                        if (magn_fft[idx]>magn_fft[last_peak_idx]):
                            indices[-1] = idx
                    else:
                        indices.append(idx)
                except:
                    indices.append(idx)

                close_to_peak = False

            initial_idx = i
            last_idx = i+1

    for idx in indices:
        frequencies.append(freq[idx])
        relative_ampl.append(magn_fft[idx]/magn_fft[indices[0]])

    return indices, frequencies, relative_ampl

def get_fft_freq(signal,fs):
    '''
    input:
        -signal: sampled signal
        -fs: sampling frequency
    output:
        -magn_fourier: magnitude of fft
        -freq: frequencies of fft
    '''
    fourier = np.fft.fft(signal)
    magn_fourier = np.abs(fourier)
    n = signal.size
    timestep = 1/fs
    freq = np.fft.fftfreq(n, d=timestep)
    return magn_fourier[:int(n/2)], freq[:int(n/2)]

#create dictionary
freq_dict = np.zeros(89)
for n in range(1,89):
    freq_dict[n] = 440*2**((n-49)/12)

def dictionary(freq):
    '''
    input:
        -singe frequency (freq)
    output:
        -frequency of closest note from the frequency dictionary of piano notes
    '''
    compare_array = np.abs( freq_dict - np.full((1,89),freq) )
    idx = np.argmin(compare_array[0,1:]) +1
    return (freq_dict[idx])

def multiples(fundamental, frequencies):
    '''
    input:
        -frequencies array
    output:
        -number of multiples of fundamental exist in frequencies array
    '''
    thresh = 0.1
    counter = 0
    ideal_fundamental = dictionary(fundamental)
    for freq in frequencies:
        factor = (freq/ideal_fundamental)
        if (np.abs(factor - round(factor)) <thresh):
            counter +=1
    return counter

def fundamental(frequencies):
    '''
    input:
        -frequencies array
    output:
        -returns fundamental frequency
        -number of multiple frequencies of the fundamental
    '''
    fundamental = 0
    max_multiples = 0
    for i, freq in enumerate(frequencies):
        num_multiples = multiples(freq,frequencies[i+1:])
        if (num_multiples >= max_multiples):
            max_multiples = num_multiples
            fundamental = freq

    note = 12*math.log(fundamental/440,2) + 49
    return round(note), max_multiples

def get_frames(input, frameSize):
    '''
    returns a numpy array with the frames of the input, which have size given by frameSize
    output[frameNumber][frameSample][channel]
    '''
    numSamples, numChannels = input.shape
    numFrames = int(math.ceil(numSamples/frameSize))
    print(type(numSamples), type(numChannels), type(numFrames))

    output = np.zeros((numFrames, frameSize, numChannels), dtype=np.float)

    frame = 0
    frameSample = 0
    for value in input:
        if (frameSample >= frameSize):
            frameSample = 0
            frame +=1

        output[frame][frameSample][0] = value[0]
        output[frame][frameSample][1] = value[1]
        frameSample +=1

    return output
