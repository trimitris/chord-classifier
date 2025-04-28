# Sound processing
Frame-based chord classifier
fs = 44100
frameSize = 512

# Environment setup:
## Install fftw3.h for Ubuntu:
```console
sudo apt-get install libfftw3-dev libfftw3-doc
```

## System capabilities

Tested with the following chord qualities:
- Minor (triad)
- Major (triad)
- Sus2 (triad)
- Dominant 7th (4 notes)

System could be able to identify also (untested):
- Diminished (triad)
- Augmented (triad)
- Sus4 (triad)
- Major 7th (4 notes)
- Minor 7th (4 notes)

## System components:
- Onset detection
- Chromagram calculation for individual frames
- Chord detection for individual frames
- Chord detection for chordGroups

### Onset detection:
- Separate the music file into frames
- Calculate the signal energy of all frames
- Filter the energy function using a gaussian kernel
- Identify max points and steps
- Separate the frames into different chordGroups (an event is a sudden increase in energy):
	- chordGroups start at a max point in energy function
	- End when energy decays by a certain factor of its original max value, or
	when a new step is detected

### Chromagram calculation for individual frames
- Calculate the DFT of the input frames
- Calculate the Chroma vector by finding the energy content of the input
frames at the location of the 12 semitones across different octaves. The
energies are then summarized in the 12 elements of a chroma vector, one for
each semitone.
- This system generates the chroma vector by only looking at 2 octaves spanning
from C3 to C5

### Chord detection for individual frames
- Calculate the energy of the chroma vector, by first filtering out the notes
that are hypothesized to be found in the chord.
- This is achieved by calculating the complementary mask of the hypothesized chord
- This is repeated for different hypothesized chords (with chord qualities: minor, major etc)
- Choose the chord which minimises the energy outside its mask
- This is done instead of finding the hypothesised chord the maximises the energy inside its mask,
because the latter method is susceptible to the variability of the dominant notes in the mask

### Chord detection for chordGroups
- Select the chord which has been identified in the majority of the individual frames of that
chordGroup


## Future work
- Context: perform full music transcription for a single instrument (guitar)
- Use machine learning techniques for onset detection, chord detection, beat tracking etc
