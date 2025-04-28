#include "interface.h"

std::vector<std::vector<std::vector<double>>> listener(){
  /*
  * This function listens for Stdin and receives data
  */
  std::string line;
  std::vector<std::vector<std::vector<double>>> frames;

  while (std::getline(std::cin, line)) {
    if (line == "<frame>") {
      std::vector<std::vector<double>> frame = receiveFrame();
      // print_2dvector(frame);
      // std::cout << std::endl;
      frames.push_back(frame);

    }
  }

  return frames;
}

std::vector<std::vector<double>> receiveFrame(){
  /*
  * Receives musical frames and stores them in a vector. The end of a frame is identified by the tag "</frame>"
  */
  std::string line, temp;
  std::vector < std::vector<double>> frame;

  std::getline(std::cin, line);
  while (line != "</frame>") {
    // for each individual line of stdin:
    std::istringstream ss(line);
    double number;
    std::vector<double> sample;

    //break down each line into the individual words
    while (!ss.eof()){
      ss >> temp;

      // detect if each word is a number
      if (std::stringstream(temp) >> number){
        sample.push_back(number);
      }
    }
    frame.push_back(sample);
    std::getline(std::cin, line);
  }
  return frame;
}

void postStdout(std::vector<std::string> data ,std::string tag){
  /*
  * General purpose function for posting data to stdout that are preceded by the tag
  */
  std::cout << "<" << tag << ">" << std::endl;
  for (unsigned int i = 0; i < data.size(); i++) {
    std::cout << data[i] << std::endl;
  }
  std::cout << "</" << tag << ">" << std::endl;
}
