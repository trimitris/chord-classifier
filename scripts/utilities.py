import scipy.io.wavfile
import numpy as np
import os
import pyaudio
import wave
import time
from plotting import plotAmpl

duration = 2 #seconds
fs = 44100


def convert(to_filetype = 'array'):
	print('start')
	#string number, number of frets per string, first_note of string
	strings = [(6,20),(5,20),(4,19),(3,19),(2,20),(1,20)]

	if (to_filetype == 'array'):
		for string, frets in strings:
			for i in range(frets):
				#read wav file
				name = str("String_{}_Fret_{}".format(string,i))
				path = str('../wavfiles/' + name)
				recording = scipy.io.wavfile.read(path)
				#convert to array

				#save file
				file_name = str('String_{} Fret_{}'.format(string,i))
				path2 = str('../Guitar_notes_440Hz/' + file_name)
				np.savetxt(path2,recording[1])
	elif (to_filetype == 'wav'):
		for string, frets in strings:
			for i in range(frets):
				name = str("String_{} Fret_{}".format(string,i))
				path3 = str('../Guitar_notes_440Hz/' + name)
				#read txt file
				myrecording = np.loadtxt(path3)
				#convert numpy array into wav file
				file_name = str('String_{}_Fret_{}'.format(string,i))
				path4 = str('../wavfiles/' + file_name)
				#convert to wav and save
				scipy.io.wavfile.write(path4, fs, myrecording)
	else:
		raise ValueError('function convert() takes arguments either "array" or "wav"')

	print('end')

def convert_custom(file, to_filetype = 'array'):
	if (to_filetype == 'array'):
		path = str('../custom_recs/' + file)
		recording = scipy.io.wavfile.read(path)
		thresh = 0.4
		array_rec = thresh*np.array(recording[1],dtype = float)
		path = str('../custom_recs/' + file + 't')
		np.savetxt(path, array_rec)
	elif (to_filetype == 'wav'):
		path = str('../custom_recs/' + file)
		recording = np.loadtxt(path)
		reduction_factor = 0.0001
		recording = reduction_factor * recording
		file_name = str(file + '_s')
		path = str('../custom_recs/' + file_name)
		scipy.io.wavfile.write(path, fs, recording)
	else:
		raise ValueError('function convert() takes arguments either "array" or "wav"')

def play(which_string, which_fret):
	#utilizes the play command from the terminal
	#This script has terminal code that can be ran with python
	name = str("String_{}_Fret_{}".format(which_string,which_fret))
	path = str('../wavfiles/' + name)
	os.system('play {}'.format(path))

def play_custom(file_name):
	path = str('../custom_recs/' + file_name)
	os.system('play {}'.format(path))

def record(file_name, seconds):
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = seconds

	audio = pyaudio.PyAudio()

	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)
	print("recording...")
	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	print("finished recording")

	path = str('../custom_recs/' + file_name)
	waveFile = wave.open(path, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

def extractChordLabels(files):
    '''
    extracts the chord labels from the file names
    '''
    labels = []
    for file in files:
        idxStart = file.index('_') + 1
        idxEnd = file[idxStart:].index('_') + idxStart
        label = file[idxStart:idxEnd]
        if (label.find('#') != -1):
            labels.append((label[0:2], label[2:]))
        else:
            labels.append((label[0],label[1:]))
    return labels


if __name__ == "__main__":
	# name = 'guitar_Emaj_s1' #s1 stands for shape 1 (see index.txt)
	# name = 'guitar_F#sus2_s2'
	# record(name,2)
	# convert_custom(name)
	# plotAmpl("custom_recs/",str(name+"t"),44100)
	# name = "guitar_G7_G#dim7_Adim7_G7_G#dim7_Adim7_Gmaj"
	# record(name,8)
	# name = "farewell_ballad_zakk_wylde.wav"
	# name = "poison_alice_cooper.wav"
	name = "nothing_else_matters_metallica.wav"
	convert_custom(name)
