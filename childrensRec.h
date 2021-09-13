#pragma once

#include <string>
#include <vector>
#include <opencv2/core.hpp>






std::string timeNow();
void saveTimeImages(std::string &resultsFile, int bedNumber, std::vector<cv::Mat> &prev_frames, std::string &framesFolder);
void childrenRec(std::string videoFile, std::string resultsFile, std::string framesFolder, int bedNumber);
   
    

    
