#include "musicData.h"
#include "interface.h"
#include <iostream>
#include <vector>
#include <string>

int main(){
  // std::string directory;
  // std::cin >> directory;
  // analyseDirectory(directory);

  int frameSize = 512;
  std::vector<std::vector<std::vector<double>>> frames = listener();
  std::vector<std::vector<std::string>> chords = analyse(frames, frameSize);
  for (unsigned int i = 0; i<chords.size(); i++){
    postStdout(chords[i],"chord");
  }

  return 0;
}
