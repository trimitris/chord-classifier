// #include "musicData.h"
#include "onsetDetector.h"
#include <string>
#include <vector>
#include <iostream>

int main(){
	// analyse("piano_Dm_oct5_t");

	int frameSize = 512;
	int fs = 44100;
	// std::string directory = std::string("../custom_recs/textfiles/");
	std::string directory = std::string("../guitar/multipleChords/");

	// analyseDirectory(directory, frameSize);
	std::vector<std::string> files = getDir(directory);

	for (unsigned int k=0; k< files.size(); k++){

		int fileSize = files[k].size();

		if (files[k][fileSize -1] != 't'){ continue;}
		std::cout << "file: " << files[k] << "<<-----------------------------------------------<<"<< std::endl << std::endl;
		std::vector<std::vector<std::vector<double>>> frames = preprocessFile(directory, files[k], frameSize);

		std::vector<std::vector<int>> chordGroups = extractChordGroups(frames,6);

		// use chordGroups to print the chords at different times
		bool firstTime = true;
		for (unsigned int i=0; i<chordGroups.size(); i++){
			std::vector<std::vector<std::vector<double>>> musicalEvent(frames.begin() + chordGroups[i][0], frames.begin()+ chordGroups[i][1]);
			std::vector<std::vector<std::string>> chords = analyse(musicalEvent, frameSize);
			std::vector<std::string> chordDetected = chords[chords.size() - 1];
			std::vector<std::string> lastChord;
			if (firstTime){
				std::cout << "Chord at time (sec): " << (double(chordGroups[i][0])/double(fs)*double(frameSize)) << std::endl;
				print_1dvector<std::string>(chordDetected);
				std::cout << std::endl;

				firstTime = false;
			}
			else {
				if (chordDetected != lastChord){
					std::cout << "Chord at time (sec): " << (double(chordGroups[i][0])/double(fs)*double(frameSize)) << std::endl;
					print_1dvector<std::string>(chordDetected);
					std::cout << std::endl;
				}
			}

			lastChord = chordDetected;
		}

	}
	return 0;
}
