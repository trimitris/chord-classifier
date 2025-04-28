#include "musicData.h"

std::vector< std::vector <double>> importMusicFile(std::string fileName) {
	// import the music samples from a .txt file into a vector

	std::string line, number;
	std::vector < std::vector<double>> output;

	std::ifstream myfile (fileName);
	if (myfile.is_open())
	{
		//read each line from the txt file into a string
		while ( std::getline (myfile,line) ) {
			std::istringstream ss(line);
			std::vector<double> row;
			//break down each line into the individual numbers
			while (std::getline(ss,number, ' ')) {
				row.push_back(atof(number.c_str()));
			}

			output.push_back(row);
		}
		myfile.close();
	}

	else throw std::runtime_error("Unable to open file");

	return output;
}

std::vector < std::vector <double>> splitChannels(std::vector <std::vector<double>> input){
	int numSamples = input.size();
	int channels = input[0].size();
	//initialise output vector
	std::vector <std::vector<double>> output(channels, std::vector<double>(numSamples));

	for (int c = 0; c <channels; c++){
		for (int s = 0; s<numSamples; s++){
			output[c][s] = input[s][c];
		}
	}

	return output;
}

std::vector<std::string> getDir (std::string dir) {
  // return vector with the files in a directory
  std::vector<std::string> files;
  DIR *dp;
  struct dirent *dirp;
  if ((dp  = opendir(dir.c_str())) == NULL) {
    throw std::runtime_error("Error whilst opening directory, error number: " + std::to_string(errno));
  }

  while ((dirp = readdir(dp)) != NULL) {
    std::string file = std::string(dirp->d_name);
    //skip files starting with a dot
    if (file[0] == '.') continue;
    files.push_back(file);
  }
  closedir(dp);
  return files;
}

std::vector<std::vector<std::vector<double>>> splitFrames(std::vector<std::vector<double>> data, int frameSize) {
	//splits the data into frames keeping both channels
	std::vector<std::vector<std::vector<double>>> output;

	int numSamples = data.size();

	std::vector<std::vector<double>> frame;
	int counter = 0;

	for (int i = 0; i < numSamples; i++){
		if (counter >= frameSize) {
			output.push_back(frame);
			frame.clear();
			counter = 0;
		}
		frame.push_back(data[i]);
		counter++;
	}

	//handle case when the last frame wasn't completed
	if (counter > 0) {
		std::vector<double> padding = {0.0,0.0};
		for (int i = counter; i<frameSize; i++){
			frame.push_back(padding);
		}
	}
	output.push_back(frame);

	return output;
}

std::vector<std::vector<std::vector<double>>> preprocessFile(std::string path, std::string fileName, int frameSize){
	// imports a music file from the given path and separates it into channels and frames
	std::string fullPath = path + fileName;
	std::vector < std::vector<double>> matrix = importMusicFile(fullPath);

	std::vector<std::vector<std::vector<double>>> frames = splitFrames(matrix,frameSize);
	return frames;
}


std::vector< std::vector<std::string>> analyse(std::vector<std::vector<std::vector<double>>> frames, int frameSize){
	// find chroma of the music file and chord quality (for channel 0)
	// The output vector contains the various chord labels identified at different frames.
	// The final entry in the output vector is the chord label selected by majority vote
	int sampleRate = 44100;
	std::vector< std::vector<std::string>> output;
	int chordCounter[12][6] = {0}; // chord counter is initialised by taking into account that only 6 chord qualities are identified

	Chromagram c(frameSize, sampleRate);
	ChordDetector chordDetector;

	for (unsigned int i = 0; i < frames.size(); i++){

		// print_1dvector<double>(splitChannels(frames[i])[0]);

		c.processAudioFrame(splitChannels(frames[i])[0]);

		if (c.isReady()){
			std::vector<double> chroma = c.getChromagram();

			// std::cout << "chroma vector, at: \t" << (int)(((float)(i+1)/(float)frames.size())*100) << "\% of file" << std::endl;
			// print_1dvector<double>(chroma);
			// std::cout << std::endl;
			chordDetector.detectChord(chroma);

			// save the chord data into a vector<string> because this way, it can also be used for interfacing with Python
			std::vector<std::string> chord = {chordDetector.getRootNote(chordDetector.rootNote),chordDetector.getChordQuality(chordDetector.quality)};
			output.push_back(chord);
			chord.clear();

			// Keep a record of the chords identified
			chordCounter[chordDetector.rootNote][chordDetector.quality]++;
		}

	}

	// Select chord label by majority vote
	int idxi =0;
	int idxj = 0;
	int max = 0;

	for (int i = 0; i<12; i++){
		for (int j = 0; j<6; j++){
			if (chordCounter[i][j] >= max){
				max = chordCounter[i][j];
				idxi = i;
				idxj = j;
			}
		}
	}

	// save the selected chord label in the output vector
	std::vector<std::string> chord = {chordDetector.getRootNote(idxi),chordDetector.getChordQuality(idxj)};
	output.push_back(chord);
	chord.clear();

	return output;
}

void analyseDirectory(std::string directory, int frameSize){
	//analyse files in the directory
	std::vector<std::string> files = getDir(directory);

	for (unsigned int i = 0; i < files.size(); i++){
		std::cout << "file: " << files[i] << "<<-----------------------------------------------<<"<< std::endl << std::endl;
		std::vector<std::vector<std::vector<double>>> data = preprocessFile(directory, files[i], frameSize);
		std::vector< std::vector<std::string>> chords = analyse(data,frameSize);

		// cout the chords
		for (unsigned int j = 0; j<chords.size(); j++){
			std::cout << "chord quality: " << chords[j][0] << " " << chords[j][1] << std:: endl;
		}
	}
}
